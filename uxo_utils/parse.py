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


def parse_data_dict(dic):
    """
    Parse an input dictionary and extract the relevant parameters
    """
    
    output = {}

    xyz_dict = dic["XYZ"]
    xyz_data = xyz_dict["Data"]

    output["times"] = np.array(dic['SensorTimes'].flatten())

    def get_index(key):
        return xyz_dict["Info"][key]["ChannelIndex"].flatten().astype(int)-1

    output["easting"] = xyz_data[get_index("Easting"), :]
    output["northing"] = xyz_data[get_index("Northing"), :]
    output["yaw"] = xyz_data[get_index("Yaw"), :]
    output["pitch"] = xyz_data[get_index("Pitch"), :]
    output["roll"] = xyz_data[get_index("Roll"), :]
    output["mn"] = xyz_data[get_index("MeasNum"), :].astype(int) - 1 # index from zero in python
    output["line"] = xyz_data[get_index("Line"), :]
    output["rx_num"] = xyz_data[get_index("RxNum"), :].astype(int) - 1
    output["tx_num"] = xyz_data[get_index("TxNum"), :].astype(int) - 1
    output["rx_comp"] = xyz_data[get_index("RxCNum"), :].astype(int) - 1
    output["data"] = xyz_data[get_index("Data"), :].T
    
    return output