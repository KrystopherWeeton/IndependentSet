import json
import os

def load_project_config(project_name: str) -> dict:
    """ Loads the project config provided the project name """
    path: str = f"{project_name}/config.json"
    return json.load(path)


def get_experiment_results_directory(project_name: str) -> str:
    """ Returns the directory in which the experimental reuslts should be put"""
    return load_project_config(project_name)["experiment_results_directory"]