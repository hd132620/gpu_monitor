from datetime import datetime
from flask import Flask, render_template
from pytz import timezone

import pynvml
import psutil


app = Flask(__name__)

# Initialize NVML
pynvml.nvmlInit()

# Function to get GPU information
def get_gpu_info():
    gpu_info = []
    max_memory = 0
    device_count = pynvml.nvmlDeviceGetCount()
    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        gpu_info.append({
            'index': i,
            'utilization': utilization.gpu,
            'memory_used': memory_info.used / (1024**2),    # Convert bytes to MB
            'memory_total': memory_info.total / (1024**2)  # Convert bytes to MB
        })
        max_memory = max(max_memory, memory_info.total / (1024**2))
    return gpu_info, max_memory

# Function to get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Function to get current time
def get_current_time():
    return datetime.now(timezone("Asia/Seoul")).strftime('%Y-%m-%d %H:%M:%S')

# Route to render HTML template with system information
@app.route('/')
def index():
    gpu_info, max_memory = get_gpu_info()
    max_utilization = 100
    cpu_usage = get_cpu_usage()
    current_time = get_current_time()
    return render_template('index.html', gpu_info=gpu_info, max_utilization=max_utilization, max_memory=max_memory, cpu_usage=cpu_usage, current_time=current_time)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
