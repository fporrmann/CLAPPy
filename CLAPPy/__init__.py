from .CLAPPy import *

try:
    from .CLAPPy import __version__
except ImportError:
    __version__ = "unknown"

__all__ = ['AxiDMA', 'AxiGPIO', 'AxiInterruptController', 'CLAP', 'CLAPBuffer16s', 'CLAPBuffer16u', 'CLAPBuffer32s', 'CLAPBuffer32u', 'CLAPBuffer64s', 'CLAPBuffer64u', 'CLAPBuffer8s', 'CLAPBuffer8u', 'ClapExp', 'HLSCore', 'Memory', 'MemoryExp', 'VDMA', 'CLAPBufferInst', 'CLAPBufferType']

from typing import Type, Union

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