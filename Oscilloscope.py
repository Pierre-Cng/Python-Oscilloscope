import tkinter as tk
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from queue import Queue
from threading import Thread
from matplotlib.figure import Figure
import os

class Oscilloscope:
    def __init__(self, root):
        self.data = []
        self.root = root
        self.set_subplot()
        self.set_canvas()
        self.running = False
        self.data_queue = Queue()

    def set_subplot(self):
        self.figure = Figure((8, self.root.winfo_screenheight()//150))
        self.figure.set_facecolor('black')
        self.ax = self.figure.add_subplot()
        self.ax.set_facecolor('black')  # Set plot background to black
        self.ax.tick_params(axis='x', colors='white')  # Set x-axis ticks to white color
        self.ax.tick_params(axis='y', colors='white')  # Set y-axis ticks to white color
        self.ax.spines['bottom'].set_color('white')  # Set x-axis color to white
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')  # Set y-axis color to white
        self.ax.spines['right'].set_color('white')

    def set_canvas(self):
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.root.grid_columnconfigure(1, weight=1)
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
    def switch_oscilloscope(self):
        self.running = not self.running
        if self.running:
            self.acquisition_thread = Thread(target=self.acquire_data)
            self.acquisition_thread.daemon = True
            self.acquisition_thread.start()
            self.update_plot()

    def acquire_data(self):
        # Start the subprocess running the Python script
        self.proc = subprocess.Popen(
            ["python", f'{os.path.join(os.getcwd(), 'read_csv3.py')}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,  # Set this to True if 'python' is not in your PATH variable
            universal_newlines=True  # For text mode
        )
        for line in iter(self.proc.stdout.readline, ''):
            line = line.strip()
            x, y = line.split(',')
            self.data.append((float(x), float(y)))
        self.proc.stdout.close()

    def update_plot(self):
        if self.running:
            self.ax.clear()
            if self.data:
                x, y = zip(*self.data[-10:-1])
                self.ax.plot(x, y, 'orange')
                self.data = self.data[:-10]
            self.ax.set_xlabel('Time', color='white')
            self.ax.set_ylabel('Amplitude', color='white')
            self.ax.set_title('Oscilloscope', color='white')
            self.canvas.draw()
            self.root.after(100, self.update_plot)

def main():
    root = tk.Tk()
    oscilloscope_app = Oscilloscope(root)
    oscilloscope_app.switch_oscilloscope()
    root.mainloop()

if __name__ == "__main__":
    main()
