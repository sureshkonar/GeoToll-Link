import csv
import requests
from geopy.distance import geodesic

# Function to check if a point is inside the zone
def is_inside_zone(point, zone):
    # Convert latitude and longitude to floats
    point = (float(point[0]), float(point[1]))
    # Check if the point is inside the zone
    return any(polygon.contains(point) for polygon in zone)

# Load the zone coordinates from a CSV file
with open('zone.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    # Create a list of tuples containing the latitude and longitude
    # coordinates of the vertices of each polygon in the zone
    zone = [tuple(map(float, row)) for row in reader]

# Initialize variables
last_point = None
distance = 0.0

# Loop to continuously read GPS data
while True:
    # Read the latitude and longitude data from the GPS module
    latitude, longitude = get_gps_data()

    # Check if the point is inside the zone
    if is_inside_zone((latitude, longitude), zone):
        # Calculate the distance between the current point and the last point
        if last_point is not None:
            distance += geodesic(last_point, (latitude, longitude)).km
        # Set the current point as the last point for the next iteration
        last_point = (latitude, longitude)
    else:
        # If the point is outside the zone, stop the distance calculation
        break

# Calculate the tax amount based on the distance traveled
tax_rate = 10.0  # Rs. 10 per kilometer
tax_amount = distance * tax_rate

# Format the tax amount as a JSON object that the deduct API endpoint can accept
tax_data = {"amount": tax_amount}

# Send a POST request to the deduct API endpoint to deduct the tax amount from the account balance
response = requests.post('http://localhost:8080/api/deduct', json=tax_data)

# Check if the transaction was successful and print the response message
if response.status_code == 200:
    print(response.json()["message"])
else:
    print(response.json()["error"])
