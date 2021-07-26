import json
import os

def load_project_config(project_name: str) -> dict:
    """ Loads the project config provided the project name """
    f = open(f"{project_name}/config.json")
    data = json.load(f)
    f.close()
    return data


def get_experiment_results_directory(project_name: str) -> str:
    """ Returns the directory in which the experimental reuslts should be put """
    return load_project_config(project_name)["experiment_results_directory"]


def get_pre_processing_directory(project_name: str) -> str:
    """ Returns the directory in which the pre-processing parts are stored """
    return load_project_config(project_name)["pre_processing_directory"]