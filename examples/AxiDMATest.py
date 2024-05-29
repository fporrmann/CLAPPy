from random import randint
from CLAPPy import CLAP
from CLAPPy import AxiDMA

DDR_BASE_ADDR = 0x000000000
DDR_SIZE      = 0x100000000

BRAM_BASE_ADDR= 0x102000000
BRAM_SIZE = 0x2000

AXIDMA_BASE_ADDR = 0x100130000

TEST_DATA_SIZE = 0x100
TEST_DATA_TYPE_BYTES = 4

# Create a CLAP object
clap = CLAP.CreatePCIe()

# Add a memory region
clap.AddMemoryRegion(CLAP.MemoryType.DDR, DDR_BASE_ADDR, DDR_SIZE)

# Fill dataIn with random values
dataIn = []
for _ in range(0,TEST_DATA_SIZE):
	dataIn.append(randint(0, 0xFFFFFFFF))

dataOut = [0xFFFFFFFF] * TEST_DATA_SIZE

axiDMA = AxiDMA(clap, AXIDMA_BASE_ADDR)

axiDMA.Reset()

CLAP.SetWatchDogPollSleepTimeMS(1)

# axiDMA.EnableInterrupts(eventNoMM2S=3, eventNoS2MM=4)

# Allocate a buffer in DDR
inBuf = clap.AllocMemoryDDR(elements=TEST_DATA_SIZE, sizeOfElement=TEST_DATA_TYPE_BYTES)
outBuf = clap.AllocMemoryDDR(elements=TEST_DATA_SIZE, sizeOfElement=TEST_DATA_TYPE_BYTES)

print(f"Input Buffer : {inBuf}")
print(f"Output Buffer: {outBuf}")

# Write and read a list of random signed 32-bit values
clap.Write(inBuf, dataIn)
clap.Write(outBuf, dataOut)

print(f"Starting AXI DMA transfer without interrupts")
axiDMA.Start(inBuf, outBuf)

axiDMA.WaitForFinish()

print(f"AXI DMA transfer finished")
print(f"MM2S Runtime: {axiDMA.GetMM2SRuntime()} ms")
print(f"S2MM Runtime: {axiDMA.GetS2MMRuntime()} ms")

dataOut = clap.Read32u(outBuf)

if dataIn == dataOut:
	print("AxiDMA Test passed")
else:
	print("AxiDMA Test failed")


axiDMA.Reset()

axiDMA.EnableInterrupts(eventNoMM2S=3, eventNoS2MM=4)

# Starting AXI DMA transfer with interrupts
print(f"Starting AXI DMA transfer with interrupts")
axiDMA.Start(inBuf, outBuf)

axiDMA.WaitForFinish()

print(f"AXI DMA transfer finished")
print(f"MM2S Runtime: {axiDMA.GetMM2SRuntime()} ms")
print(f"S2MM Runtime: {axiDMA.GetS2MMRuntime()} ms")

dataOut = clap.Read32u(outBuf)

if dataIn == dataOut:
	print("AxiDMA Test passed")
else:
	print("AxiDMA Test failed")
