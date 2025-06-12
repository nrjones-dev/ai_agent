import unittest

from functions.get_files_info import get_files_info


class TestDirectory(unittest.TestCase):
    def test_1(self):
        result = get_files_info("calculator", ".")
        print(result)

    def test_2(self):
        result = get_files_info("calculator", "pkg")
        print(result)

    def test_3(self):
        result = get_files_info("calculator", "/bin")
        print(result)

    def test_4(self):
        result = get_files_info("calculator", "../")
        print(result)


if __name__ == "__main__":
    unittest.main()
