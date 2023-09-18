import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to update CPU and memory charts
def update_charts():
    # Get CPU and memory information
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent

    # Update CPU line chart
    cpu_data.append(cpu_percent)
    cpu_ax.clear()
    cpu_ax.plot(cpu_data, color='b')
    cpu_ax.set_ylim(0, 100)
    cpu_ax.set_title("CPU Usage")

    # Update memory bar chart
    memory_data.append(memory_percent)
    memory_ax.clear()
    memory_ax.bar(['Memory'], [memory_percent], color='g')
    memory_ax.set_ylim(0, 100)
    memory_ax.set_title("Memory Usage")

    # Redraw canvas
    cpu_canvas.draw()
    memory_canvas.draw()

    # Schedule the function to run again after 1000ms (1 second)
    root.after(1000, update_charts)

# Create the main application window
root = tk.Tk()
root.title("System Monitor")

# Create frames for charts
cpu_frame = ttk.Frame(root)
memory_frame = ttk.Frame(root)

# Create CPU line chart
cpu_fig, cpu_ax = plt.subplots()
cpu_canvas = FigureCanvasTkAgg(cpu_fig, master=cpu_frame)
cpu_canvas.get_tk_widget().pack()

# Create memory bar chart
memory_fig, memory_ax = plt.subplots()
memory_canvas = FigureCanvasTkAgg(memory_fig, master=memory_frame)
memory_canvas.get_tk_widget().pack()

# Initialize data lists
cpu_data = []
memory_data = []

# Update CPU and memory charts periodically
update_charts()

# Pack frames
cpu_frame.pack(side="left", padx=10, pady=10)
memory_frame.pack(side="left", padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()
