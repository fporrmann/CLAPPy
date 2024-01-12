cmake_minimum_required(VERSION 3.24)
set(PROJECT_NAME CLAPPy)
project(${PROJECT_NAME} LANGUAGES CXX)

include(FetchContent)
FetchContent_Declare(
	pybind11
	GIT_REPOSITORY https://github.com/pybind/pybind11.git
	GIT_TAG 0630807c3070287c716f6be3eacb00b8816b4215 # v2.11.1
)

FetchContent_MakeAvailable(pybind11)

FetchContent_Declare(
	CLAP
	GIT_REPOSITORY https://github.com/fporrmann/CLAP.git
)

FetchContent_MakeAvailable(CLAP)

find_package(CLAP PATHS ${clap_SOURCE_DIR}/API/cmake/modules REQUIRED)

include_directories(${CLAP_INCLUDE_DIRS})

add_definitions(-DMODULE_NAME=${PROJECT_NAME})
add_definitions(-DCLAP_VERSION=${CLAP_VERSION})

pybind11_add_module(${PROJECT_NAME} src/CLAPPy.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE ${CLAP_LIBS})