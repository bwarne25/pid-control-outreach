import time  # Required to timestamp & delay functions
import numpy as np

from pyfirmata import Arduino, util, STRING_DATA

portName = 'COM5'

arduino = Arduino(portName)  
it = util.Iterator(arduino)
it.start()
start_time = time.time()
input_pin = arduino.get_pin('a:0:i') #analog, input to the computer
output_pin = arduino.get_pin('d:6:p') #digital, PWM mode, from the computer
switch_pin = arduino.get_pin('d:9:i') #digital, input to the computer (switch-state)


def get_temperature():
    temperature = calculate_temperature(read_input_pin())
    return temperature

def read_input_pin():
    return read_voltage_fast(input_pin)
def read_voltage(pin):
    """
        Returns the voltage of the pin passed in (between 0 and 5 Volts)
        It takes a number of measurements, then averages them to reduce noise
    """
    outputs = []
    for i in range(2):
        time.sleep(.05)
        outputs.append(pin.read())
    return 5.0 * np.average(outputs)
def read_voltage_fast(pin):
    """
        Returns the voltage of the pin passed in (between 0 and 5 Volts)
        It takes a single of measurement
    """
    return 5.0 * pin.read()
    
def is_switch_on():
    switch_voltage = read_voltage_fast(switch_pin)
    return switch_voltage > 1

def update_duty_cycle(DC): 
    output_pin.write(DC)

def calculate_temperature(signal1):
    """
       Calculates the temperature from an initial reference voltage and a current voltage (each between 0 and 5)
    """

    R_ratio = np.log((2.5/signal1)*((5-signal1)/(5-2.5)))
    T_Kelvin = 1/((0.003354016 + 0.0002569850*R_ratio +
                   2.620131e-06*R_ratio**2 + 6.383091e-08*R_ratio**3))
    return (T_Kelvin)-273.15

time.sleep(2)
update_duty_cycle(0)