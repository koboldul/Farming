kill -9 $(pidof python farm) 
echo "Starting the process again"
nohup python farm.py &
