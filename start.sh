sudo docker build -t gpu-monitor .
sudo docker run --rm --gpus all -p 5000:5000 --name gpu_monitor gpu-monitor