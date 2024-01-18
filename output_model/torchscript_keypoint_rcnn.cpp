// Copyright (c) Facebook, Inc. and its affiliates.
// @lint-ignore-every CLANGTIDY
// This is an example code that demonstrates how to run inference
// with a torchscript format Mask R-CNN model exported by ./export_model.py
// using export method=tracing, caffe2_tracing & scripting.

#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>

#include <c10/cuda/CUDAStream.h>
#include <torch/csrc/autograd/grad_mode.h>
#include <torch/csrc/jit/runtime/graph_executor.h>

#include <torch/script.h>

#include <torchvision/vision.h> // @oss-only
// @fb-only: #include <torchvision/csrc/vision.h>

using namespace std;



c10::IValue get_tracing_inputs(cv::Mat& img, c10::Device device) {
  const int height = img.rows;
  const int width = img.cols;
  const int channels = 3;

  auto input =
      torch::from_blob(img.data, {height, width, channels}, torch::kUInt8);
  // HWC to CHW
  input = input.to(device, torch::kFloat).permute({2, 0, 1}).contiguous();
  return input;
}



c10::IValue
get_inputs(cv::Mat& img, c10::Device device) {
  return get_tracing_inputs(img, device);
}

struct KeypointRCNNOutputs {
  at::Tensor pred_boxes, pred_classes, pred_heatmaps, keypoints,scores,imgsize;
  int num_instances() const {
    return pred_boxes.sizes()[0];
  }
};

KeypointRCNNOutputs get_outputs(c10::IValue outputs) {
  // Given outputs of the model, extract tensors from it to turn into a
  // common KeypointRCNNOutputs format.

  auto out_tuple = outputs.toTuple()->elements();
  // They are ordered alphabetically by their field name in Instances
  return KeypointRCNNOutputs{
    out_tuple[0].toTensor(),
    out_tuple[1].toTensor(),
    out_tuple[2].toTensor(),
    out_tuple[3].toTensor(),
    out_tuple[4].toTensor(),
    out_tuple[5].toTensor(),
  };
}

int main(int argc, const char* argv[]) {
  if (argc != 3) {
    cerr << R"xx(
Usage:
   ./torchscript_mask_rcnn model.ts input.jpg 
)xx";
    return 1;
  }
  std::string image_file = argv[2];
  torch::jit::getBailoutDepth()=1;
  // cout << "t:::::::::::::::;" << t << endl;
  // torch::_C::_jit_set_profiling_executor(False);
  // torch::jit::FusionStrategy strat = {{torch::jit::FusionBehavior::DYNAMIC, 1}};
  // torch::jit::setFusionStrategy(strat);
  // at::AutoNonVariableTypeMode nonVarTypeModeGuard(true);
  torch::autograd::AutoGradMode guard(false);
  auto module = torch::jit::load(argv[1]);

  assert(module.buffers().size() > 0);
  // Assume that the entire model is on the same device.
  // We just put input to this device.
  auto device = (*begin(module.buffers())).device();

  cv::Mat input_img = cv::imread(image_file, cv::IMREAD_COLOR);
  // cv::cvtColor(input_img,input_img,cv::COLOR_BGR2RGB);
  
  auto inputs = get_inputs(input_img, device);


  auto output = module.forward({inputs});

  if (device.is_cuda())
    c10::cuda::getCurrentCUDAStream().synchronize();


  auto rcnn_outputs = get_outputs(output);
//   cout << "Number of detected objects: " << rcnn_outputs.num_instances()
//        << endl;

  cout << "pred_boxes: " << rcnn_outputs.pred_boxes << " "
       << rcnn_outputs.pred_boxes.sizes() << endl;
  cout << "scores: " << rcnn_outputs.scores << " "
       << rcnn_outputs.scores.sizes() << endl;
  cout << "pred_classes: " << rcnn_outputs.pred_classes<< " "
       << rcnn_outputs.pred_classes.sizes() << endl;
  cout << "pred_keypoints: " << rcnn_outputs.keypoints << " "
       << rcnn_outputs.keypoints.sizes() << endl;


  auto keypoints = rcnn_outputs.keypoints.to(torch::kCPU);

  auto accessor = keypoints.accessor<float,3>();

  vector<vector<float> > points;

  for (int i = 0; i< keypoints.size(1); i++){
    vector<float> coordinates;
    for(int j = 0; j< keypoints.size(2);j++){
      coordinates.push_back(accessor[0][i][j]);
    }
    points.push_back(coordinates);
  }

  

  for(const auto& coordinates : points){
    cv::circle(input_img,cv::Point(coordinates[0],coordinates[1]),1,cv::Scalar(0,255,0),2);
    
  }
  cv::imshow("image",input_img);
  cv::waitKey(0);
  cv::destroyAllWindows();

//   cout << rcnn_outputs.pred_boxes << endl;
  return 0;
}
