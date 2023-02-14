from openvino.runtime import Core
from openvino.offline_transformations import serialize



ie = Core()
print("initial Core engine:{}".format(ie))

devices = ie.available_devices
for device in devices:
    device_name = ie.get_property(device_name = device,name = "FULL_DEVICE_NAME")
    print(f"{device}:{device_name}")

onnx_model = "/home/zy/vision/detectron2/output_model/model.onnx"
# onnx_model = "/home/zy/Downloads/openvino_ir_model/resnet18_ir/resnet18.onnx"

model = ie.read_model(model = onnx_model)
compiled_model = ie.compile_model(model = model,device_name = "CPU")

input_layer = model.input(0)
print(input_layer)
print("input precision:{}".format(input_layer.element_type))
print("input shape:{}".format(input_layer.shape))