import random
from CLAPPy import CLAP
from CLAPPy import HLSCore

DDR_BASE_ADDR = 0x000000000
DDR_SIZE      = 0x100000000

BRAM_BASE_ADDR= 0x102000000
BRAM_SIZE = 0x2000


AXIDMA_BASE_ADDR = 0x100130000

HLS_CORE_BASE_ADDR = 0x100100000
HLS_ADDR_PDDRIN_DATA   = 0x10
HLS_ADDR_PDDROUT_DATA  = 0x1c
HLS_ADDR_ELEMENTS_DATA = 0x28

TEST_DATA_SIZE = 0x100000
TEST_DATA_TYPE_BYTES = 4

# Create a CLAP object
clap = CLAP.CreatePCIe()

# Add a memory region
clap.AddMemoryRegion(CLAP.MemoryType.DDR, DDR_BASE_ADDR, DDR_SIZE)

dataIn = random.sample(range(0, 0xFFFFFFFF), TEST_DATA_SIZE)
dataOut = [0xFFFFFFFF] * TEST_DATA_SIZE

hlsTest = HLSCore(clap, HLS_CORE_BASE_ADDR, "hlsTest")

# Allocate a buffer in DDR
inBuf = clap.AllocMemoryDDR(elements=TEST_DATA_SIZE, sizeOfElement=TEST_DATA_TYPE_BYTES)
outBuf = clap.AllocMemoryDDR(elements=TEST_DATA_SIZE, sizeOfElement=TEST_DATA_TYPE_BYTES)

hlsTest.SetDataAddr(HLS_ADDR_PDDRIN_DATA, inBuf)
hlsTest.SetDataAddr(HLS_ADDR_PDDROUT_DATA, outBuf)
hlsTest.SetDataAddr(HLS_ADDR_ELEMENTS_DATA, TEST_DATA_SIZE)

# Write and read a list of random signed 32-bit values
clap.Write(inBuf, dataIn)
clap.Write(outBuf, dataOut)

# hlsTest.EnableInterrupts(eventNo=0)
hlsTest.Start()

hlsTest.WaitForFinish()

print(f"HLS Test finished after: {hlsTest.GetRuntime()} ms")

hlsTest.DisableInterrupts()
dataOut = clap.Read32u(outBuf)

checkData = [x+5 for x in dataIn]

if dataOut == checkData:
	print("HLS Test passed")
else:
	print("HLS Test failed")