#!/bin/bash

STUB_ENV_NAME="stub_env"
CLAPPY_DIR="../.."
FILE_NAME="CLAPPy"
FILE_EXT="pyi"
OUTPUT_FILE="$FILE_NAME.$FILE_EXT"
OUTPUT_PATH="$CLAPPY_DIR/$OUTPUT_FILE"

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

echo "Generating stubs ..."
pybind11-stubgen --enum-class-locations=DMAChannel:CLAPPy.CLAP \
--enum-class-locations=Verbosity:CLAPPy.CLAP \
--enum-class-locations=DualChannel:CLAPPy.AxiGPIO  \
--enum-class-locations=ResetOnInit:CLAPPy.AxiGPIO \
--enum-class-locations=GPIOInterrupts:CLAPPy.AxiGPIO \
--enum-class-locations=AddressType:CLAPPy.HLSCore \
--enum-class-locations=APInterrupts:CLAPPy.HLSCore \
--enum-class-locations=DMAInterrupts:CLAPPy.AxiDMA \
--enum-class-locations=VDMAInterrupts:CLAPPy.VDMA \
--print-invalid-expressions-as-is \
-o $CLAPPY_DIR \
--stub-extension $FILE_EXT \
CLAPPy

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
	echo "from typing import Union"
	echo "CLAPBufferType = Union["
	echo "	CLAPBuffer8s,"
	echo "	CLAPBuffer16s,"
	echo "	CLAPBuffer32s,"
	echo "	CLAPBuffer64s,"
	echo "	CLAPBuffer8u,"
	echo "	CLAPBuffer16u,"
	echo "	CLAPBuffer32u,"
	echo "	CLAPBuffer64u,"
	echo "]"
} >> "$OUTPUT_PATH"

# Update the __all__ = [] list to include the new type
sed -i "s/\(__all__ = \[.*\)\]/\1, 'CLAPBufferType']/" "$OUTPUT_PATH"

echo "Done"