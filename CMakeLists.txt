cmake_minimum_required(VERSION 3.15)

set(TARGET_NAME bpw-vulkan-engine)
project(${TARGET_NAME})

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR})
include(compiler_options)

set(VULKAN_PATH "D:/Programacion/VulkanSDK/1.3.296.0")
set(ENV{VULKAN_SDK} ${VULKAN_PATH}) # Black Magic (?)

find_package(glfw3 REQUIRED)
find_package(glm REQUIRED)
find_package(Vulkan REQUIRED)

set(INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)
file(GLOB HPP_FILES ${INCLUDE_DIR}/*.hpp)
file(GLOB CPP_FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

add_executable(${TARGET_NAME})

target_sources(${TARGET_NAME}
    PUBLIC
        ${CPP_FILES})

target_link_libraries(${TARGET_NAME}
    PUBLIC
        glfw
        glm::glm
        Vulkan::Vulkan)