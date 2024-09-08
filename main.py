import requests
import csv
import time

# Your Foursquare API key
API_KEY = 'Your_Foursquare_API_key'

# Define the Foursquare API endpoints
SEARCH_URL = 'https://api.foursquare.com/v3/places/search'
DETAILS_URL = 'https://api.foursquare.com/v3/places/'

def fetch_cafe_details(fsq_id):
    headers = {
        'Authorization': API_KEY,
        'Accept': 'application/json'
    }
    response = requests.get(f"{DETAILS_URL}{fsq_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching details for {fsq_id}: {response.status_code}")
        return None

def fetch_cafes(lat, lon, limit=100):
    headers = {
        'Authorization': API_KEY,
        'Accept': 'application/json'
    }
    
    all_results = []
    offset = 0
    page_limit = 50  # Foursquare API typically limits to 50 results per request

    while len(all_results) < limit:
        params = {
            'query': 'cafe',
            'll': f'{lat},{lon}',
            'limit': min(page_limit, limit - len(all_results)),
            'categories': '13032',
            'radius': 5000,
            'offset': offset,
            'fields': 'fsq_id,name,location,categories'
        }
        
        response = requests.get(SEARCH_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            all_results.extend(results)
            
            if len(results) < page_limit:  # No more results available
                break
            
            offset += len(results)
            time.sleep(1)  # Add a delay to avoid hitting rate limits
        else:
            print(f"Error fetching data: {response.status_code}")
            break

    return all_results

def is_open_environment(attributes):
    outdoor_seating = any(attr.get('name') == 'Outdoor Seating' for attr in attributes)
    return 'Yes' if outdoor_seating else 'No'

def save_to_csv(cafes, city):
    with open(f'{city}_cafes.csv', mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Address', 'Categories', 'Open Environment', 'Website', 'Menu'])
        for cafe in cafes:
            name = cafe.get('name', 'N/A')
            location = cafe.get('location', {})
            address = location.get('formatted_address', ['N/A'])
            if isinstance(address, list):
                address = ' '.join(address)
            categories = ', '.join([category['name'] for category in cafe.get('categories', [])])
            
            # Fetch additional details
            details = fetch_cafe_details(cafe['fsq_id'])
            if details:
                open_env = is_open_environment(details.get('attributes', []))
                website = details.get('website', 'N/A')
                menu = details.get('menu', 'N/A')
            else:
                open_env = 'N/A'
                website = 'N/A'
                menu = 'N/A'
            
            writer.writerow([name, address, categories, open_env, website, menu])
        
        time.sleep(1)  # Add delay between detail requests

def main():
    city = "Tabriz"
    lat, lon = 38.0800, 46.2919  # Latitude and longitude for Tabriz
    limit = 150  # Desired number of results
    
    cafes = fetch_cafes(lat, lon, limit)
    
    if cafes:
        save_to_csv(cafes, city)
        print(f"Saved {len(cafes)} cafes to {city}_cafes.csv")
    else:
        print("No cafes found for the given city!")

if __name__ == '__main__':
    main()