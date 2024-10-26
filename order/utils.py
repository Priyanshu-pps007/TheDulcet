import requests

def get_coordinates_opencage(address):
    api_key = "59a3afc0eeb4434a8a6574f5ced5de4c"  # Replace this with your OpenCage API key
    base_url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": address,
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    # If the request was successful and results are found
    if data['results']:
        lat_lng = data['results'][0]['geometry']
        return lat_lng['lat'], lat_lng['lng']
    else:
        return None, None

def calculate_distance(lat1, lng1, lat2, lng2):
    import math
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance


# import requests

# def get_coordinates_opencage(address):
#     api_key = "59a3afc0eeb4434a8a6574f5ced5de4c"
#     base_url = "https://api.opencagedata.com/geocode/v1/json"
#     params = {
#         "q": address,
#         "key": api_key
#     }
#     response = requests.get(base_url, params=params)
#     data = response.json()

#     print(data)
    
#     if data['results']:
#         lat_lng = data['results'][0]['geometry']
#         return lat_lng['lat'], lat_lng['lng']
#     else:
#         return None, None
    



# # Example usage:
# address = "Daud Naar, Mewa Lal Bagiya, 11/7, next to Bank of India, Naini, Prayagraj, Chak Mohiuddin, Uttar Pradesh 211008, India"
# lat, lng = get_coordinates_opencage(address)

# if lat and lng:
#     print(f"Restaurant Latitude: {lat}, Longitude: {lng}")
# else:
#     print("Could not get coordinates for the provided address.")
