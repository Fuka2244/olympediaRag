import torch
import accelerate
import bitsandbytes

print(f"加速库版本: {accelerate.__version__}")
print(f"是否检测到显卡: {torch.cuda.is_available()}")
print(f"当前显卡: {torch.cuda.get_device_name(0)}")