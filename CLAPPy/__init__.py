from .CLAPPy import *

try:
    from .CLAPPy import __version__
except ImportError:
    __version__ = "unknown"

__all__ = ['AxiDMA', 'AxiGPIO', 'AxiInterruptController', 'CLAP', 'CLAPBuffer16s', 'CLAPBuffer16u', 'CLAPBuffer32s', 'CLAPBuffer32u', 'CLAPBuffer64s', 'CLAPBuffer64u', 'CLAPBuffer8s', 'CLAPBuffer8u', 'ClapExp', 'HLSCore', 'Memory', 'MemoryExp', 'VDMA', 'CLAPBufferType']

from typing import Union
CLAPBufferType = Union[
	CLAPBuffer8s,
	CLAPBuffer16s,
	CLAPBuffer32s,
	CLAPBuffer64s,
	CLAPBuffer8u,
	CLAPBuffer16u,
	CLAPBuffer32u,
	CLAPBuffer64u,
]
