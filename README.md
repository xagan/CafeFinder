---

# Café Finder: Fetch Cafés in a Given City using Foursquare API

This Python script allows users to fetch café data from the **Foursquare API** based on latitude and longitude coordinates. The script gathers basic café information such as the name, address, categories, and additional details such as open environment seating, website, and menu availability.

The resulting café data is saved into a CSV file, making it easy to review and share. This is particularly useful for planning outings, dates, or just finding new spots to explore.

## Features:
- Fetches cafés in a specified city or region using latitude and longitude.
- Fetches details like **name, address, categories**, whether the café has **outdoor seating**, and its **website** or **menu** (if available).
- Automatically handles paginated results from Foursquare API.
- Saves the data in a clean, UTF-8 CSV file with fields that are useful for users looking to pick a spot based on specific criteria.

## Requirements

- Python 3.x
- `requests` library
- A **Foursquare API Key** (Get it [here](https://foursquare.com/developers/apps))

### Install dependencies
```bash
pip install requests
```

## Usage

1. Clone this repository:

```bash
git clone https://github.com/your-username/cafe-finder.git
cd cafe-finder
```

2. Replace the `API_KEY` variable with your own Foursquare API Key:

```python
API_KEY = 'YOUR_FOURSQUARE_API_KEY'
```

3. Run the script:

```bash
python cafe_finder.py
```

4. The script will generate a CSV file named after the specified city (e.g., `Tabriz_cafes.csv`).

### CSV Output

The CSV file will contain the following fields:
- **Name**: The name of the café.
- **Address**: The café’s formatted address.
- **Categories**: A list of categories the café belongs to.
- **Open Environment**: Indicates whether the café has outdoor seating.
- **Website**: The café’s website (if available).
- **Menu**: The café’s online menu (if available).

## Code Overview

### Main Functions:

- `fetch_cafes(lat, lon, limit=100)`: This function queries the Foursquare API for cafés near the provided latitude and longitude. The limit controls how many results you retrieve (default is 100).
  
- `fetch_cafe_details(fsq_id)`: Fetches detailed information (e.g., outdoor seating, menu, website) for a café using its unique `fsq_id`.
  
- `save_to_csv(cafes, city)`: Saves the collected café data into a CSV file, ensuring the text is correctly encoded for non-English characters (e.g., Persian).

- `is_open_environment(attributes)`: Determines if the café has outdoor seating by scanning its attributes.

### Notes:

- **Rate Limits**: The script includes time delays between API requests to avoid hitting the Foursquare API rate limit.
- **Adjusting Search Radius**: The search radius is set to 5 km by default. You can adjust this value in the `fetch_cafes` function based on your needs.
  
## Contributing

Feel free to open an issue or create a pull request if you want to improve this script. Contributions are always welcome!

---

### Hints:
- **Pagination Handling**: The script manages pagination by fetching cafés in chunks (50 at a time) and aggregating results until the desired limit is reached.
- **Delay in Detail Fetching**: To prevent hitting the rate limit, a delay (`time.sleep()`) is added when fetching detailed information for each café.
