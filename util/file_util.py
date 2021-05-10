import os


# Creates a directory if it doesn't already exists
def create_dir(name: str, agressive: bool = False) -> str:
    number = 0
    directory = f"results/{name}"
    if not agressive:
        if os.path.isdir(directory):
            print(
                f"⚠️  The directory {name} already exists. Creating new directory...")

        while os.path.isdir(directory):
            number += 1
            directory = f"results/{name}({number})"

    if not os.path.isdir(directory):
        os.mkdir(directory)
    return directory