import pickle


def __pickle_path(file_name: str, directory: str = None) -> str:
    return f"{file_name}.pkl" if not directory else f"{directory}/{file_name}.pkl"


# Stores an object into a pickle file
def store(obj, file_name: str, directory: str = None):
    with open(__pickle_path(file_name, directory), "wb") as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


# Loads an object from a pickle file
def load(file_name: str, directory: str = None):
    return load_from_path(__pickle_path(file_name, directory))


def load_from_path(path: str):
    """ Loads a file from the provided path """
    with open(path, "rb") as input:
        obj = pickle.load(input)
    return obj