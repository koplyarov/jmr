set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
set(JOINT_MODULE_OUTPUT_DIRECTORY "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")

################################################################################

include_directories(${JOINT_CPP_INCLUDE_DIRECTORIES})
include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_CURRENT_BINARY_DIR})

if (MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /EHsc")
else()
    add_definitions(-Wall)
    add_definitions(-std=c++11)
endif()

joint_generate_adapters(c++ adapters.hpp ${IDL_FILES})

include_directories(${CMAKE_CURRENT_BINARY_DIR})
add_executable(test_app adapters.hpp main.cpp)
target_link_libraries(test_app ${JOINT_LIBRARIES})
