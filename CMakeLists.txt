# Check that we aren't building in-source
if(${CMAKE_SOURCE_DIR} STREQUAL ${CMAKE_BINARY_DIR})
    message(FATAL_ERROR
        "We don't allow building in the original (source) directory!"
        "Please, remove the CMakeCache.txt and repeat from a dedicate directory, e.g:\n"
        " rm CMakeCache.txt"
        " mkdir ../python-artoolkit-build"
        " cd ../python-artoolkit-build"
        " cmake ../python-artoolkit   #or whatever it is!"
    )
endif()

project (python-artoolkit)
cmake_minimum_required(VERSION 2.8)

find_package(PythonLibs)
include_directories (${PYTHON_INCLUDE_DIRS})

find_package(Boost 1.45.0 COMPONENTS python)
include_directories (${Boost_INCLUDE_DIRS})


add_library (
    mylibinterface SHARED  
    mylib.cpp
)

target_link_libraries (mylibinterface
    boost_python
    ${PYTHON_LIBRARIES}
    ${Boost_LIBRARIES}
)