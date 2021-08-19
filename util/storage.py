import gc
import os
import pickle
from typing import List, Dict

import dill
import klepto.archives

from util.config import get_experiment_results_directory, get_preprocessing_directory
from util.models.result import Result


def __pickle_path(file_name: str, directory: str = None) -> str:
    return f"{file_name}.pkl" if not directory else f"{directory}/{file_name}.pkl"


# Stores an object into a pickle file
def store(obj, file_name: str, directory: str = None):
    path = __pickle_path(file_name, directory)
    print(path)
    with open(path, "wb") as output:
        dill.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def store_dict_as_dir(d: Dict[object, object], file_name: str, directory: str = None):
    # store_list(d.items(), file_name, directory)

    print(__pickle_path(file_name, directory))
    k = klepto.archives.dir_archive(directory + '/' + file_name, d, serialized=True)
    del d
    gc.collect()
    k.dump()
    k.clear()


def load_dict(file_name: str, directory: str = None):
    return load_dict_from_dir(__pickle_path((file_name, directory)))


def load_dict_from_dir(path: str):
    """
    IMPORTANT: KEYS MUST BE INTEGERS!
    :param path:
    :return:
    """
    # return dict(load_list_from_path(path))
    r = {}
    for dirpath, dirnames, files in os.walk(path):
        print(f'In directory: {dirpath}')
        for file_name in files:
            # God, I really hope this works. But dirpath should be something like alksdjflkjasfd/K_|G|, so splitting like this should give me the key
            key = int(dirpath.split('K_')[-1])
            r[key] = load_from_path(f'{dirpath}/{file_name}')

    return r


# Stores an list of LARGE objects into a pickle file (to avoid memory issues)
def store_list(l: List[object], file_name: str, directory: str = None):
    path = __pickle_path(file_name, directory)
    print(path)
    with open(path, "wb") as output:
        dill.dump(len(l), output, pickle.HIGHEST_PROTOCOL)
        for value in l:
            dill.dump(value, output, pickle.HIGHEST_PROTOCOL)


def load_list(file_name: str, directory: str = None):
    return load_list_from_path(__pickle_path(file_name, directory))


def load_list_from_path(path: str):
    with open(path, 'rb') as input:
        for _ in range(dill.load(input)):
            yield dill.load(input)


# Loads an object from a pickle file
def load(file_name: str, directory: str = None):
    return load_from_path(__pickle_path(file_name, directory))


def load_from_path(path: str):
    """ Loads a file from the provided path """
    with open(path, "rb") as input:
        obj = dill.load(input)
    return obj

# TODO: Once all the result objects have migrated to the new Result structure, get rid of the store_experiment functions
def store_experiment(project_name: str, file_name: str, obj: any):
    """ Stores an experiment provided only the project name and file """
    store(obj, file_name, get_experiment_results_directory(project_name))

def store_preprocessing(project_name: str, file_name: str, obj: any):
    store_dict_as_dir(obj, file_name, get_preprocessing_directory(project_name))

def load_preprocessing(project_name: str, file_name: str):
    preprocessing_dir: str = get_preprocessing_directory(project_name)
    return load_dict_from_dir(f"{preprocessing_dir}/{file_name}")

def load_experiment(project_name: str, file_name: str):
    results_dir: str = get_experiment_results_directory(project_name)
    return load_from_path(f"{results_dir}/{file_name}.pkl")


def store_results(project_name: str, res: Result):
    """Stores a result from an experiment"""
    store(res, res.generate_file_name(), get_experiment_results_directory(project_name))


def load_results(project_name: str, file_name: str):
    results_dir: str = get_experiment_results_directory(project_name)
    return load_from_path(f"{results_dir}/{file_name}.pkl")
