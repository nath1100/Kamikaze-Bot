try:
    import cPickle as pickle
except ImportError:
    import pickle

def loadPickle(file : str):
    with open(file, 'rb') as f:
        data = pickle.load(f)
    return data

def dumpPickle(data, file : str):
    with open(file, 'wb') as f:
        pickle.dump(data, f)