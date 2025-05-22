#!/bin/bash

STUB_ENV_NAME="stub_env"
CLAPPY_DIR="../.."
FILE_NAME="CLAPPy"
FILE_EXT="pyi"
OUTPUT_FILE="$FILE_NAME.$FILE_EXT"
OUTPUT_DIR="CLAPPy"
OUTPUT_PATH="$CLAPPY_DIR/$OUTPUT_DIR/$OUTPUT_FILE"

REBUILD_CLAPPY=0

# Check if the user provided a command line argument
if [ $# -gt 0 ]; then
	if [ "$1" == "rebuild" ]; then
		REBUILD_CLAPPY=1
	fi
fi

# If the environment does not exist, create it
if [ ! -d "$STUB_ENV_NAME" ]; then
	echo -n "Creating virtual environment ... "
	python3 -m venv $STUB_ENV_NAME
	echo "Done"
	echo -n "Activating virtual environment ... "
	source $STUB_ENV_NAME/bin/activate
	echo "Done"
	echo "Installing requirements ... "
	pip install -r requirements.txt
	echo "Requirements installed successfully."
else
	echo -n "Activating virtual environment... "
	source $STUB_ENV_NAME/bin/activate
	echo "Done"
fi

# Check if CLAPPy is not installed
if ! python -c "import CLAPPy" &> /dev/null; then
	REBUILD_CLAPPY=1
fi

if [ $REBUILD_CLAPPY -eq 1 ]; then
	echo "Installing CLAPPy ..."
	pip install $CLAPPY_DIR
	echo "CLAPPy installed successfully."
fi

echo "Generating stubs in $OUTPUT_PATH ... "
pybind11-stubgen --enum-class-locations=DMAChannel:CLAPPy.CLAPPy.CLAP \
--enum-class-locations=Verbosity:CLAPPy.CLAPPy.CLAP \
--enum-class-locations=DualChannel:CLAPPy.CLAPPy.AxiGPIO  \
--enum-class-locations=ResetOnInit:CLAPPy.CLAPPy.AxiGPIO \
--enum-class-locations=GPIOInterrupts:CLAPPy.CLAPPy.AxiGPIO \
--enum-class-locations=AddressType:CLAPPy.CLAPPy.HLSCore \
--enum-class-locations=APInterrupts:CLAPPy.CLAPPy.HLSCore \
--enum-class-locations=DMAInterrupts:CLAPPy.CLAPPy.AxiDMA \
--enum-class-locations=VDMAInterrupts:CLAPPy.CLAPPy.VDMA \
--print-invalid-expressions-as-is \
-o $CLAPPY_DIR \
--stub-extension $FILE_EXT \
CLAPPy.CLAPPy

# Check the return code of the last command
if [ $? -ne 0 ]; then
	echo "Error: Failed to generate stubs."
	exit 1
fi

# Check if the output file exists
if [ ! -f "$OUTPUT_PATH" ]; then
	echo "Error: Output file $OUTPUT_PATH does not exist."
	exit 1
fi

echo "Stubs generated successfully."

echo -n "Cleaning up stubs ... "
# Replace occurences of 4294967295 with 0xFFFFFFFF in the generated stubs
sed -i 's/4294967295/0xFFFFFFFF/g' "$OUTPUT_PATH"

# Remove import pybind11_stubgen.typing_ext
sed -i '/import pybind11_stubgen.typing_ext/d' "$OUTPUT_PATH"

# Replace typing.Annotated[list[int], pybind11_stubgen.typing_ext.FixedSize(2)] with Tuple[int, int]
sed -i 's/typing.Annotated\[list\[int\], pybind11_stubgen.typing_ext.FixedSize(2)\]/Tuple\[int, int\]/g' "$OUTPUT_PATH"

# Replace callback: std::function<void (unsigned int)> with callback: Callable[[int], None]
sed -i 's/callback: std::function<void (unsigned int)>/callback: Callable[[int], None]/g' "$OUTPUT_PATH"

# Replace callback: std::function<void (clap::AxiGPIO::Channel const&, unsigned int const&, bool const&)> with callback: Callable[[AxiGPIO.Channel, int, bool], None]
sed -i 's/callback: std::function<void (clap::AxiGPIO::Channel const&, unsigned int const&, bool const&)>/callback: Callable[[AxiGPIO.Channel, int, bool], None]/g' "$OUTPUT_PATH"

## At the end of the file, add the following:
{
	echo ""
	echo "from typing import Type, Union, Callable"
	echo ""
	echo "CLAPBufferInst = Union["
	echo "	CLAPBuffer8s,"
	echo "	CLAPBuffer16s,"
	echo "	CLAPBuffer32s,"
	echo "	CLAPBuffer64s,"
	echo "	CLAPBuffer8u,"
	echo "	CLAPBuffer16u,"
	echo "	CLAPBuffer32u,"
	echo "	CLAPBuffer64u,"
	echo "]"
	echo ""
	echo "CLAPBufferType = Union["
	echo "	Type[CLAPBuffer8s],"
	echo "	Type[CLAPBuffer16s],"
	echo "	Type[CLAPBuffer32s],"
	echo "	Type[CLAPBuffer64s],"
	echo "	Type[CLAPBuffer8u],"
	echo "	Type[CLAPBuffer16u],"
	echo "	Type[CLAPBuffer32u],"
	echo "	Type[CLAPBuffer64u],"
	echo "]"
	echo ""
	echo "CLAPCreateType = Union["
	echo "	Callable[[], CLAP.CreatePCIe],"
	echo "	Callable[[], CLAP.CreatePetaLinux],"
	echo "]"
} >> "$OUTPUT_PATH"

# Update the __all__ = [] list to include the new types
sed -i "s/\(__all__ = \[.*\)\]/\1, 'CLAPBufferInst', 'CLAPBufferType', 'CLAPCreateType']/" "$OUTPUT_PATH"

echo "Done"