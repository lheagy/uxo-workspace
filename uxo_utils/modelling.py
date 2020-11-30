import numpy as np

from .data import load_ordnance_dict
from .imports import (
    sensorCoords2RxCoords, preCalcLoopCorners, FModParam, Model, forwardWithQ
)


def create_profile(
    sensorinfo,
    ymin=0., ymax=3., y_spacing=0.2, z=0.28,
    pitch=0, roll=0, yaw=0,
):
    domain_y = ymax - ymin
    ntx = len(sensorinfo.transmitters)
    dy = y_spacing / ntx
    nloc = int(np.ceil(domain_y/dy))
    ncycles = int(nloc/ntx)

    y = np.linspace(ymin, ymax-dy, nloc)
    x = np.zeros(nloc)
    z = z * np.ones(nloc)

    pitch = pitch*np.ones(nloc)
    roll = roll*np.ones(nloc)
    yaw = yaw*np.ones(nloc)

    txnum = np.kron(np.ones(ncycles), np.arange(ntx))

    # Convert sensor location coordinates to Rx locations
    pos, mnum = sensorCoords2RxCoords(
        sensorinfo=sensorinfo,
        x = x,
        y = y,
        z = z,
        pitch = pitch,
        roll = roll,
        yaw = yaw,
        txnum = txnum
    )

    pitch = np.concatenate([np.tile(x,pos[i].shape[0]) for i,x in enumerate(pitch)])
    roll = np.concatenate([np.tile(x,pos[i].shape[0]) for i,x in enumerate(roll)])
    yaw = np.concatenate([np.tile(x,pos[i].shape[0]) for i,x in enumerate(yaw)])
    pos = np.concatenate(pos,axis=0)

    return pos, mnum, pitch, roll, yaw

def create_forward_modelling_params(
    sensorinfo, times, mnum, pos, pitch, roll, yaw
):
    Tx_indices_rot, Rx_indices_rot = preCalcLoopCorners(
        sensorinfo=sensorinfo, mnum=mnum, rlist=pos,
        pitch=pitch, roll=roll, yaw=yaw
    )

    return FModParam(sensorinfo, pos, mnum, times, Tx_indices_rot, Rx_indices_rot)

def generate_random_variables(n, bounds, log_scaled=False):
    if log_scaled is True:
        if any(bounds == 0):
            return np.zeros(n)
        bounds = np.log(bounds)
        return np.exp(bounds.min() + (bounds.max() - bounds.min()) * np.random.rand(n))
    return bounds.min() + (bounds.max() - bounds.min()) * np.random.rand(n)

def noise_model(times, amplitude=0.1, slope=-1):
    return amplitude * np.exp(slope * np.log(times))

def simulate_object(ordnance_key, st, times, x, y, z, yaw, pitch, roll, polarization_index=0):
    xyz = np.r_[x, y, z]
    ypr = np.r_[yaw, pitch, roll]

    ordnance = load_ordnance_dict()

    # polarizabilities
    pi = int(polarization_index)
    L3 = ordnance[ordnance_key]["L3"][pi]
    L2 = ordnance[ordnance_key]["L2"][pi]
    L1 = ordnance[ordnance_key]["L1"][pi]

    # run simulation
    mod = Model(xyz=xyz, gba=ypr, l3=L3, l2=L2, l1=L1, times=times)
    V = forwardWithQ(mod, st) # nT/s (some version of db/dt)
    V = V.reshape(-1, st.mnum.max()+1, len(times))
    V = np.swapaxes(V, 0, 1)

    return V


