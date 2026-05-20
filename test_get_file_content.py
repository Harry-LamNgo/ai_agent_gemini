from functions.get_file_content import get_file_content


def test() -> None:

    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")
    print("")

    result = get_file_content("calculator", "main.py")
    print(result)
    # print(f"main.py length: {len(result)}")
    # print(f"main.py truncated: {'truncated' in result}")
    print("")

    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)
    # print(f"pkg/calculator.py length: {len(result)}")
    # print(f"pkg/calculator.py truncated: {'truncated' in result}")
    print("")

    # This case suppose failed -- Error: Cannot read "/bin/cat" as it is outside the permitted working directory
    result = get_file_content("calculator", "/bin/cat")
    print(result)
    print("")

    # This case suppose failed -- Error: File not found or is not a regular file
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result)
    print("")

if __name__ == "__main__":
    test()

