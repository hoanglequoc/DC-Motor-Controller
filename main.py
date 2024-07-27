
import tkinter as tk
from tkinter import ttk
import serial

# Create the main window
root = tk.Tk()
root.title("Motor Controller")
root.configure(bg="#333")  # Dark mode background

# Create a Tkthemes style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background="#444", foreground="#fff")
style.configure("TScale", background="#444", foreground="#fff")

# Create a serial connection
ser = None

def connect_port():
    global ser
    try:
        ser = serial.Serial(port_var.get(), 9600, timeout=1)
        status_label.config(text="Connected", foreground="green")
    except serial.SerialException as e:
        status_label.config(text=f"Error: {e}", foreground="red")

# Port selection
port_label = ttk.Label(root, text="Select COM Port:")
port_label.pack(fill="x")
port_var = tk.StringVar()
port_entry = ttk.Entry(root, width=10, textvariable=port_var)
port_entry.pack(fill="x")
port_var.set("COM3")  # default port
connect_button = ttk.Button(root, text="Connect", command=connect_port)
connect_button.pack(fill="x")
status_label = ttk.Label(root, text="Not connected", foreground="red")
status_label.pack(fill="x")

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
    try:
        speed = int(speed_entry.get())
        if 0 <= speed <= 9:
            ser.write(bytes([speed]))
        else:
            status_label.config(text="Speed must be 0-9", foreground="red")
    except ValueError:
        status_label.config(text="Invalid speed input", foreground="red")

speed_button = ttk.Button(motor_frame, text="Set Speed", command=set_speed)
speed_button.pack(side="left")

# Create a button to move the motor forward
def move_forward():
    ser.write(b"F")

forward_button = ttk.Button(motor_frame, text="Forward", command=move_forward)
forward_button.pack(side="left")

# Create a button to move the motor backward
def move_backward():
    ser.write(b"B")

backward_button = ttk.Button(motor_frame, text="Backward", command=move_backward)
backward_button.pack(side="left")

# Create a button to stop the motor
def stop_motor():
    ser.write(b"S")

stop_button = ttk.Button(motor_frame, text="Stop", command=stop_motor)
stop_button.pack(side="left")



# Start the Tkinter event loop
root.mainloop()