cmake_minimum_required(VERSION 3.1)
project(YamlExample)

find_package(ROOT REQUIRED COMPONENTS RIO Net)
# include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
target_include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include test PRIVATE /uscms/home/agrummer/nobackup/range-v3/include/ )
add_subdirectory(/uscms/home/agrummer/nobackup/yaml-cpp/include/ ) # This is one way of referencing another
                                       # CMake project

add_executable(
    yaml-example
    makeHists.cpp
    HistFileClass.cpp
    YamlFileClass.cpp
    makeHists.h
    HistFileClass.h
    YamlFileClass.h
)

target_link_libraries(
    yaml-example
    PRIVATE
    yaml-cpp  # This is the "target" exposed by
              # yaml-cpp's CMakeLists.txt file
)
