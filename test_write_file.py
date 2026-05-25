from functions.write_file import write_file


def test() -> None:
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)
    print("")

    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolar sit amet")
    print(result)
    print("")

    result = write_file("calculator", "/tmp/temp.txt", "This should not be allowed")
    print(result)
    print("")


if __name__ == "__main__":
    test()
