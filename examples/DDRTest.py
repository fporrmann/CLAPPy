import random
from CLAPPy import CLAP, CLAPBuffer32u, CLAPBuffer32s

DDR_BASE = 0x000000000
DDR_SIZE = 0x100000000

TEST_DWORD = 0xDEADBEEF
TEST_ADDR = DDR_BASE

TEST_DATA_TYPE_BYTES = 4
TEST_DATA_SIZE = 0x1000
TEST_DATA_BYTE_SIZE = TEST_DATA_SIZE * TEST_DATA_TYPE_BYTES

# Create a CLAP object
clap = CLAP.CreatePCIe()

# Add a memory region
clap.AddMemoryRegion(CLAP.MemoryType.DDR, DDR_BASE, DDR_SIZE)

# Write and read a 32-bit value
clap.Write32(TEST_ADDR, TEST_DWORD)
if clap.Read32(TEST_ADDR) == TEST_DWORD:
	print("Single Write/Read Test passed")
else:
	print("Single Write/Read Test failed")

# Initialize a list of unsigned 32-bit values
data = CLAPBuffer32u([0xDEADBEEF, 0xCAFEBABE, 0x12345678, 0x87654321])

# Write and read a list of unsigned 32-bit values
clap.Write(TEST_ADDR, data)
r = clap.Read32u(TEST_ADDR, len(data) * TEST_DATA_TYPE_BYTES)
if r == data:
	print("Small Block Write/Read Test passed")
else:
	print("Small Block Write/Read Test failed")

# Initialize a list of random signed 32-bit values
data = CLAPBuffer32s(random.sample(range(-0xFFFFF, 0xFFFFF), TEST_DATA_SIZE))

# Allocate a buffer in DDR
buf = clap.AllocMemoryDDR(elements=TEST_DATA_SIZE, sizeOfElement=TEST_DATA_TYPE_BYTES)

# Write and read a list of random signed 32-bit values
clap.Write(buf, data)
res = clap.Read32s(buf, TEST_DATA_BYTE_SIZE)

if res == data:
	print("Large Block Write/Read Test passed")
else:
	print("Large Block Write/Read Test failed")
