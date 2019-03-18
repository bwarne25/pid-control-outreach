import time
import numpy as np

from pyfirmata import Arduino, util, STRING_DATA

arduino = Arduino('COM5')

def reset_arduino(portName):
    global arduino
    global start_time
    global input_pin
    global output_pin
    try:
        arduino.exit()
        arduino = Arduino(portName)
        it = util.Iterator(arduino)
        it.start()
        start_time = time.time()
        input_pin = arduino.get_pin('a:0:i')
        output_pin = arduino.get_pin('d:6:p')
        return True
    except Exception as e:
        print(e)
        return False

reset_arduino('COM5')


def get_temperature():
    try:
        temperature = calculate_temperature(read_input_pin())
        return temperature
    except:
        return 25


def read_input_pin():
    try:
        return read_voltage_fast(input_pin)
    except:
        return 1


def read_voltage_fast(pin):
    """
        Returns the voltage of the pin passed in (between 0 and 5 Volts)
        It takes a single of measurement
    """
    return 5.0 * pin.read()


def update_duty_cycle(DC):
    try:
        output_pin.write(DC)
    except:
        pass


def calculate_temperature(signal1):
    """
       Calculates the temperature from an initial reference voltage and a current voltage (each between 0 and 5)
    """

    R_ratio = np.log((2.5/signal1)*((5-signal1)/(5-2.5)))
    T_Kelvin = 1/((0.003354016 + 0.0002569850*R_ratio +
                   2.620131e-06*R_ratio**2 + 6.383091e-08*R_ratio**3))
    return (T_Kelvin)-273.15


try:
    time.sleep(2)
    update_duty_cycle(0)
except:
    pass
