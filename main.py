To develop an application named "Eco-Route Optimizer," which calculates the most fuel-efficient routes for delivery services, we'll use Python. For this project, we'll leverage the Google Maps API, as it provides detailed route information and estimated traffic conditions. We'll also utilize libraries like `geopy` for geospatial calculations and `requests` for API interactions. Please ensure you have a valid Google Maps API key for accessing their services.

Below is a sample Python program for the Eco-Route Optimizer:

```python
import requests
from geopy.distance import geodesic as GD

# Constants
API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'  # Replace with your Google Maps API key
BASE_URL = 'https://maps.googleapis.com/maps/api/directions/json?'

def get_route_info(start, end):
    """
    Get route information from Google Maps API.
    
    :param start: Starting address or coordinates
    :param end: Ending address or coordinates
    :return: JSON response with route details
    """
    try:
        # Setup parameters
        params = {
            'origin': start,
            'destination': end,
            'key': API_KEY,
            'mode': 'driving',
            'avoid': 'highways',  # Optimize for more eco-friendly routes
            'traffic_model': 'best_guess'
        }
        
        # Send request to Google Maps Directions API
        response = requests.get(BASE_URL, params=params)
        
        # Raise HTTPError for bad responses
        response.raise_for_status()
        
        # Return the JSON response
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching route data: {e}")
        return None

def calculate_optimal_route(start, mid_points, end):
    """
    Calculate the most fuel-efficient route using geospatial and API data.
    
    :param start: Starting address
    :param mid_points: List of waypoints
    :param end: Ending address
    :return: Best route details
    """
    best_route = None
    min_distance = float('inf')
    
    try:
        # Iterate over midpoints to calculate potential routes
        for point in mid_points:
            route_info = get_route_info(start, point)
            if not route_info:
                continue
            
            # Extract route distance
            legs = route_info.get('routes', [])[0].get('legs', [])
            total_distance = sum(leg['distance']['value'] for leg in legs)
            
            # Check if this route is more efficient
            if total_distance < min_distance:
                min_distance = total_distance
                best_route = route_info
        
        # Add final leg from last midpoint to destination
        if best_route:
            final_leg_info = get_route_info(mid_points[-1], end)
            if final_leg_info:
                best_route['routes'][0]['legs'].extend(final_leg_info['routes'][0]['legs'])
        
        return best_route
    except Exception as e:
        print(f"Error in route calculation: {e}")
        return None

def print_route(route):
    """
    Print the details of the given route.
    
    :param route: Route details obtained from Google Maps API
    """
    if not route:
        print("No route information available.")
        return
    
    try:
        legs = route['routes'][0]['legs']
        for leg in legs:
            start_address = leg['start_address']
            end_address = leg['end_address']
            distance = leg['distance']['text']
            duration = leg['duration']['text']
            print(f"Start: {start_address}, End: {end_address}, Distance: {distance}, Duration: {duration}")
    except (KeyError, IndexError) as e:
        print(f"Error accessing route details: {e}")

# Example Usage
start_location = "Times Square, New York, NY"
end_location = "Statue of Liberty, New York, NY"
waypoints = ["Central Park, New York, NY", "Empire State Building, New York, NY"]

optimal_route = calculate_optimal_route(start_location, waypoints, end_location)
print_route(optimal_route)
```

### Key Components

- **API Integration**: We use the Google Maps Directions API to fetch routes, avoiding highways to attempt reducing fuel consumption.
- **Route Calculation**: Calculates the optimal route based on total distance, which can indirectly contribute to fuel savings.
- **Error Handling**: Includes error checks for HTTP responses and key operations like API requests and JSON parsing.
- **Code Comments**: Provides comments to explain functionality, aiding understanding and maintenance.

### Pre-Requisites

1. Install necessary Python packages:
   ```bash
   pip install requests geopy
   ```
2. Replace `'YOUR_GOOGLE_MAPS_API_KEY'` with your actual API key.

This application setup allows for finding the most eco-friendly routes, reducing both carbon footprints and fuel costs effectively by leveraging geographical and traffic data provided by Google Maps.