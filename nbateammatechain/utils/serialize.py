import pickle

def create_pickle(filename, obj):
    """
    Creates a pickle file to serialize object
    """
    with open(filename, 'wb') as out_file:
        pickle.dump(obj, out_file, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(filename):
    """
    Loads pickle file and returns unserialized object
    """
    with open(filename, 'rb') as in_file:
        return pickle.load(in_file)
