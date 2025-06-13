import unittest

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file


class TestRunPython(unittest.TestCase):
    def run_python_file_main(self):
        print(run_python_file("calculator", "main.py"))

    def run_python_file_tests(self):
        print(run_python_file("calculator", "tests.py"))

    def test_run_python_file_outside_dir(self):
        print(run_python_file("calculator", "../main.py"))

    def test_run_python_file_nonexistent(self):
        print(run_python_file("calculator", "nonexistent.py"))


class TestWriteFile(unittest.TestCase):
    def test_write_file(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)

    def test_write_file_subdir(self):
        result = write_file(
            "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
        )
        print(result)

    def test_write_file_wrong_dir(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result)


class TestGetFilesInfo(unittest.TestCase):
    def test_files_info_current_directory(self):
        result = get_files_info("calculator", ".")
        print(result)

    def test_files_info_pkg_directory(self):
        result = get_files_info("calculator", "pkg")
        print(result)

    def test_files_info_invalid_directory(self):
        result = get_files_info("calculator", "/bin")
        print(result)

    def test_files_info_parent_directory(self):
        result = get_files_info("calculator", "../")
        print(result)


class TestFileContent(unittest.TestCase):
    def test_get_file_content_main(self):
        result = get_file_content("calculator", "main.py")
        print(result)

    def test_get_file_content_subdir(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        print(result)

    def test_get_file_content_exterior_dir(self):
        result = get_file_content("calculator", "/bin/cat")
        print(result)


if __name__ == "__main__":
    unittest.main()
