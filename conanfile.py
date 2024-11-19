from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake
from conan.tools.files import copy
from os import path

class VulkanEngineRecipe(ConanFile):
    name    = "bpw-vulkan-engine"
    version = "0.1.0"

    # Optional metadata
    license     = "GNU-3.0"
    author      = "Borja Pozo Wals", "borja.pozo@gmail.com"
    url         = "https://github.com/Boruha/VulkanEngine.git"
    description = "Engine to open windows and draw stuff with Vulkan."
    topics      = "Graphics", "Vulkan"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options  = {
        "shared"         : [True, False],
        "fPIC"           : [True, False],
        "unit_test"      : [True, False],
        "benchmark_test" : [True, False]
    }
    default_options = {
        "shared"         : False, 
        "fPIC"           : True,
        "unit_test"      : False,
        "benchmark_test" : False
    }
    generators = "CMakeDeps"

    def requirements(self):
        self.requires("glfw/3.4")
        self.requires("glm/1.0.1")

        if self.options.get_safe("unit_test"):
            self.requires("gtest/1.15.0")
        if self.options.get_safe("benchmark_test"):
            self.requires("benchmark/1.9.0")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        self.folders.generators = path.join("build", self.settings.get_safe("os"), "generator")
        self.folders.build = path.join("build", self.settings.get_safe("os"), 
                                                self.settings.get_safe("arch"), 
                                                self.settings.get_safe("build_type"))

    def generate(self):
        compiler_name = self.settings.get_safe("compiler")
        compiler_c    = { "msvc": "cl", "clang": "clang" }
        compiler_cxx  = { "msvc": "cl", "clang": "clang++" }

        tc = CMakeToolchain(self)
        if compiler_name in compiler_c:
            tc.variables["CMAKE_C_COMPILER"] = compiler_c[compiler_name] 
        if compiler_name in compiler_cxx:
            tc.variables["CMAKE_CXX_COMPILER"] = compiler_cxx[compiler_name]

        tc.variables["BPW_UNIT_TEST"]      = self.options.get_safe("unit_test")
        tc.variables["BPW_BENCHMARK_TEST"] = self.options.get_safe("benchmark_test")
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package_info(self):
        self.cpp_info.libs = self.name
        self.cpp_info.includedirs = ['include']

        self.cpp_info.set_property("cmake_find_mode", "both")

    def package(self):
        copy(self, "*.hpp", path.join(self.source_folder, "include"), path.join(self.package_folder, "include"))

        copy(self, "conanfile.py", self.source_folder, self.package_folder)
        copy(self, "CMakeLists.txt", self.source_folder, self.package_folder)
        copy(self, "compiler_options.cmake", self.source_folder, self.package_folder)

    
