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

# Try to find pybind11 quietly first
find_package(pybind11 QUIET)
if(NOT pybind11_FOUND)
    message (STATUS "Could not find locally installed pybind11. Fetching it via FetchContent ...")
    include(FetchContent)
    FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        GIT_TAG v2.13.6
    )
    FetchContent_MakeAvailable(pybind11)
endif()

# Try to find CLAP quietly first
find_package(CLAP QUIET)
if(NOT CLAP_FOUND)
    message (STATUS "Could not find locally installed CLAP. Fetching it via FetchContent ...")
    include(FetchContent)
    FetchContent_Declare(
        CLAP
        GIT_REPOSITORY https://github.com/mkaiser/CLAP.git
        GIT_TAG cmake_improvements
    )
    FetchContent_MakeAvailable(CLAP)

    # Append path to clap-config.cmake to search path
    list(APPEND CMAKE_PREFIX_PATH "${clap_SOURCE_DIR}/API/cmake/modules")

    find_package(CLAP REQUIRED)
endif()


add_definitions(-DMODULE_NAME=${PROJECT_NAME})

# If CLAPPY_VERSION is defined add it as a preprocessor definition
if(DEFINED CLAPPY_VERSION)
	add_definitions(-DCLAPPY_VERSION=${CLAPPY_VERSION})
endif()

pybind11_add_module(${PROJECT_NAME} src/CLAPPy.cpp)

target_link_libraries(${PROJECT_NAME} PRIVATE CLAP::CLAP)

install(TARGETS ${PROJECT_NAME} DESTINATION CLAPPy)
install(DIRECTORY CLAPPy/ DESTINATION CLAPPy)