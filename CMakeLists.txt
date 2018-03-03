cmake_minimum_required(VERSION 2.8)

project(jmr)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/joint/buildsystems/cmake/")

find_package(Joint)

set(JOINT_MODULE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

joint_import_directories(${CMAKE_CURRENT_SOURCE_DIR}/interfaces)

add_subdirectory(interfaces)

add_subdirectory(core)
add_subdirectory(joint)
add_subdirectory(test_app)
add_subdirectory(web_client)
