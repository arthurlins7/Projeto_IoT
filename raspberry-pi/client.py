import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import pandas as pd

# Store time-series data
data = pd.DataFrame(columns=["timestamp", "light"])

# Setup GUI
root = tk.Tk()
root.title("ESP8266 Light Sensor Dashboard")

# Live value label
label_var = tk.StringVar()
label_var.set("Waiting for data...")
label = ttk.Label(root, textvariable=label_var, font=("Helvetica", 16))
label.pack(pady=10)

# Setup plot with seaborn
sns.set(style="darkgrid")
fig, ax = plt.subplots(figsize=(6, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(padx=10, pady=10)

# Update the seaborn plot
def update_plot():
    if not data.empty:
        ax.clear()
        sns.lineplot(data=data, x="timestamp", y="light", ax=ax, marker="o", color="red")
        ax.set_title("Light Intensity Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Intensity")
        ax.tick_params(axis='x', rotation=45)
        canvas.draw()

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe("sensor/light")

def on_message(client, userdata, msg):
    value = msg.payload.decode()
    try:
        light = int(value)
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Append to DataFrame
        global data
        data = pd.concat([data, pd.DataFrame([{"timestamp": timestamp, "light": light}])], ignore_index=True)
        if len(data) > 20:  # Limit to last 20 values
            data = data.tail(20)

        label_var.set(f"Light Intensity: {light}")
        update_plot()
    except ValueError:
        print(f"Invalid data received: {value}")

# MQTT setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

# Periodic MQTT loop call
def mqtt_loop():
    client.loop(timeout=1.0)
    root.after(500, mqtt_loop)

root.after(500, mqtt_loop)
root.mainloop()
