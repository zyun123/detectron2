cmake_minimum_required(VERSION 3.12 FATAL_ERROR)
project(torchscript_keypoint_rcnn)

set(Torch_DIR /home/zy/Downloads/libtorch-cxx11-abi-shared-with-deps-1.9.1+cu111/libtorch/share/cmake/Torch)
find_package(Torch REQUIRED)
find_package(OpenCV REQUIRED)
find_package(TorchVision REQUIRED)   # needed by export-method=tracing/scripting
# find_package(Python3 COMPONENTS Development)
add_executable(torchscript_keypoint_rcnn torchscript_keypoint_rcnn.cpp)
# target_link_libraries(
#   torchscript_mask_rcnn
#   -Wl,--no-as-needed TorchVision::TorchVision -Wl,--as-needed
#   "${TORCH_LIBRARIES}" ${OpenCV_LIBS})

target_link_libraries(torchscript_keypoint_rcnn   "${OpenCV_LIBS}"  "${TORCH_LIBRARIES}" TorchVision::TorchVision)

set_property(TARGET torchscript_keypoint_rcnn PROPERTY CXX_STANDARD 14)
