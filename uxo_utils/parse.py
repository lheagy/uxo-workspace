import h5py
import numpy as np

# H5 functions
def proc_attr(inp):
    """
    HDF5 - Process attributes for the input group and return them in a
    dictionary.
    """
    dic = {}
    for att in inp.attrs.keys():
        if getattr(inp.attrs[att], "dtype", None) is None:
            dic[att] = inp.attrs[att]
        elif inp.attrs[att].dtype.char == 'S':
            dic[att] = [
                x.strip() for x in inp.attrs[att].tostring().decode('ascii').split(',')
            ]
        else:
            dic[att] = (
                inp.attrs[att][0]
                if isinstance(inp.attrs[att],np.ndarray) and
                inp.attrs[att].size==1
                else inp.attrs[att]
            )
    return dic
    pass

def proc_group(inp):
    """
    HDF5 - A recursive function for reading datasets and attributes into a
    dictionary.
    """
    dic = {}
    dic.update(proc_attr(inp))
    for key in inp.keys():
        if isinstance(inp[key], h5py.Group):
            dic.update({key:proc_group(inp[key])})
        else:
            dic[key] = inp[key][()]
        pass
    return dic

