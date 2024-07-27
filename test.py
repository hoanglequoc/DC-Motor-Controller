import serial
import tkinter as tk
from tkinter import ttk
import threading
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# First Code: Motor Controller on COM5
# Create a Tkinter window for the motor controller
root = tk.Tk()
root.title("Motor Controller")
root.configure(bg="#333")  # Dark mode background

# Create a Tkthemes style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background="#444", foreground="#fff")
style.configure("TScale", background="#444", foreground="#fff")

# Create a serial connection for the motor controller
ser_motor = serial.Serial("COM5", 9600, timeout=1)  # Replace with your serial port

# Create a frame for the motor controls
motor_frame = ttk.Frame(root, padding="10")
motor_frame.pack(fill="x")

# Create a label and entry for the motor speed
speed_label = ttk.Label(motor_frame, text="Speed:")
speed_label.pack(side="left")
speed_entry = ttk.Entry(motor_frame, width=5)
speed_entry.pack(side="left")

# Create a button to set the motor speed
def set_speed():
    speed = int(speed_entry.get())
    ser_motor.write(str(speed).encode())
speed_button = ttk.Button(motor_frame, text="Set Speed", command=set_speed)
speed_button.pack(side="left")

# Create a button to move the motor forward
def move_forward():
    ser_motor.write(b"F")
forward_button = ttk.Button(motor_frame, text="Forward", command=move_forward)
forward_button.pack(side="left")

# Create a button to move the motor backward
def move_backward():
    ser_motor.write(b"B")
backward_button = ttk.Button(motor_frame, text="Backward", command=move_backward)
backward_button.pack(side="left")

# Create a button to stop the motor
def stop_motor():
    ser_motor.write(b"S")
stop_button = ttk.Button(motor_frame, text="Stop", command=stop_motor)
stop_button.pack(side="left")

# Create a scale to control the motor speed
def scale_changed(val):
    ser_motor.write(str(int(val)).encode())
speed_scale = ttk.Scale(root, from_=0, to=9, orient="horizontal", command=scale_changed)
speed_scale.pack(fill="x")

# Second Code: Real-time Plot on COM6
precision = 5

def animate(i, voltage_list, current_list, avg_voltage, avg_current, time_list, ser_plot):
    arduino_string = ser_plot.readline().decode().strip()
    try:
        current_str, voltage_str = arduino_string.split(',')
        voltage = float(voltage_str)
        current = float(current_str)

        voltage_list.append(voltage)
        current_list.append(current)
        time_list.append(len(time_list))

        # Calculate average of voltage_list and current_list
        avg_voltage = sum(voltage_list) / len(voltage_list)
        avg_current = sum(current_list) / len(current_list)

    except ValueError:  # Pass if data point is bad
        pass

    ax1.clear()
    ax2.clear()

    ax1.plot(time_list, voltage_list, 'b-', label='Voltage (V)')
    ax2.plot(time_list, current_list, 'r-', label='Current (A)')

    ax1.set_ylim([4, 7])  # Adjust the limits according to your data range
    ax2.set_ylim([0, 2])  # Adjust the limits according to your data range

    ax1.set_xlabel("Time")

    color = 'tab:blue'
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylabel("Voltage (V)", color=color)
    ax1.set_title('Avg. Voltage: 'f'{avg_voltage:.{precision}f}'' (V)', color=color, loc='left')

    color = 'tab:red'
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.secondary_yaxis('right').set_ylabel("Current (A)", color=color)
    ax2.set_title('Avg. Current: 'f'{avg_current:.{precision}f}'' (A)', color=color, loc='right')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper left', bbox_to_anchor=(0.0, 0.9))  # Position ax2 legend below ax1 legend


def start_plot():
    voltage_list = []
    current_list = []
    time_list = []
    avg_voltage = 0
    avg_current = 0

    global ax1, ax2  # Declare ax1 and ax2 as global to modify them in animate()

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # Instantiate a second y-axis that shares the same x-axis

    ser_plot = serial.Serial("COM6", 9600)  # Establish Serial object with COM port and BAUD rate to match Arduino Port/rate
    time.sleep(2)  # Time delay for Arduino Serial initialization

    ani = animation.FuncAnimation(fig, animate, fargs=(voltage_list, current_list, avg_voltage, avg_current, time_list, ser_plot), interval=100)

    plt.show()  # Keep Matplotlib plot persistent on screen until it is closed
    ser_plot.close()  # Close Serial connection when plot is closed

# Create a thread to run the plot function
plot_thread = threading.Thread(target=start_plot)
plot_thread.start()

# Start the Tkinter main loop
root.mainloop()

# Close the motor serial connection when Tkinter window is closed
ser_motor.close()