import csv
import webbrowser

# By Steve Teoh (c) 2025-04-16

# Path to your CSV file
csv_file = "C:\\Users\\111537\\OneDrive - Taylor's Education Group\\Desktop\\ESD-USB1\\data\\Mybike2\\A7670SA\\2025-04-16.csv"

# lat / Lon field naming
lats = 'Lat'
lons = 'Lon'

# Loop count
count=0
start=595  # to filter out irrelevant starting points (e.g. from time 9:44:09 am)
steps=100
oaddr="origin="
daddr="destination="

# Read lat/lon from CSV
coordinates = []
with open(csv_file, encoding=None, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if count < start:    #skip until starting point
            count+=1
            continue
        if count >= start + steps:    #take the next steps only (so as not to choke up Google Map Server)
            continue
        if row['Lat']=="N" and row['Lon']=="E":  #remove blank records, i.e. " N" and " E"
            continue        
        lat = row[lats].replace(' N','')         #the record contains N and E for the GPS coordinates. We must truncate it
        lon = row[lons].replace(' E','')
        if count == start:
            oaddr+=f'{lat},{lon}'
        daddr=f'{lat},{lon}'
        coordinates.append(f'{lat}%2C{lon}%7C')
        #print(count)
        count+=1
        
# Construct Google Maps directions URL
if coordinates:
    base_url = "https://www.google.com/maps/dir/?api=1&"+ oaddr + "&destination=" + daddr + "&travelmode=driving&zoom=12&waypoints="
    url = base_url + "".join(coordinates)
    print("Opening Google Maps with the following waypoints:")
    print(url)
    webbrowser.open(url)
else:
    print("No coordinates found.")
