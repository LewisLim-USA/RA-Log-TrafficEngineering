🛠️ Raspberry Pi Motorbike Project Log & Questions (Update to Steve)

📂 Directory: /home/user/Desktop/MOTORBIKE/

✅ [NEW/EDITED] mqtt_gps_simplified_latest2.py

Purpose: Main script to publish GPS coordinates via MQTT.

Change: Adjusted NMEA data parsing and MQTT topic format.

Question: Is it okay to hardcode the serial port (/dev/ttyUSB3) or should we add auto-detection?



---

✅ [NEW/EDITED] picamera2_loop.py

Purpose: Captures images or videos using PiCamera2 in a loop.

Change: Added timestamped file saving; reduced resolution for faster processing.

Question: Can I use threading for camera preview + save without freezing other tasks?



---

✅ [NEW/EDITED] plotmap.py

Purpose: Visualizes recorded GPS coordinates on a map (likely Google Maps or folium).

Change: Tested basic webbrowser.open() of a .kml file.

Question: Should we integrate real-time plotting using folium + Flask for remote view?



---

📄 Document from Steve Teoh.kml & Document from Steve Teoh(1).kml

Note: Used as base for plotmap.py test. No modifications made.

Question: Should we stick to .kml or convert to .csv for easier handling?



---

📂 Subdirectory: systemd/

✅ [NEW] install.sh

Purpose: Automates installation of .service files and enables them.

Change: Created to avoid manual copy + enable commands.

Question: Should I add log redirection (e.g. >> logfile.txt) for debugging boot issues?



---

✅ [NEW] runsystem.service

Purpose: Auto-start mqtt_gps_simplified_latest2.py at boot.

Question: Should I include Restart=on-failure or After=network.target?



---

✅ [NEW] runvideo.service

Purpose: Auto-start camera logging via picamera2_loop.py.

Question: Is it okay to use ExecStart=/usr/bin/python3 /home/user/Desktop/MOTORBIKE/picamera2_loop.py directly or do we need a wrapper?
