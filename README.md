# CLAPPy
Python bindings for [CLAP](https://github.com/fporrmann/CLAP)

**This package is currently still under development and only PCIe and PetaLinux have been partially tested.**

## Requirements
- Python >= 3.7
- CMake >= 3.24
- g++ >= 9 or comparable compiler supporting C++17

## Installation
```bash
# Crate a virtual environment
python3 -m venv clappy_env
# Activate the virtual environment
source clappy_env/bin/activate
# Clone the repository
git clone https://github.com/fporrmann/CLAPPy.git
cd CLAPPy
# Build and install the package
pip install .
# use ```pip install . -v ``` for verbose log output 
```

## Usage
Refer to the examples in the `examples` folder.

To create a PCIe object use:

	CLAPPy.CLAP.CreatePCIe()

To create a PetaLinux object use:

	CLAPPy.CLAP.CreatePetaLinux()
