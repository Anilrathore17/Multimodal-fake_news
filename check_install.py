# save as check_install.py and run: python check_install.py

libs = [
    "torch",
    "torchvision",
    "transformers",
    "datasets",
    "open_clip",
    "PIL",
    "timm",
    "cv2",
    "langchain",
    "sklearn",
    "numpy",
    "pandas",
    "streamlit",
    "huggingface_hub",
    "tqdm",
    "requests",
]

print("Checking libraries...\n")
failed = []
for lib in libs:
    try:
        __import__(lib)
        print(f"  ✅  {lib}")
    except ImportError:
        print(f"  ❌  {lib}  <-- NOT installed")
        failed.append(lib)

print("\n")
if failed:
    print(f"Fix these: pip install {' '.join(failed)}")
else:
    print("All libraries installed successfully!")

import torch
print(f"\nPyTorch version : {torch.__version__}")
print(f"GPU available   : {torch.cuda.is_available()}")