from conans import ConanFile, CMake, tools
import os


class sqlpp11Conan(ConanFile):
    name = "sqlpp11-connector-sqlite3"
    version = "0.29"
    description = "A C++ wrapper for sqlite3 meant to be used in combination with sqlpp11."
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/bincrafters/conan-sqlpp11-connector-sqlite3"
    homepage = "https://github.com/rbock/sqlpp11-connector-sqlite3"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "BSD 2-Clause"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    requires = "sqlpp11/0.57@bincrafters/stable", "sqlite3/3.25.3@bincrafters/stable"
    short_paths = True

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version),
                  sha256="2904ddd578adb0e122a70f73a80bae4843434d685b7a23ae3ab43471c35efc4f")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_TESTS"] = False
        cmake.definitions['HinnantDate_ROOT_DIR'] = self.deps_cpp_info['date'].include_paths[0]
        cmake.definitions['SQLPP11_INCLUDE_DIR'] = self.deps_cpp_info['sqlpp11'].include_paths[0]
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["sqlpp11-connector-sqlite3"]
