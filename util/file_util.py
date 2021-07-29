import os
from util.config import get_experiment_results_directory

# Creates a directory if it doesn't already exists
def create_dir(path: str, dir_name: str, agressive: bool = False) -> str:
    orig_dir_name: str = dir_name
    total_path = f"{path}/{dir_name}"
    number = 0
    if not agressive:
        if os.path.isdir(total_path):
            print(
                f"⚠️  The directory at {total_path} already exists. Creating new directory...")

        while os.path.isdir(total_path):
            number += 1
            dir_name = f"{orig_dir_name}({number})"
            total_path = f"{path}/{dir_name}"

    if not os.path.isdir(total_path):
        os.mkdir(total_path)
    return dir_name



def create_dir_in_experiment_results_directory(dir_name: str, project_name: str, aggressive: bool = False) -> str:
    return create_dir(get_experiment_results_directory(project_name), dir_name, aggressive)