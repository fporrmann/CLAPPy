cmake_minimum_required(VERSION 3.21)
set(PROJECT_NAME CLAPPy)

if(NOT DEFINED CLAPPY_VERSION)
	if(DEFINED SKBUILD_PROJECT_VERSION)
		# If using skbuild, set the version from the project version
		set(CLAPPY_VERSION ${SKBUILD_PROJECT_VERSION})
	else()
		# If not using skbuild, set a default version
		set(CLAPPY_VERSION 0.0.0)
	endif()
endif()

project(${PROJECT_NAME} LANGUAGES CXX VERSION ${CLAPPY_VERSION})

# Use the new FindPython mode
set(PYBIND11_FINDPYTHON ON)

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

# Some build environments like petalinux cannot properly find the CLAP package
# unless the path is explicitly added to the CMAKE_FIND_ROOT_PATH and CMAKE_MODULE_PATH
list(PREPEND CMAKE_FIND_ROOT_PATH ${clap_SOURCE_DIR}/API)
list(PREPEND CMAKE_MODULE_PATH ${clap_SOURCE_DIR}/API/cmake/modules)
find_package(CLAP PATHS ${clap_SOURCE_DIR}/API/cmake/modules REQUIRED)

include_directories(${CLAP_INCLUDE_DIRS})

add_definitions(-DMODULE_NAME=${PROJECT_NAME})

# If CLAPPY_VERSION is defined add it as a preprocessor definition
if(DEFINED CLAPPY_VERSION)
	add_definitions(-DCLAPPY_VERSION=${CLAPPY_VERSION})
endif()

pybind11_add_module(${PROJECT_NAME} src/CLAPPy.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE ${CLAP_LIBS})

install(TARGETS ${PROJECT_NAME} DESTINATION CLAPPy)
install(DIRECTORY CLAPPy/ DESTINATION CLAPPy)