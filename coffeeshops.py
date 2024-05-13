import googlemaps
from datetime import datetime
from polyline import decode
from itertools import chain

def find_points_along_route(api_key, origin, destination, radius = 1000):
    gmaps = googlemaps.Client(key = api_key)
    directions = gmaps.directions(origin, destination, mode="driving", departure_time = datetime.now())
    overview_polyline = directions[0]['overview_polyline']['points']
    route_coordinates = decode(overview_polyline)
    all_points = list(chain.from_iterable(route_coordinates))
    return all_points

def find_closest_coffee_shops(api_key, points, radius=1000):
    gmaps = googlemaps.Client(key = api_key)
    coffee_shops = {}
    for point in points:
        coffee_shops[point] = gmaps.places_nearby(location = point, radius = radius, type = "cafe")
    return coffee_shops
def main():
    api_key = "google_maps_api_key"
    origin = "Current Location"
    destination = "1600 Amphitheatre Parkway"

    points = find_points_along_route(api_key, origin, destination)
    
    coffee_shops = find_closest_coffee_shops(api_key, points)

    for point, shops in coffee_shops.items():
        if shops.get('results'):
            print(f"Coffee shops near {point}:")
            for shop in shops['results']:
                name = shop.get('name', 'N/A')
                address = shop.get('vicinity', 'N/A')
                rating = shop.get('rating', 'N/A')
                user_ratings_total = shop.get('user_ratings_total', 'N/A')
                print(f"- {name}")
                print(f"  Address: {address}")
                print(f"  Rating: {rating} (based on {user_ratings_total} reviews)")
                print()
        else:
            print(f"No coffee shops found near {point}.\n")