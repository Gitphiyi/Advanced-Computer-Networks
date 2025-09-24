cmake_minimum_required(VERSION 3.24)
project(HTTP)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

option(ENABLE_ASAN "Enable AddressSanitizer" ON)

add_library(lib STATIC 
    server.cpp
    client.cpp
)

target_include_directories(lib PUBLIC ${PROJECT_SOURCE_DIR})
add_executable(main main.cpp)
target_link_libraries(main PRIVATE lib)
