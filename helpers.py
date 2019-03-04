import time
import numpy as np
from threading import Thread

def calculate_temperature(signal1):
    """
       Calculates the temperature from an initial reference voltage and a current voltage (each between 0 and 5)
    """

    R_ratio = np.log((2.5/signal1)*((5-signal1)/(5-2.5)))
    T_Kelvin = 1/((0.003354016 + 0.0002569850*R_ratio +
                   2.620131e-06*R_ratio**2 + 6.383091e-08*R_ratio**3))
    return (T_Kelvin)-273.15

def parse_model_paramaters(popt):
    tau = str(round(popt[0], 2))
    K =str(round(popt[1], 2))
    C = str(round(popt[2], 2))
    theta = str(round(popt[3], 2))
    return (tau, K, C, theta)