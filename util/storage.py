import dill
import pickle
import os
from util.config import get_experiment_results_directory


def __pickle_path(file_name: str, directory: str = None) -> str:
    return f"{file_name}.pkl" if not directory else f"{directory}/{file_name}.pkl"


# Stores an object into a pickle file
def store(obj, file_name: str, directory: str = None):
    path = __pickle_path(file_name, directory)
    print(path)
    with open(path, "wb") as output:
        dill.dump(obj, output, pickle.HIGHEST_PROTOCOL)


# Loads an object from a pickle file
def load(file_name: str, directory: str = None):
    return load_from_path(__pickle_path(file_name, directory))


def load_from_path(path: str):
    """ Loads a file from the provided path """
    with open(path, "rb") as input:
        obj = dill.load(input)
    return obj


def store_experiment(project_name: str, file_name: str, obj: any):
    """ Stores an experiment provided only the project name and file """
    store(obj, file_name, get_experiment_results_directory(project_name))