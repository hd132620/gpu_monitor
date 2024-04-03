sudo docker build -t gpu-monitor .
sudo docker run --gpus all -p 5000:5000 gpu-monitor