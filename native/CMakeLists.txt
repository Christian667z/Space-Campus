cmake_minimum_required(VERSION 3.16)
project(native_example LANGUAGES CXX)

add_library(native SHARED native.cpp)
set_target_properties(native PROPERTIES PREFIX "" OUTPUT_NAME "native")
