if (MSVC)
    message("USING MSVC")
    # warning level 4
    add_compile_options(/W1 /O2)
endif()

if (${CMAKE_CXX_COMPILER_ID} STREQUAL "Clang")
    message("USING CLANG")
endif()