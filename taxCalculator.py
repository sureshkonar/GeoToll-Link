import csv
import requests
from geopy.distance import geodesic
from shapely.geometry import shape, Point

# Class to manage the geographical zone
class GeoZone:
    def __init__(self, zone_file_path='zone.csv'):
        # Load the zone coordinates from the CSV file
        self.zone = self._load_zone_coordinates(zone_file_path)
    
    # Method to load the zone coordinates from a CSV file
    def _load_zone_coordinates(self, path):
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            # Convert each row to a Polygon object and store in a list
            return [shape(row) for row in reader]
    
    # Method to check if a point is inside the zone
    def isInside(self, point):
        # Check if any polygon in the zone contains the point
        return any(polygon.contains(Point(*point)) for polygon in self.zone)

# Class to calculate the tax
class TaxCalculator:
    def __init__(self, tax_rate=10.0):
        # Initialize tax rate and other properties
        self.tax_rate = tax_rate
        self.distance =   0.0
        self.last_point = None
    
    # Method to update the distance traveled
    def updateDist(self, current_point):
        # Update the distance if there is a last point
        if self.last_point is not None:
            self.distance += geodesic(self.last_point, current_point).kilometers
        # Set the current point as the last point for the next update
        self.last_point = current_point
    
    # Method to calculate the tax based on the distance traveled
    def taxCalc(self):
        # Calculate the tax amount by multiplying distance by tax rate
        return self.distance * self.tax_rate
    
    # Method to send the tax amount to be deducted
    def sendAmount(self, tax_amount):
        # URL for the deduct API endpoint
        url = "http://localhost:8080/api/deduct"
        # Send a POST request with the tax amount
        response = requests.post(url, json={"amount": tax_amount})
        # Handle the response from the API
        if response.status_code ==   200:
            return response.json()["message"]
        else:
            raise Exception(response.json()["error"])

def main():
    geo_zone = GeoZone()
    tax_calculator = TaxCalculator()
    
    while True:
        lat, long = getGPSData()
        point = (lat, long)
        
        if geo_zone.isInside(point):
            tax_calculator.updateDist(point)
        else:
            break
    
    try:
        print(tax_calculator.sendAmount())
    except requests.exceptions.HTTPError as err:
        print("An error occurred while sending tax amount:", str(err))

if __name__ == "__main__":
    main()
