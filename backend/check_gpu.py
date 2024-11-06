import torch
print("CUDA available:", torch.cuda.is_available())  # Should print True
print("GPU count:", torch.cuda.device_count())       # Should print the number of GPUs detected
print("GPU name:", torch.cuda.get_device_name(0))    # Should print the name of your GPU
