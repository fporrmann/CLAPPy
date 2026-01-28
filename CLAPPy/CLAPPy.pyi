from __future__ import annotations
import typing
__all__ = ['AxiDMA', 'AxiGPIO', 'AxiInterruptController', 'CLAP', 'CLAPBuffer16s', 'CLAPBuffer16u', 'CLAPBuffer32s', 'CLAPBuffer32u', 'CLAPBuffer64s', 'CLAPBuffer64u', 'CLAPBuffer8s', 'CLAPBuffer8u', 'ClapExp', 'HLSCore', 'Memory', 'MemoryExp', 'VDMA', 'CLAPBufferInst', 'CLAPBufferType', 'CLAPCreateType']
class AxiDMA:
    class DMAInterrupts:
        """
        Members:
        
          INTR_ON_COMPLETE
        
          INTR_ON_DELAY
        
          INTR_ON_ERROR
        
          INTR_ALL
        """
        INTR_ALL: typing.ClassVar[AxiDMA.DMAInterrupts]  # value = <DMAInterrupts.INTR_ALL: 7>
        INTR_ON_COMPLETE: typing.ClassVar[AxiDMA.DMAInterrupts]  # value = <DMAInterrupts.INTR_ON_COMPLETE: 1>
        INTR_ON_DELAY: typing.ClassVar[AxiDMA.DMAInterrupts]  # value = <DMAInterrupts.INTR_ON_DELAY: 2>
        INTR_ON_ERROR: typing.ClassVar[AxiDMA.DMAInterrupts]  # value = <DMAInterrupts.INTR_ON_ERROR: 4>
        __members__: typing.ClassVar[dict[str, AxiDMA.DMAInterrupts]]  # value = {'INTR_ON_COMPLETE': <DMAInterrupts.INTR_ON_COMPLETE: 1>, 'INTR_ON_DELAY': <DMAInterrupts.INTR_ON_DELAY: 2>, 'INTR_ON_ERROR': <DMAInterrupts.INTR_ON_ERROR: 4>, 'INTR_ALL': <DMAInterrupts.INTR_ALL: 7>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    @typing.overload
    def DisableInterrupts(self, intr: AxiDMA.DMAInterrupts = AxiDMA.DMAInterrupts.INTR_ALL) -> None:
        ...
    @typing.overload
    def DisableInterrupts(self, channel: CLAP.DMAChannel, intr: AxiDMA.DMAInterrupts = AxiDMA.DMAInterrupts.INTR_ALL) -> None:
        ...
    @typing.overload
    def EnableInterrupts(self, eventNoMM2S: int = 0xFFFFFFFF, eventNoS2MM: int = 0xFFFFFFFF, intr: AxiDMA.DMAInterrupts = AxiDMA.DMAInterrupts.INTR_ALL) -> None:
        ...
    @typing.overload
    def EnableInterrupts(self, channel: CLAP.DMAChannel, eventNo: int = 0xFFFFFFFF, intr: AxiDMA.DMAInterrupts = AxiDMA.DMAInterrupts.INTR_ALL) -> None:
        ...
    def GetDataWidth(self, channel: CLAP.DMAChannel) -> int:
        ...
    def GetHasDRE(self, channel: CLAP.DMAChannel) -> bool:
        ...
    def GetMM2SByteLength(self) -> int:
        ...
    def GetMM2SRuntime(self) -> float:
        ...
    def GetMM2SSrcAddr(self) -> int:
        ...
    def GetS2MMByteLength(self) -> int:
        ...
    def GetS2MMDestAddr(self) -> int:
        ...
    @typing.overload
    def GetS2MMRuntime(self) -> float:
        ...
    @typing.overload
    def GetS2MMRuntime(self) -> bool:
        ...
    def OnMM2SFinished(self) -> bool:
        ...
    def OnS2MMFinished(self) -> bool:
        ...
    @typing.overload
    def Reset(self) -> None:
        ...
    @typing.overload
    def Reset(self, channel: CLAP.DMAChannel) -> None:
        ...
    def SetBufferLengthRegWidth(self, width: int) -> None:
        ...
    @typing.overload
    def SetDataWidth(self, width: int, channel: CLAP.DMAChannel = CLAP.DMAChannel.MM2S) -> None:
        ...
    @typing.overload
    def SetDataWidth(self, widths: Tuple[int, int]) -> None:
        ...
    @typing.overload
    def SetDataWidthBits(self, width: int, channel: CLAP.DMAChannel = CLAP.DMAChannel.MM2S) -> None:
        ...
    @typing.overload
    def SetDataWidthBits(self, widths: Tuple[int, int]) -> None:
        ...
    def SetHasDRE(self, dre: bool, channel: CLAP.DMAChannel) -> None:
        ...
    @typing.overload
    def Start(self, srcAddr: int, srcLength: int, dstAddr: int, dstLength: int) -> None:
        ...
    @typing.overload
    def Start(self, srcMem: Memory, dstMem: Memory) -> None:
        ...
    @typing.overload
    def Start(self, mem: Memory) -> None:
        ...
    @typing.overload
    def Start(self, channel: CLAP.DMAChannel, mem: Memory) -> None:
        ...
    @typing.overload
    def Start(self, channel: CLAP.DMAChannel, addr: int, length: int) -> None:
        ...
    @typing.overload
    def StartSG(self, memBDTx: Memory, memBDRx: Memory, memDataIn: Memory, memDataOut: Memory, maxPktByteLen: int, numPkts: int = 1, bdsPerPkt: int = 1) -> None:
        ...
    @typing.overload
    def StartSG(self, channel: CLAP.DMAChannel, memBD: Memory, memData: Memory, maxPktByteLen: int, numPkts: int = 1, bdsPerPkt: int = 1) -> None:
        ...
    @typing.overload
    def Stop(self) -> None:
        ...
    @typing.overload
    def Stop(self, channel: CLAP.DMAChannel) -> None:
        ...
    @typing.overload
    def UseInterruptController(self, axiIntC: AxiInterruptController) -> None:
        ...
    @typing.overload
    def UseInterruptController(self, channel: CLAP.DMAChannel, axiIntC: AxiInterruptController) -> None:
        ...
    @typing.overload
    def WaitForFinish(self, timeoutMS: int = -1) -> bool:
        ...
    @typing.overload
    def WaitForFinish(self, channel: CLAP.DMAChannel, timeoutMS: int = -1) -> bool:
        ...
    def __init__(self, clap: CLAP, ctrlOffset: int, mm2sPresent: bool = True, s2mmPresent: bool = True) -> None:
        ...
class AxiGPIO:
    class Channel:
        """
        Members:
        
          CHANNEL_1
        
          CHANNEL_2
        """
        CHANNEL_1: typing.ClassVar[AxiGPIO.Channel]  # value = <Channel.CHANNEL_1: 0>
        CHANNEL_2: typing.ClassVar[AxiGPIO.Channel]  # value = <Channel.CHANNEL_2: 1>
        __members__: typing.ClassVar[dict[str, AxiGPIO.Channel]]  # value = {'CHANNEL_1': <Channel.CHANNEL_1: 0>, 'CHANNEL_2': <Channel.CHANNEL_2: 1>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class DualChannel:
        """
        Members:
        
          Yes
        
          No
        """
        No: typing.ClassVar[AxiGPIO.DualChannel]  # value = <DualChannel.No: 0>
        Yes: typing.ClassVar[AxiGPIO.DualChannel]  # value = <DualChannel.Yes: 1>
        __members__: typing.ClassVar[dict[str, AxiGPIO.DualChannel]]  # value = {'Yes': <DualChannel.Yes: 1>, 'No': <DualChannel.No: 0>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class GPIOInterrupts:
        """
        Members:
        
          INTR_ON_CH1
        
          INTR_ON_CH2
        
          INTR_ALL
        """
        INTR_ALL: typing.ClassVar[AxiGPIO.GPIOInterrupts]  # value = <GPIOInterrupts.INTR_ALL: 3>
        INTR_ON_CH1: typing.ClassVar[AxiGPIO.GPIOInterrupts]  # value = <GPIOInterrupts.INTR_ON_CH1: 1>
        INTR_ON_CH2: typing.ClassVar[AxiGPIO.GPIOInterrupts]  # value = <GPIOInterrupts.INTR_ON_CH2: 2>
        __members__: typing.ClassVar[dict[str, AxiGPIO.GPIOInterrupts]]  # value = {'INTR_ON_CH1': <GPIOInterrupts.INTR_ON_CH1: 1>, 'INTR_ON_CH2': <GPIOInterrupts.INTR_ON_CH2: 2>, 'INTR_ALL': <GPIOInterrupts.INTR_ALL: 3>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class PortStates:
        """
        Members:
        
          OUTPUT
        
          INPUT
        """
        INPUT: typing.ClassVar[AxiGPIO.PortStates]  # value = <PortStates.INPUT: 1>
        OUTPUT: typing.ClassVar[AxiGPIO.PortStates]  # value = <PortStates.OUTPUT: 0>
        __members__: typing.ClassVar[dict[str, AxiGPIO.PortStates]]  # value = {'OUTPUT': <PortStates.OUTPUT: 0>, 'INPUT': <PortStates.INPUT: 1>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class ResetOnInit:
        """
        Members:
        
          Yes
        
          No
        """
        No: typing.ClassVar[AxiGPIO.ResetOnInit]  # value = <ResetOnInit.No: 0>
        Yes: typing.ClassVar[AxiGPIO.ResetOnInit]  # value = <ResetOnInit.Yes: 1>
        __members__: typing.ClassVar[dict[str, AxiGPIO.ResetOnInit]]  # value = {'Yes': <ResetOnInit.Yes: 1>, 'No': <ResetOnInit.No: 0>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    def EnableInterrupts(self, channel: int, intr: AxiGPIO.GPIOInterrupts = AxiGPIO.GPIOInterrupts.INTR_ALL) -> None:
        ...
    def GetGPIOBit(self, channel: AxiGPIO.Channel, port: int) -> int:
        ...
    def RegisterInterruptCallback(self, callback: Callable[[AxiGPIO.Channel, int, bool], None]) -> None:
        ...
    def Reset(self) -> None:
        ...
    def SetDualChannel(self, dualChannel: bool) -> None:
        ...
    def SetGPIOBit(self, channel: AxiGPIO.Channel, port: int, value: bool) -> None:
        ...
    def SetGPIOState(self, channel: AxiGPIO.Channel, port: int, state: AxiGPIO.PortStates) -> None:
        ...
    def SetGPIOWidth(self, channel: AxiGPIO.Channel, width: int) -> None:
        ...
    def SetGPIOWidths(self, widths: Tuple[int, int]) -> None:
        ...
    def SetTriStateDefaultValue(self, channel: AxiGPIO.Channel, value: int) -> None:
        ...
    def SetTriStateDefaultValues(self, values: Tuple[int, int]) -> None:
        ...
    def Start(self) -> bool:
        ...
    def Stop(self) -> None:
        ...
    def UseInterruptController(self, axiIntC: AxiInterruptController) -> None:
        ...
    @typing.overload
    def __init__(self, clap: CLAP, ctrlOffset: int, dualChannel: AxiGPIO.DualChannel = AxiGPIO.DualChannel.No, resetOnInit: AxiGPIO.ResetOnInit = AxiGPIO.ResetOnInit.Yes) -> None:
        ...
    @typing.overload
    def __init__(self, clap: CLAP, ctrlOffset: int, resetOnInit: AxiGPIO.ResetOnInit = AxiGPIO.ResetOnInit.Yes) -> None:
        ...
class AxiInterruptController:
    def EnableInterrupt(self, interruptNum: int, enable: bool = True) -> None:
        ...
    def Reset(self) -> None:
        ...
    def Start(self, eventNo: int = 0xFFFFFFFF) -> bool:
        ...
    def Stop(self) -> None:
        ...
    def __init__(self, clap: CLAP, ctrlOffset: int) -> None:
        ...
class CLAP:
    class DMAChannel:
        """
        Members:
        
          MM2S
        
          S2MM
        """
        MM2S: typing.ClassVar[CLAP.DMAChannel]  # value = <DMAChannel.MM2S: 0>
        S2MM: typing.ClassVar[CLAP.DMAChannel]  # value = <DMAChannel.S2MM: 1>
        __members__: typing.ClassVar[dict[str, CLAP.DMAChannel]]  # value = {'MM2S': <DMAChannel.MM2S: 0>, 'S2MM': <DMAChannel.S2MM: 1>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class MemoryType:
        """
        Members:
        
          DDR
        
          BRAM
        """
        BRAM: typing.ClassVar[CLAP.MemoryType]  # value = <MemoryType.BRAM: 2>
        DDR: typing.ClassVar[CLAP.MemoryType]  # value = <MemoryType.DDR: 0>
        __members__: typing.ClassVar[dict[str, CLAP.MemoryType]]  # value = {'DDR': <MemoryType.DDR: 0>, 'BRAM': <MemoryType.BRAM: 2>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class Verbosity:
        """
        Members:
        
          VB_DEBUG
        
          VB_VERBOSE
        
          VB_INFO
        
          VB_WARNING
        
          VB_ERROR
        
          VB_NONE
        """
        VB_DEBUG: typing.ClassVar[CLAP.Verbosity]  # value = <Verbosity.VB_DEBUG: 0>
        VB_ERROR: typing.ClassVar[CLAP.Verbosity]  # value = <Verbosity.VB_ERROR: 4>
        VB_INFO: typing.ClassVar[CLAP.Verbosity]  # value = <Verbosity.VB_INFO: 2>
        VB_NONE: typing.ClassVar[CLAP.Verbosity]  # value = <Verbosity.VB_NONE: 255>
        VB_VERBOSE: typing.ClassVar[CLAP.Verbosity]  # value = <Verbosity.VB_VERBOSE: 1>
        VB_WARNING: typing.ClassVar[CLAP.Verbosity]  # value = <Verbosity.VB_WARNING: 3>
        __members__: typing.ClassVar[dict[str, CLAP.Verbosity]]  # value = {'VB_DEBUG': <Verbosity.VB_DEBUG: 0>, 'VB_VERBOSE': <Verbosity.VB_VERBOSE: 1>, 'VB_INFO': <Verbosity.VB_INFO: 2>, 'VB_WARNING': <Verbosity.VB_WARNING: 3>, 'VB_ERROR': <Verbosity.VB_ERROR: 4>, 'VB_NONE': <Verbosity.VB_NONE: 255>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    @staticmethod
    def CreatePCIe(deviceNum: int = 0, channelNum: int = 0, disableWarden: bool = False) -> CLAP:
        ...
    @staticmethod
    def CreatePetaLinux(deviceNum: int = 0, channelNum: int = 0, disableWarden: bool = False) -> CLAP:
        ...
    @staticmethod
    def SetVerbosity(verbosity: CLAP.Verbosity = CLAP.Verbosity.VB_INFO) -> None:
        ...
    @staticmethod
    def SetWatchDogPollSleepTimeMS(timeMS: int = 10) -> None:
        ...
    def AddMemoryRegion(self, type: CLAP.MemoryType, baseAddr: int, size: int) -> None:
        ...
    @typing.overload
    def AllocMemory(self, type: CLAP.MemoryType, elements: int, sizeOfElement: int, memIdx: int = -1) -> Memory:
        ...
    @typing.overload
    def AllocMemory(self, type: CLAP.MemoryType, byteSize: int, memIdx: int = -1) -> Memory:
        ...
    @typing.overload
    def AllocMemoryBRAM(self, elements: int, sizeOfElement: int, memIdx: int = -1) -> Memory:
        ...
    @typing.overload
    def AllocMemoryBRAM(self, byteSize: int, memIdx: int = -1) -> Memory:
        ...
    @typing.overload
    def AllocMemoryDDR(self, elements: int, sizeOfElement: int, memIdx: int = -1) -> Memory:
        ...
    @typing.overload
    def AllocMemoryDDR(self, byteSize: int, memIdx: int = -1) -> Memory:
        ...
    def FreeMemory(self, mem: Memory) -> None:
        ...
    @typing.overload
    def Read16(self, mem: Memory) -> int:
        ...
    @typing.overload
    def Read16(self, addr: int) -> int:
        ...
    @typing.overload
    def Read16s(self, mem: Memory, sizeInByte: int = 0) -> CLAPBuffer16s:
        ...
    @typing.overload
    def Read16s(self, addr: int, sizeInByte: int) -> CLAPBuffer16s:
        ...
    @typing.overload
    def Read16u(self, mem: Memory, sizeInByte: int = 0) -> CLAPBuffer16u:
        ...
    @typing.overload
    def Read16u(self, addr: int, sizeInByte: int) -> CLAPBuffer16u:
        ...
    @typing.overload
    def Read32(self, mem: Memory) -> int:
        ...
    @typing.overload
    def Read32(self, addr: int) -> int:
        ...
    @typing.overload
    def Read32s(self, mem: Memory, sizeInByte: int = 0) -> CLAPBuffer32s:
        ...
    @typing.overload
    def Read32s(self, addr: int, sizeInByte: int) -> CLAPBuffer32s:
        ...
    @typing.overload
    def Read32u(self, mem: Memory, sizeInByte: int = 0) -> CLAPBuffer32u:
        ...
    @typing.overload
    def Read32u(self, addr: int, sizeInByte: int) -> CLAPBuffer32u:
        ...
    @typing.overload
    def Read64(self, mem: Memory) -> int:
        ...
    @typing.overload
    def Read64(self, addr: int) -> int:
        ...
    @typing.overload
    def Read64s(self, mem: Memory, sizeInByte: int = 0) -> CLAPBuffer64s:
        ...
    @typing.overload
    def Read64s(self, addr: int, sizeInByte: int) -> CLAPBuffer64s:
        ...
    @typing.overload
    def Read64u(self, mem: Memory, sizeInByte: int = 0) -> CLAPBuffer64u:
        ...
    @typing.overload
    def Read64u(self, addr: int, sizeInByte: int) -> CLAPBuffer64u:
        ...
    @typing.overload
    def Read8(self, mem: Memory) -> int:
        ...
    @typing.overload
    def Read8(self, addr: int) -> int:
        ...
    @typing.overload
    def Read8s(self, mem: Memory, sizeInByte: int = 0) -> CLAPBuffer8s:
        ...
    @typing.overload
    def Read8s(self, addr: int, sizeInByte: int) -> CLAPBuffer8s:
        ...
    @typing.overload
    def Read8u(self, mem: Memory, sizeInByte: int = 0) -> CLAPBuffer8u:
        ...
    @typing.overload
    def Read8u(self, addr: int, sizeInByte: int) -> CLAPBuffer8u:
        ...
    @typing.overload
    def Write(self, mem: Memory, buffer: CLAPBuffer8u, sizeInByte: int = 0) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer8u) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer8u, sizeInByte: int) -> None:
        ...
    @typing.overload
    def Write(self, mem: Memory, buffer: CLAPBuffer16u, sizeInByte: int = 0) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer16u) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer16u, sizeInByte: int) -> None:
        ...
    @typing.overload
    def Write(self, mem: Memory, buffer: CLAPBuffer32u, sizeInByte: int = 0) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer32u) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer32u, sizeInByte: int) -> None:
        ...
    @typing.overload
    def Write(self, mem: Memory, buffer: CLAPBuffer64u, sizeInByte: int = 0) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer64u) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer64u, sizeInByte: int) -> None:
        ...
    @typing.overload
    def Write(self, mem: Memory, buffer: CLAPBuffer8s, sizeInByte: int = 0) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer8s) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer8s, sizeInByte: int) -> None:
        ...
    @typing.overload
    def Write(self, mem: Memory, buffer: CLAPBuffer16s, sizeInByte: int = 0) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer16s) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer16s, sizeInByte: int) -> None:
        ...
    @typing.overload
    def Write(self, mem: Memory, buffer: CLAPBuffer32s, sizeInByte: int = 0) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer32s) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer32s, sizeInByte: int) -> None:
        ...
    @typing.overload
    def Write(self, mem: Memory, buffer: CLAPBuffer64s, sizeInByte: int = 0) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer64s) -> None:
        ...
    @typing.overload
    def Write(self, addr: int, buffer: CLAPBuffer64s, sizeInByte: int) -> None:
        ...
    @typing.overload
    def Write16(self, mem: Memory, data: int) -> None:
        ...
    @typing.overload
    def Write16(self, addr: int, data: int) -> None:
        ...
    @typing.overload
    def Write32(self, mem: Memory, data: int) -> None:
        ...
    @typing.overload
    def Write32(self, addr: int, data: int) -> None:
        ...
    @typing.overload
    def Write64(self, mem: Memory, data: int) -> None:
        ...
    @typing.overload
    def Write64(self, addr: int, data: int) -> None:
        ...
    @typing.overload
    def Write8(self, mem: Memory, data: int) -> None:
        ...
    @typing.overload
    def Write8(self, addr: int, data: int) -> None:
        ...
class CLAPBuffer16s:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: int) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: CLAPBuffer16s) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> CLAPBuffer16s:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> int:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: CLAPBuffer16s) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: CLAPBuffer16s) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: int) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: CLAPBuffer16s) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: int) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: int) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: CLAPBuffer16s) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: int) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> int:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> int:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: int) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
    def resize(self, arg0: int) -> None:
        ...
    def size(self) -> int:
        ...
    def sort(self) -> None:
        ...
class CLAPBuffer16u:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: int) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: CLAPBuffer16u) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> CLAPBuffer16u:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> int:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: CLAPBuffer16u) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: CLAPBuffer16u) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: int) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: CLAPBuffer16u) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: int) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: int) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: CLAPBuffer16u) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: int) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> int:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> int:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: int) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
    def resize(self, arg0: int) -> None:
        ...
    def size(self) -> int:
        ...
    def sort(self) -> None:
        ...
class CLAPBuffer32s:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: int) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: CLAPBuffer32s) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> CLAPBuffer32s:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> int:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: CLAPBuffer32s) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: CLAPBuffer32s) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: int) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: CLAPBuffer32s) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: int) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: int) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: CLAPBuffer32s) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: int) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> int:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> int:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: int) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
    def resize(self, arg0: int) -> None:
        ...
    def size(self) -> int:
        ...
    def sort(self) -> None:
        ...
class CLAPBuffer32u:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: int) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: CLAPBuffer32u) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> CLAPBuffer32u:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> int:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: CLAPBuffer32u) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: CLAPBuffer32u) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: int) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: CLAPBuffer32u) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: int) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: int) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: CLAPBuffer32u) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: int) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> int:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> int:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: int) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
    def resize(self, arg0: int) -> None:
        ...
    def size(self) -> int:
        ...
    def sort(self) -> None:
        ...
class CLAPBuffer64s:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: int) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: CLAPBuffer64s) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> CLAPBuffer64s:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> int:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: CLAPBuffer64s) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: CLAPBuffer64s) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: int) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: CLAPBuffer64s) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: int) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: int) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: CLAPBuffer64s) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: int) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> int:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> int:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: int) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
    def resize(self, arg0: int) -> None:
        ...
    def size(self) -> int:
        ...
    def sort(self) -> None:
        ...
class CLAPBuffer64u:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: int) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: CLAPBuffer64u) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> CLAPBuffer64u:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> int:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: CLAPBuffer64u) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: CLAPBuffer64u) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: int) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: CLAPBuffer64u) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: int) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: int) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: CLAPBuffer64u) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: int) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> int:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> int:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: int) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
    def resize(self, arg0: int) -> None:
        ...
    def size(self) -> int:
        ...
    def sort(self) -> None:
        ...
class CLAPBuffer8s:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: int) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: CLAPBuffer8s) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> CLAPBuffer8s:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> int:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: CLAPBuffer8s) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: CLAPBuffer8s) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: int) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: CLAPBuffer8s) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: int) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: int) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: CLAPBuffer8s) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: int) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> int:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> int:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: int) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
    def resize(self, arg0: int) -> None:
        ...
    def size(self) -> int:
        ...
    def sort(self) -> None:
        ...
class CLAPBuffer8u:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: int) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: CLAPBuffer8u) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> CLAPBuffer8u:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> int:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: CLAPBuffer8u) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[int]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: CLAPBuffer8u) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: int) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: CLAPBuffer8u) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: int) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: int) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: CLAPBuffer8u) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: int) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> int:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> int:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: int) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
    def resize(self, arg0: int) -> None:
        ...
    def size(self) -> int:
        ...
    def sort(self) -> None:
        ...
class ClapExp(Exception):
    pass
class HLSCore:
    class APInterrupts:
        """
        Members:
        
          AP_INTR_DONE
        
          AP_INTR_READY
        
          AP_INTR_ALL
        """
        AP_INTR_ALL: typing.ClassVar[HLSCore.APInterrupts]  # value = <APInterrupts.AP_INTR_ALL: 3>
        AP_INTR_DONE: typing.ClassVar[HLSCore.APInterrupts]  # value = <APInterrupts.AP_INTR_DONE: 1>
        AP_INTR_READY: typing.ClassVar[HLSCore.APInterrupts]  # value = <APInterrupts.AP_INTR_READY: 2>
        __members__: typing.ClassVar[dict[str, HLSCore.APInterrupts]]  # value = {'AP_INTR_DONE': <APInterrupts.AP_INTR_DONE: 1>, 'AP_INTR_READY': <APInterrupts.AP_INTR_READY: 2>, 'AP_INTR_ALL': <APInterrupts.AP_INTR_ALL: 3>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class AddressType:
        """
        Members:
        
          BIT_32
        
          BIT_64
        """
        BIT_32: typing.ClassVar[HLSCore.AddressType]  # value = <AddressType.BIT_32: 4>
        BIT_64: typing.ClassVar[HLSCore.AddressType]  # value = <AddressType.BIT_64: 8>
        __members__: typing.ClassVar[dict[str, HLSCore.AddressType]]  # value = {'BIT_32': <AddressType.BIT_32: 4>, 'BIT_64': <AddressType.BIT_64: 8>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    def DisableInterrupts(self, intr: HLSCore.APInterrupts = HLSCore.APInterrupts.AP_INTR_ALL) -> None:
        ...
    def EnableInterrupts(self, eventNo: int = 0xFFFFFFFF, intr: HLSCore.APInterrupts = HLSCore.APInterrupts.AP_INTR_ALL) -> None:
        ...
    def GetDataAddr(self, offset: int) -> int:
        ...
    def GetName(self) -> str:
        ...
    def GetRuntime(self) -> float:
        ...
    def IsDone(self) -> bool:
        ...
    def IsIdle(self) -> bool:
        ...
    def PrintApStatus(self) -> None:
        ...
    def RegisterInterruptCallback(self, callback: Callable[[int], None]) -> None:
        ...
    def SetAutoRestart(self, enable: bool = True) -> None:
        ...
    @typing.overload
    def SetDataAddr(self, offset: int, addr: int) -> None:
        ...
    @typing.overload
    def SetDataAddr(self, offset: int, mem: Memory, addrType: HLSCore.AddressType = HLSCore.AddressType.BIT_64) -> None:
        ...
    def Start(self) -> bool:
        ...
    def WaitForFinish(self, timeoutMS: int = -1) -> bool:
        ...
    def __init__(self, clap: CLAP, ctrlOffset: int, name: str) -> None:
        ...
class Memory:
    def GetBaseAddr(self) -> int:
        ...
    def GetSize(self) -> int:
        ...
    def __repr__(self) -> str:
        ...
class MemoryExp(Exception):
    pass
class VDMA:
    class VDMAInterrupts:
        """
        Members:
        
          INTR_ON_COMPLETE
        
          INTR_ON_DELAY
        
          INTR_ON_ERROR
        
          INTR_ALL
        """
        INTR_ALL: typing.ClassVar[VDMA.VDMAInterrupts]  # value = <VDMAInterrupts.INTR_ALL: 7>
        INTR_ON_COMPLETE: typing.ClassVar[VDMA.VDMAInterrupts]  # value = <VDMAInterrupts.INTR_ON_COMPLETE: 1>
        INTR_ON_DELAY: typing.ClassVar[VDMA.VDMAInterrupts]  # value = <VDMAInterrupts.INTR_ON_DELAY: 2>
        INTR_ON_ERROR: typing.ClassVar[VDMA.VDMAInterrupts]  # value = <VDMAInterrupts.INTR_ON_ERROR: 4>
        __members__: typing.ClassVar[dict[str, VDMA.VDMAInterrupts]]  # value = {'INTR_ON_COMPLETE': <VDMAInterrupts.INTR_ON_COMPLETE: 1>, 'INTR_ON_DELAY': <VDMAInterrupts.INTR_ON_DELAY: 2>, 'INTR_ON_ERROR': <VDMAInterrupts.INTR_ON_ERROR: 4>, 'INTR_ALL': <VDMAInterrupts.INTR_ALL: 7>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    @typing.overload
    def DisableInterrupts(self, intr: VDMA.VDMAInterrupts = VDMA.VDMAInterrupts.INTR_ALL) -> None:
        ...
    @typing.overload
    def DisableInterrupts(self, channel: CLAP.DMAChannel, intr: VDMA.VDMAInterrupts = VDMA.VDMAInterrupts.INTR_ALL) -> None:
        ...
    @typing.overload
    def EnableInterrupts(self, eventNoMM2S: int, eventNoS2MM: int, intr: VDMA.VDMAInterrupts = VDMA.VDMAInterrupts.INTR_ALL) -> None:
        ...
    @typing.overload
    def EnableInterrupts(self, channel: CLAP.DMAChannel, eventNo: int, intr: VDMA.VDMAInterrupts = VDMA.VDMAInterrupts.INTR_ALL) -> None:
        ...
    def GetMM2SHSize(self) -> int:
        ...
    def GetMM2SSrcAddr(self) -> int:
        ...
    def GetMM2SVSize(self) -> int:
        ...
    def GetS2MMDestAddr(self) -> int:
        ...
    def GetS2MMHSize(self) -> int:
        ...
    def GetS2MMVSize(self) -> int:
        ...
    @typing.overload
    def Reset(self) -> None:
        ...
    @typing.overload
    def Reset(self, channel: CLAP.DMAChannel) -> None:
        ...
    def SetMM2SStartAddress(self, addr: int) -> None:
        ...
    def SetS2MMStartAddress(self, addr: int) -> None:
        ...
    @typing.overload
    def Start(self, srcAddr: int, srcHSize: int, srcVSize: int, dstAddr: int, dstHSize: int = 0, dstVSize: int = 0) -> None:
        ...
    @typing.overload
    def Start(self, srcMem: Memory, srcHSize: int, srcVSize: int, dstMem: Memory, dstHSize: int = 0, dstVSize: int = 0) -> None:
        ...
    @typing.overload
    def Start(self, channel: CLAP.DMAChannel, mem: Memory, hSize: int, vSize: int) -> None:
        ...
    @typing.overload
    def Start(self, channel: CLAP.DMAChannel, addr: int, hSize: int, vSize: int) -> None:
        ...
    @typing.overload
    def Stop(self) -> None:
        ...
    @typing.overload
    def Stop(self, channel: CLAP.DMAChannel) -> None:
        ...
    def UseInterruptController(self, axiIntC: AxiInterruptController) -> None:
        ...
    def WaitForFinish(self, channel: CLAP.DMAChannel, timeoutMS: int = -1) -> bool:
        ...
    def __init__(self, clap: CLAP, ctrlOffset: int) -> None:
        ...
__version__: str = '0.1.14'

from typing import Type, Union, Callable

CLAPBufferInst = Union[
	CLAPBuffer8s,
	CLAPBuffer16s,
	CLAPBuffer32s,
	CLAPBuffer64s,
	CLAPBuffer8u,
	CLAPBuffer16u,
	CLAPBuffer32u,
	CLAPBuffer64u,
]

CLAPBufferType = Union[
	Type[CLAPBuffer8s],
	Type[CLAPBuffer16s],
	Type[CLAPBuffer32s],
	Type[CLAPBuffer64s],
	Type[CLAPBuffer8u],
	Type[CLAPBuffer16u],
	Type[CLAPBuffer32u],
	Type[CLAPBuffer64u],
]

CLAPCreateType = Union[
	Callable[[], CLAP.CreatePCIe],
	Callable[[], CLAP.CreatePetaLinux],
]
