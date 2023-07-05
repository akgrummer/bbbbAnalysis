cmake_minimum_required(VERSION 3.1)
project(YamlExample)

add_subdirectory(third-party/yaml-cpp) # This is one way of referencing another
                                       # CMake project

add_executable(
    yaml-example
    main.cpp
)

target_link_libraries(
    yaml-example  
    PRIVATE
    yaml-cpp  # This is the "target" exposed by 
              # yaml-cpp's CMakeLists.txt file
)
