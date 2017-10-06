cmake_minimum_required(VERSION 3.5)
set(CMAKE_VERBOSE_MAKEFILE ON)

# Set output directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# Include thirdparty libraries header files
include_directories(thirdparty/csv)

# Compile with -std=c++11
add_compile_options(-std=c++11)

# Add sub-project
add_subdirectory(csv2csv)
add_subdirectory(naivebayes)
