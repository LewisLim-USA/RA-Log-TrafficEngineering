echo "Before running this install script, "
echo "please EDIT the runsystem.script and runvideo.script"
echo " and ensure the path to the python files are valid."

# Copy the script files in this folder to /etc/systemd/system
sudo cp *.service /etc/systemd/system/

# After creating or modifying a service file, 
# you need to reload the systemd manager configuration to recognize the new service 
sudo systemctl daemon-reload 


# Enable the new services
sudo systemctl enable runvideo.service
sudo systemctl enable runsystem.service

# Start the new services
sudo systemctl start runvideo.service
sudo systemctl start runsystem.service

# To check if your service is running
# sudo systemctl status runvideo.service
# sudo systemctl status runsystem.service

# To view logs for your service, you can use journalctl:
# sudo journalctl -u runvideo.service -r
# sudo journalctl -u runsystem.service -r