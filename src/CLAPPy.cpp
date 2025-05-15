/*
 *  File: CLAPPy.cpp
 *  Copyright (c) 2023 Florian Porrmann
 *
 *  MIT License
 *
 *  Permission is hereby granted, free of charge, to any person obtaining a copy
 *  of this software and associated documentation files (the "Software"), to deal
 *  in the Software without restriction, including without limitation the rights
 *  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 *  copies of the Software, and to permit persons to whom the Software is
 *  furnished to do so, subject to the following conditions:
 *
 *  The above copyright notice and this permission notice shall be included in all
 *  copies or substantial portions of the Software.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 *  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 *  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 *  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 *  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 *  SOFTWARE.
 *
 */

#include <CLAP.hpp>
#include <IP_Cores/AxiDMA.hpp>
#include <IP_Cores/AxiGPIO.hpp>
#include <IP_Cores/AxiInterruptController.hpp>
#include <IP_Cores/HLSCore.hpp>
#include <IP_Cores/VDMA.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include <array>
#include <cstdint>
#include <string>

namespace py = pybind11;

#define STRINGIFY(x)       #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

// TODO: Look into Buffer protocol

// Macro to bind common methods for any vector type
#define BIND_VECTOR_COMMON_METHODS(vec_type)                                                                             \
	.def("size", &vec_type::size)                                                                                        \
		.def("append", [](vec_type &v, typename vec_type::value_type item) { v.push_back(item); })                       \
		.def("clear", &vec_type::clear)                                                                                  \
		.def("extend", [](vec_type &v, const vec_type &other) { v.insert(v.end(), other.begin(), other.end()); })        \
		.def("pop", [](vec_type &v) {                                                                                    \
			if (v.empty())                                                                                               \
				throw std::out_of_range("pop from empty vector");                                                        \
			typename vec_type::value_type item = v.back();                                                               \
			v.pop_back();                                                                                                \
			return item;                                                                                                 \
		})                                                                                                               \
		.def("insert", [](vec_type &v, size_t index, typename vec_type::value_type item) {                               \
			if (index > v.size())                                                                                        \
				throw std::out_of_range("inser index out of range");                                                     \
			v.insert(v.begin() + index, item);                                                                           \
		})                                                                                                               \
		.def("remove", [](vec_type &v, typename vec_type::value_type item) {                                             \
			auto it = std::find(v.begin(), v.end(), item);                                                               \
			if (it != v.end())                                                                                           \
				v.erase(it);                                                                                             \
			else                                                                                                         \
				throw std::invalid_argument("value to remove not found in vector");                                      \
		})                                                                                                               \
		.def("sort", [](vec_type &v) { std::sort(v.begin(), v.end()); })                                                 \
		.def("resize", [](vec_type &v, size_t new_size) { v.resize(new_size); })                                         \
		.def("__contains__", [](const vec_type &v, typename vec_type::value_type item) {                                 \
			return std::find(v.begin(), v.end(), item) != v.end();                                                       \
		})                                                                                                               \
		.def(                                                                                                            \
			"__iter__", [](const vec_type &v) { return py::make_iterator(v.begin(), v.end()); }, py::keep_alive<0, 1>()) \
		.def("__repr__", [](const vec_type &v) {                                                                         \
			std::stringstream ss;                                                                                        \
			ss << "[";                                                                                                   \
			for (size_t i = 0; i < v.size(); ++i)                                                                        \
			{                                                                                                            \
				if (i > 0) ss << ", ";                                                                                   \
				ss << v[i];                                                                                              \
			}                                                                                                            \
			ss << "]";                                                                                                   \
			return ss.str();                                                                                             \
		})                                                                                                               \
		.def("__len__", &vec_type::size)

// Macro to bind the vector type and its common methods
#define BIND_VECTOR(m, vec_type, name) \
	py::bind_vector<vec_type>(m, name) \
		BIND_VECTOR_COMMON_METHODS(vec_type)

template<typename T>
void defRWTemplate(py::class_<clap::CLAP, clap::CLAPPtr> &c, const bool &isSigned = false)
{
	const std::size_t size     = sizeof(T);
	const std::string readName = "Read" + std::to_string(size * 8) + (isSigned ? "s" : "u");

	c.def("Write", py::overload_cast<const clap::Memory &, const clap::CLAPBuffer<T> &, const uint64_t &>(&clap::CLAP::Write<T>), py::arg("mem"), py::arg("buffer"), py::arg("sizeInByte") = clap::USE_MEMORY_SIZE)
		.def("Write", py::overload_cast<const uint64_t &, const clap::CLAPBuffer<T> &>(&clap::CLAP::Write<T>), py::arg("addr"), py::arg("buffer"))
		.def("Write", py::overload_cast<const uint64_t &, const clap::CLAPBuffer<T> &, const uint64_t &>(&clap::CLAP::Write<T>), py::arg("addr"), py::arg("buffer"), py::arg("sizeInByte"))
		.def(readName.c_str(), py::overload_cast<const clap::Memory &, const uint64_t &>(&clap::CLAP::Read<T>), py::arg("mem"), py::arg("sizeInByte") = clap::USE_MEMORY_SIZE)
		.def(readName.c_str(), py::overload_cast<const uint64_t &, const uint64_t &>(&clap::CLAP::Read<T>), py::arg("addr"), py::arg("sizeInByte"));
}

template<typename T>
std::string printWrapper(const T &obj)
{
	std::stringstream ss;
	ss.str("");
	ss << obj;
	return ss.str();
}

PYBIND11_MAKE_OPAQUE(clap::CLAPBuffer<uint8_t>);
PYBIND11_MAKE_OPAQUE(clap::CLAPBuffer<uint16_t>);
PYBIND11_MAKE_OPAQUE(clap::CLAPBuffer<uint32_t>);
PYBIND11_MAKE_OPAQUE(clap::CLAPBuffer<uint64_t>);

PYBIND11_MAKE_OPAQUE(clap::CLAPBuffer<int8_t>);
PYBIND11_MAKE_OPAQUE(clap::CLAPBuffer<int16_t>);
PYBIND11_MAKE_OPAQUE(clap::CLAPBuffer<int32_t>);
PYBIND11_MAKE_OPAQUE(clap::CLAPBuffer<int64_t>);

PYBIND11_MODULE(MODULE_NAME, m)
{
	py::register_exception<clap::CLAPException>(m, "ClapExp");
	py::register_exception<clap::MemoryException>(m, "MemoryExp");

	BIND_VECTOR(m, clap::CLAPBuffer<uint8_t>, "CLAPBuffer8u");
	BIND_VECTOR(m, clap::CLAPBuffer<uint16_t>, "CLAPBuffer16u");
	BIND_VECTOR(m, clap::CLAPBuffer<uint32_t>, "CLAPBuffer32u");
	BIND_VECTOR(m, clap::CLAPBuffer<uint64_t>, "CLAPBuffer64u");

	BIND_VECTOR(m, clap::CLAPBuffer<int8_t>, "CLAPBuffer8s");
	BIND_VECTOR(m, clap::CLAPBuffer<int16_t>, "CLAPBuffer16s");
	BIND_VECTOR(m, clap::CLAPBuffer<int32_t>, "CLAPBuffer32s");
	BIND_VECTOR(m, clap::CLAPBuffer<int64_t>, "CLAPBuffer64s");

	py::class_<clap::Memory>(m, "Memory").def("__repr__", &printWrapper<clap::Memory>);

	py::class_<clap::CLAP, clap::CLAPPtr> clap(m, "CLAP");
	py::class_<clap::HLSCore> hlsCore(m, "HLSCore");
	py::class_<clap::AxiDMA<uint64_t>> axiDMA(m, "AxiDMA");
	py::class_<clap::AxiInterruptController> axiIntc(m, "AxiInterruptController");
	py::class_<clap::VDMA<uint64_t>> vdma(m, "VDMA");
	py::class_<clap::AxiGPIO> axiGPIO(m, "AxiGPIO");

	py::enum_<clap::CLAP::MemoryType>(clap, "MemoryType")
		.value("DDR", clap::CLAP::MemoryType::DDR)
		.value("BRAM", clap::CLAP::MemoryType::BRAM);

	py::enum_<clap::HLSCore::AddressType>(hlsCore, "AddressType")
		.value("BIT_32", clap::HLSCore::AddressType::BIT_32)
		.value("BIT_64", clap::HLSCore::AddressType::BIT_64);

	py::enum_<clap::HLSCore::APInterrupts>(hlsCore, "APInterrupts")
		.value("AP_INTR_DONE", clap::HLSCore::APInterrupts::AP_INTR_DONE)
		.value("AP_INTR_READY", clap::HLSCore::APInterrupts::AP_INTR_READY)
		.value("AP_INTR_ALL", clap::HLSCore::APInterrupts::AP_INTR_ALL);

	py::enum_<clap::AxiDMA<uint64_t>::DMAInterrupts>(hlsCore, "DMAInterrupts")
		.value("INTR_ON_COMPLETE", clap::AxiDMA<uint64_t>::DMAInterrupts::INTR_ON_COMPLETE)
		.value("INTR_ON_DELAY", clap::AxiDMA<uint64_t>::DMAInterrupts::INTR_ON_DELAY)
		.value("INTR_ON_ERROR", clap::AxiDMA<uint64_t>::DMAInterrupts::INTR_ON_ERROR)
		.value("INTR_ALL", clap::AxiDMA<uint64_t>::DMAInterrupts::INTR_ALL);

	py::enum_<clap::VDMA<uint64_t>::VDMAInterrupts>(hlsCore, "VDMAInterrupts")
		.value("INTR_ON_COMPLETE", clap::VDMA<uint64_t>::VDMAInterrupts::VDMA_INTR_ON_FRAME_COUNT)
		.value("INTR_ON_DELAY", clap::VDMA<uint64_t>::VDMAInterrupts::VDMA_INTR_ON_DELAY)
		.value("INTR_ON_ERROR", clap::VDMA<uint64_t>::VDMAInterrupts::VDMA_INTR_ON_ERROR)
		.value("INTR_ALL", clap::VDMA<uint64_t>::VDMAInterrupts::VDMA_INTR_ALL);

	py::enum_<DMAChannel>(clap, "DMAChannel")
		.value("MM2S", DMAChannel::MM2S)
		.value("S2MM", DMAChannel::S2MM);

	py::enum_<clap::AxiGPIO::GPIOInterrupts>(axiGPIO, "GPIOInterrupts")
		.value("INTR_ON_CH1", clap::AxiGPIO::GPIOInterrupts::INTR_ON_CH1)
		.value("INTR_ON_CH2", clap::AxiGPIO::GPIOInterrupts::INTR_ON_CH2)
		.value("INTR_ALL", clap::AxiGPIO::GPIOInterrupts::INTR_ALL);

	py::enum_<clap::AxiGPIO::Channel>(axiGPIO, "Channel")
		.value("CHANNEL_1", clap::AxiGPIO::Channel::CHANNEL_1)
		.value("CHANNEL_2", clap::AxiGPIO::Channel::CHANNEL_2);

	py::enum_<clap::AxiGPIO::PortStates>(axiGPIO, "PortStates")
		.value("OUTPUT", clap::AxiGPIO::PortStates::OUTPUT)
		.value("INPUT", clap::AxiGPIO::PortStates::INPUT);

	py::enum_<clap::logging::Verbosity>(clap, "Verbosity")
		.value("VB_DEBUG", clap::logging::Verbosity::VB_DEBUG)
		.value("VB_VERBOSE", clap::logging::Verbosity::VB_VERBOSE)
		.value("VB_INFO", clap::logging::Verbosity::VB_INFO)
		.value("VB_WARNING", clap::logging::Verbosity::VB_WARNING)
		.value("VB_ERROR", clap::logging::Verbosity::VB_ERROR)
		.value("VB_NONE", clap::logging::Verbosity::VB_NONE);

	py::enum_<clap::AxiGPIO::DualChannel>(axiGPIO, "DualChannel")
		.value("Yes", clap::AxiGPIO::DualChannel::Yes)
		.value("No", clap::AxiGPIO::DualChannel::No);

	py::enum_<clap::AxiGPIO::ResetOnInit>(axiGPIO, "ResetOnInit")
		.value("Yes", clap::AxiGPIO::ResetOnInit::Yes)
		.value("No", clap::AxiGPIO::ResetOnInit::No);

	axiGPIO
		.def(py::init<const clap::CLAPPtr &, const uint64_t &, const clap::AxiGPIO::DualChannel &, const clap::AxiGPIO::ResetOnInit &>(), py::arg("clap"), py::arg("ctrlOffset"),
			 py::arg("dualChannel") = clap::AxiGPIO::DualChannel::No, py::arg("resetOnInit") = clap::AxiGPIO::ResetOnInit::Yes)
		.def(py::init<const clap::CLAPPtr &, const uint64_t &, const clap::AxiGPIO::ResetOnInit &>(), py::arg("clap"), py::arg("ctrlOffset"), py::arg("resetOnInit") = clap::AxiGPIO::ResetOnInit::Yes)
		.def("Reset", &clap::AxiGPIO::Reset)
		.def("SetDualChannel", &clap::AxiGPIO::SetDualChannel, py::arg("dualChannel"))
		.def("SetGPIOWidth", &clap::AxiGPIO::SetGPIOWidth, py::arg("channel"), py::arg("width"))
		.def("SetGPIOWidths", &clap::AxiGPIO::SetGPIOWidths, py::arg("widths"))
		.def("SetTriStateDefaultValue", &clap::AxiGPIO::SetTriStateDefaultValue, py::arg("channel"), py::arg("value"))
		.def("SetTriStateDefaultValues", &clap::AxiGPIO::SetTriStateDefaultValues, py::arg("values"))
		.def("EnableInterrupts", &clap::AxiGPIO::EnableInterrupts, py::arg("channel"), py::arg("intr") = clap::AxiGPIO::GPIOInterrupts::INTR_ALL)
		.def("UseInterruptController", &clap::AxiGPIO::UseInterruptController, py::arg("axiIntC"))
		.def("RegisterInterruptCallback", &clap::AxiGPIO::RegisterInterruptCallback, py::arg("callback"))
		.def("Start", &clap::AxiGPIO::Start)
		.def("Stop", &clap::AxiGPIO::Stop)
		.def("SetGPIOState", &clap::AxiGPIO::SetGPIOState, py::arg("channel"), py::arg("port"), py::arg("state"))
		.def("GetGPIOBit", &clap::AxiGPIO::GetGPIOBit, py::arg("channel"), py::arg("port"))
		.def("SetGPIOBit", &clap::AxiGPIO::SetGPIOBit, py::arg("channel"), py::arg("port"), py::arg("value"));
	vdma
		.def(py::init<const clap::CLAPPtr &, const uint64_t &>(), py::arg("clap"), py::arg("ctrlOffset"))
		.def("Start", py::overload_cast<const uint64_t &, const uint32_t &, const uint32_t &, const uint64_t &, const uint32_t &, const uint32_t &>(&clap::VDMA<uint64_t>::Start), py::arg("srcAddr"), py::arg("srcHSize"), py::arg("srcVSize"), py::arg("dstAddr"), py::arg("dstHSize") = 0, py::arg("dstVSize") = 0)
		.def("Start", py::overload_cast<const clap::Memory &, const uint32_t &, const uint32_t &, const clap::Memory &, const uint32_t &, const uint32_t &>(&clap::VDMA<uint64_t>::Start), py::arg("srcMem"), py::arg("srcHSize"), py::arg("srcVSize"), py::arg("dstMem"), py::arg("dstHSize") = 0, py::arg("dstVSize") = 0)
		.def("Start", py::overload_cast<const DMAChannel &, const clap::Memory &, const uint32_t &, const uint32_t &>(&clap::VDMA<uint64_t>::Start), py::arg("channel"), py::arg("mem"), py::arg("hSize"), py::arg("vSize"))
		.def("Start", py::overload_cast<const DMAChannel &, const uint64_t &, const uint32_t &, const uint32_t &>(&clap::VDMA<uint64_t>::Start), py::arg("channel"), py::arg("addr"), py::arg("hSize"), py::arg("vSize"))
		.def("Stop", py::overload_cast<>(&clap::VDMA<uint64_t>::Stop))
		.def("Stop", py::overload_cast<const DMAChannel &>(&clap::VDMA<uint64_t>::Stop), py::arg("channel"))
		.def("WaitForFinish", &clap::VDMA<uint64_t>::WaitForFinish, py::arg("channel"), py::arg("timeoutMS") = clap::WAIT_INFINITE)
		.def("Reset", py::overload_cast<>(&clap::VDMA<uint64_t>::Reset))
		.def("Reset", py::overload_cast<const DMAChannel &>(&clap::VDMA<uint64_t>::Reset), py::arg("channel"))
		.def("UseInterruptController", &clap::VDMA<uint64_t>::UseInterruptController, py::arg("axiIntC"))
		.def("EnableInterrupts", py::overload_cast<const uint32_t &, const uint32_t &, const clap::VDMA<uint64_t>::VDMAInterrupts &>(&clap::VDMA<uint64_t>::EnableInterrupts), py::arg("eventNoMM2S"), py::arg("eventNoS2MM"), py::arg("intr") = clap::VDMA<uint64_t>::VDMAInterrupts::VDMA_INTR_ALL)
		.def("EnableInterrupts", py::overload_cast<const DMAChannel &, const uint32_t &, const clap::VDMA<uint64_t>::VDMAInterrupts &>(&clap::VDMA<uint64_t>::EnableInterrupts), py::arg("channel"), py::arg("eventNo"), py::arg("intr") = clap::VDMA<uint64_t>::VDMAInterrupts::VDMA_INTR_ALL)
		.def("DisableInterrupts", py::overload_cast<const clap::VDMA<uint64_t>::VDMAInterrupts &>(&clap::VDMA<uint64_t>::DisableInterrupts), py::arg("intr") = clap::VDMA<uint64_t>::VDMAInterrupts::VDMA_INTR_ALL)
		.def("DisableInterrupts", py::overload_cast<const DMAChannel &, const clap::VDMA<uint64_t>::VDMAInterrupts &>(&clap::VDMA<uint64_t>::DisableInterrupts), py::arg("channel"), py::arg("intr") = clap::VDMA<uint64_t>::VDMAInterrupts::VDMA_INTR_ALL)
		.def("GetMM2SSrcAddr", &clap::VDMA<uint64_t>::GetMM2SSrcAddr)
		.def("GetS2MMDestAddr", &clap::VDMA<uint64_t>::GetS2MMDestAddr)
		.def("SetMM2SStartAddress", &clap::VDMA<uint64_t>::SetMM2SStartAddress, py::arg("addr"))
		.def("SetS2MMStartAddress", &clap::VDMA<uint64_t>::SetS2MMStartAddress, py::arg("addr"))
		.def("GetMM2SVSize", &clap::VDMA<uint64_t>::GetMM2SVSize)
		.def("GetS2MMVSize", &clap::VDMA<uint64_t>::GetS2MMVSize)
		.def("GetMM2SHSize", &clap::VDMA<uint64_t>::GetMM2SHSize)
		.def("GetS2MMHSize", &clap::VDMA<uint64_t>::GetS2MMHSize);

	axiIntc
		.def(py::init<const clap::CLAPPtr &, const uint64_t &>(), py::arg("clap"), py::arg("ctrlOffset"))
		.def("Reset", &clap::AxiInterruptController::Reset)
		.def("Start", &clap::AxiInterruptController::Start, py::arg("eventNo") = clap::USE_AUTO_DETECT)
		.def("Stop", &clap::AxiInterruptController::Stop)
		.def("EnableInterrupt", &clap::AxiInterruptController::EnableInterrupt, py::arg("interruptNum"), py::arg("enable") = true);

	axiDMA
		.def(py::init<const clap::CLAPPtr &, const uint64_t &, const bool &, const bool &>(), py::arg("clap"), py::arg("ctrlOffset"), py::arg("mm2sPresent") = true, py::arg("s2mmPresent") = true)
		.def("OnMM2SFinished", &clap::AxiDMA<uint64_t>::OnMM2SFinished)
		.def("OnS2MMFinished", &clap::AxiDMA<uint64_t>::OnS2MMFinished)
		.def("Start", py::overload_cast<const uint64_t &, const uint32_t &, const uint64_t &, const uint32_t &>(&clap::AxiDMA<uint64_t>::Start), py::arg("srcAddr"), py::arg("srcLength"), py::arg("dstAddr"), py::arg("dstLength"))
		.def("Start", py::overload_cast<const clap::Memory &, const clap::Memory &>(&clap::AxiDMA<uint64_t>::Start), py::arg("srcMem"), py::arg("dstMem"))
		.def("Start", py::overload_cast<const clap::Memory &>(&clap::AxiDMA<uint64_t>::Start), py::arg("mem"))
		.def("Start", py::overload_cast<const DMAChannel &, const clap::Memory &>(&clap::AxiDMA<uint64_t>::Start), py::arg("channel"), py::arg("mem"))
		.def("Start", py::overload_cast<const DMAChannel &, const uint64_t &, const uint32_t &>(&clap::AxiDMA<uint64_t>::Start), py::arg("channel"), py::arg("addr"), py::arg("length"))
		.def("Stop", py::overload_cast<>(&clap::AxiDMA<uint64_t>::Stop))
		.def("Stop", py::overload_cast<const DMAChannel &>(&clap::AxiDMA<uint64_t>::Stop), py::arg("channel"))
		.def("WaitForFinish", py::overload_cast<const int32_t &>(&clap::AxiDMA<uint64_t>::WaitForFinish), py::arg("timeoutMS") = clap::WAIT_INFINITE)
		.def("WaitForFinish", py::overload_cast<const DMAChannel &, const int32_t &>(&clap::AxiDMA<uint64_t>::WaitForFinish), py::arg("channel"), py::arg("timeoutMS") = clap::WAIT_INFINITE)
		.def("Reset", py::overload_cast<>(&clap::AxiDMA<uint64_t>::Reset))
		.def("Reset", py::overload_cast<const DMAChannel &>(&clap::AxiDMA<uint64_t>::Reset), py::arg("channel"))
		.def("UseInterruptController", py::overload_cast<clap::AxiInterruptController &>(&clap::AxiDMA<uint64_t>::UseInterruptController), py::arg("axiIntC"))
		.def("UseInterruptController", py::overload_cast<const DMAChannel &, clap::AxiInterruptController &>(&clap::AxiDMA<uint64_t>::UseInterruptController), py::arg("channel"), py::arg("axiIntC"))
		.def("EnableInterrupts", py::overload_cast<const uint32_t &, const uint32_t &, const clap::AxiDMA<uint64_t>::DMAInterrupts &>(&clap::AxiDMA<uint64_t>::EnableInterrupts), py::arg("eventNoMM2S") = clap::USE_AUTO_DETECT, py::arg("eventNoS2MM") = clap::USE_AUTO_DETECT, py::arg("intr") = clap::AxiDMA<uint64_t>::DMAInterrupts::INTR_ALL)
		.def("EnableInterrupts", py::overload_cast<const DMAChannel &, const uint32_t &, const clap::AxiDMA<uint64_t>::DMAInterrupts &>(&clap::AxiDMA<uint64_t>::EnableInterrupts), py::arg("channel"), py::arg("eventNo") = clap::USE_AUTO_DETECT, py::arg("intr") = clap::AxiDMA<uint64_t>::DMAInterrupts::INTR_ALL)
		.def("DisableInterrupts", py::overload_cast<const clap::AxiDMA<uint64_t>::DMAInterrupts &>(&clap::AxiDMA<uint64_t>::DisableInterrupts), py::arg("intr") = clap::AxiDMA<uint64_t>::DMAInterrupts::INTR_ALL)
		.def("DisableInterrupts", py::overload_cast<const DMAChannel &, const clap::AxiDMA<uint64_t>::DMAInterrupts &>(&clap::AxiDMA<uint64_t>::DisableInterrupts), py::arg("channel"), py::arg("intr") = clap::AxiDMA<uint64_t>::DMAInterrupts::INTR_ALL)
		.def("SetBufferLengthRegWidth", &clap::AxiDMA<uint64_t>::SetBufferLengthRegWidth, py::arg("width"))
		.def("SetDataWidth", py::overload_cast<const uint32_t &, const DMAChannel &>(&clap::AxiDMA<uint64_t>::SetDataWidth), py::arg("width"), py::arg("channel") = DMAChannel::MM2S)
		.def("SetDataWidth", py::overload_cast<const std::array<uint32_t, 2> &>(&clap::AxiDMA<uint64_t>::SetDataWidth), py::arg("widths"))
		.def("GetDataWidth", &clap::AxiDMA<uint64_t>::GetDataWidth, py::arg("channel"))
		.def("SetHasDRE", &clap::AxiDMA<uint64_t>::SetHasDRE, py::arg("dre"), py::arg("channel"))
		.def("GetHasDRE", &clap::AxiDMA<uint64_t>::GetHasDRE, py::arg("channel"))
		.def("SetDataWidthBits", py::overload_cast<const uint32_t &, const DMAChannel &>(&clap::AxiDMA<uint64_t>::SetDataWidthBits), py::arg("width"), py::arg("channel") = DMAChannel::MM2S)
		.def("SetDataWidthBits", py::overload_cast<const std::array<uint32_t, 2> &>(&clap::AxiDMA<uint64_t>::SetDataWidthBits), py::arg("widths"))
		.def("GetMM2SSrcAddr", &clap::AxiDMA<uint64_t>::GetMM2SSrcAddr)
		.def("GetS2MMDestAddr", &clap::AxiDMA<uint64_t>::GetS2MMDestAddr)
		.def("GetMM2SByteLength", &clap::AxiDMA<uint64_t>::GetMM2SByteLength)
		.def("GetS2MMByteLength", &clap::AxiDMA<uint64_t>::GetS2MMByteLength)
		.def("GetMM2SRuntime", &clap::AxiDMA<uint64_t>::GetMM2SRuntime)
		.def("GetS2MMRuntime", &clap::AxiDMA<uint64_t>::GetS2MMRuntime)
		.def("GetS2MMRuntime", &clap::AxiDMA<uint64_t>::IsSGEnabled)
		.def("StartSG", py::overload_cast<const clap::Memory &, const clap::Memory &, const clap::Memory &, const clap::Memory &, const uint32_t &, const uint8_t &, const uint32_t &>(&clap::AxiDMA<uint64_t>::StartSG), py::arg("memBDTx"), py::arg("memBDRx"), py::arg("memDataIn"), py::arg("memDataOut"), py::arg("maxPktByteLen"), py::arg("numPkts") = 1, py::arg("bdsPerPkt") = 1)
		.def("StartSG", py::overload_cast<const DMAChannel &, const clap::Memory &, const clap::Memory &, const uint32_t &, const uint8_t &, const uint32_t &>(&clap::AxiDMA<uint64_t>::StartSG), py::arg("channel"), py::arg("memBD"), py::arg("memData"), py::arg("maxPktByteLen"), py::arg("numPkts") = 1, py::arg("bdsPerPkt") = 1);

	hlsCore
		.def(py::init<const clap::CLAPPtr &, const uint64_t &, const std::string &>(), py::arg("clap"), py::arg("ctrlOffset"), py::arg("name"))
		.def("Start", &clap::HLSCore::Start)
		.def("WaitForFinish", &clap::HLSCore::WaitForFinish, py::arg("timeoutMS") = clap::WAIT_INFINITE)
		.def("GetRuntime", &clap::HLSCore::GetRuntime)
		.def("EnableInterrupts", &clap::HLSCore::EnableInterrupts, py::arg("eventNo") = clap::USE_AUTO_DETECT, py::arg("intr") = clap::HLSCore::APInterrupts::AP_INTR_ALL)
		.def("DisableInterrupts", &clap::HLSCore::DisableInterrupts, py::arg("intr") = clap::HLSCore::APInterrupts::AP_INTR_ALL)
		.def("SetDataAddr", &clap::HLSCore::SetDataAddr<uint64_t>, py::arg("offset"), py::arg("addr"))
		.def("SetDataAddr", static_cast<void (clap::HLSCore::*)(const uint64_t &, const clap::Memory &, const clap::HLSCore::AddressType &)>(&clap::HLSCore::SetDataAddr), py::arg("offset"), py::arg("mem"), py::arg("addrType") = clap::HLSCore::AddressType::BIT_64)
		.def("GetDataAddr", &clap::HLSCore::GetDataAddr<uint64_t>, py::arg("offset"))
		.def("GetName", &clap::HLSCore::GetName)
		.def("SetAutoRestart", &clap::HLSCore::SetAutoRestart, py::arg("enable") = true)
		.def("IsDone", &clap::HLSCore::IsDone)
		.def("IsIdle", &clap::HLSCore::IsIdle)
		.def("PrintApStatus", &clap::HLSCore::PrintApStatus)
		.def("RegisterInterruptCallback", &clap::HLSCore::RegisterInterruptCallback, py::arg("callback"));

	clap.def("AddMemoryRegion", py::overload_cast<const clap::CLAP::MemoryType &, const uint64_t &, const uint64_t &>(&clap::CLAP::AddMemoryRegion), py::arg("type"), py::arg("baseAddr"), py::arg("size"))
		.def("AllocMemoryDDR", py::overload_cast<const uint64_t &, const std::size_t &, const int32_t &>(&clap::CLAP::AllocMemoryDDR), py::arg("elements"), py::arg("sizeOfElement"), py::arg("memIdx") = -1)
		.def("AllocMemoryDDR", py::overload_cast<const uint64_t &, const int32_t &>(&clap::CLAP::AllocMemoryDDR), py::arg("byteSize"), py::arg("memIdx") = -1)
		.def("AllocMemoryBRAM", py::overload_cast<const uint64_t &, const std::size_t &, const int32_t &>(&clap::CLAP::AllocMemoryBRAM), py::arg("elements"), py::arg("sizeOfElement"), py::arg("memIdx") = -1)
		.def("AllocMemoryBRAM", py::overload_cast<const uint64_t &, const int32_t &>(&clap::CLAP::AllocMemoryBRAM), py::arg("byteSize"), py::arg("memIdx") = -1)
		.def("FreeMemory", &clap::CLAP::FreeMemory, py::arg("mem"))
		//////////////////////////////////////
		.def("Write8", py::overload_cast<const clap::Memory &, const uint8_t &>(&clap::CLAP::Write8), py::arg("mem"), py::arg("data"))
		.def("Write8", py::overload_cast<const uint64_t &, const uint8_t &>(&clap::CLAP::Write8), py::arg("addr"), py::arg("data"))
		.def("Write16", py::overload_cast<const clap::Memory &, const uint16_t &>(&clap::CLAP::Write16), py::arg("mem"), py::arg("data"))
		.def("Write16", py::overload_cast<const uint64_t &, const uint16_t &>(&clap::CLAP::Write16), py::arg("addr"), py::arg("data"))
		.def("Write32", py::overload_cast<const clap::Memory &, const uint32_t &>(&clap::CLAP::Write32), py::arg("mem"), py::arg("data"))
		.def("Write32", py::overload_cast<const uint64_t &, const uint32_t &>(&clap::CLAP::Write32), py::arg("addr"), py::arg("data"))
		.def("Write64", py::overload_cast<const clap::Memory &, const uint64_t &>(&clap::CLAP::Write64), py::arg("mem"), py::arg("data"))
		.def("Write64", py::overload_cast<const uint64_t &, const uint64_t &>(&clap::CLAP::Write64), py::arg("addr"), py::arg("data"))
		//////////////////////////////////////
		.def("Read8", py::overload_cast<const clap::Memory &>(&clap::CLAP::Read8), py::arg("mem"))
		.def("Read8", py::overload_cast<const uint64_t &>(&clap::CLAP::Read8), py::arg("addr"))
		.def("Read16", py::overload_cast<const clap::Memory &>(&clap::CLAP::Read16), py::arg("mem"))
		.def("Read16", py::overload_cast<const uint64_t &>(&clap::CLAP::Read16), py::arg("addr"))
		.def("Read32", py::overload_cast<const clap::Memory &>(&clap::CLAP::Read32), py::arg("mem"))
		.def("Read32", py::overload_cast<const uint64_t &>(&clap::CLAP::Read32), py::arg("addr"))
		.def("Read64", py::overload_cast<const clap::Memory &>(&clap::CLAP::Read64), py::arg("mem"))
		.def("Read64", py::overload_cast<const uint64_t &>(&clap::CLAP::Read64), py::arg("addr"))
		//////////////////////////////////////
		.def_static("CreatePCIe", &clap::CLAP::Create<clap::backends::PCIeBackend>, py::arg("deviceNum") = 0, py::arg("channelNum") = 0, py::arg("disableWarden") = false)
		.def_static("CreatePetaLinux", &clap::CLAP::Create<clap::backends::PetaLinuxBackend>, py::arg("deviceNum") = 0, py::arg("channelNum") = 0, py::arg("disableWarden") = false);

	clap.def_static("SetVerbosity", &clap::logging::SetVerbosity, py::arg("verbosity") = clap::logging::Verbosity::VB_INFO);
	clap.def_static("SetWatchDogPollSleepTimeMS", &clap::SetWatchDogPollSleepTimeMS, py::arg("timeMS") = 10);

	defRWTemplate<uint8_t>(clap);
	defRWTemplate<uint16_t>(clap);
	defRWTemplate<uint32_t>(clap);
	defRWTemplate<uint64_t>(clap);

	defRWTemplate<int8_t>(clap, true);
	defRWTemplate<int16_t>(clap, true);
	defRWTemplate<int32_t>(clap, true);
	defRWTemplate<int64_t>(clap, true);

#ifdef CLAPPY_VERSION
	m.attr("__version__") = MACRO_STRINGIFY(CLAPPY_VERSION);
#else
	m.attr("__version__") = "dev";
#endif
}
