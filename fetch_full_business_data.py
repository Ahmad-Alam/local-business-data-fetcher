import os
import http.client
import json
import csv
from urllib.parse import quote
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST', 'local-business-data.p.rapidapi.com')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if not RAPIDAPI_KEY or not GOOGLE_API_KEY:
    raise ValueError("API keys not found in environment variables. Please check your .env file.")

# Helper Functions
def geocode_location(location):
    """Geocode location using Google Maps API."""
    print(f"Geocoding location '{location}' using Google API...")
    conn = http.client.HTTPSConnection("maps.googleapis.com")
    params = f"/maps/api/geocode/json?address={quote(location)}&key={GOOGLE_API_KEY}"
    conn.request("GET", params)
    res = conn.getresponse()
    data = json.loads(res.read())
    
    if data.get("status") == "OK":
        result = data["results"][0]
        lat = result["geometry"]["location"]["lat"]
        lng = result["geometry"]["location"]["lng"]
        print(f"Location geocoded: Latitude={lat}, Longitude={lng}")
        return lat, lng
    else:
        print(f"Geocoding failed: {data.get('status')}")
        return None, None

def fetch_data(host, endpoint, params, headers):
    """Fetch data from the API."""
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", f"{endpoint}?{params}", headers=headers)
    res = conn.getresponse()
    return json.loads(res.read())

def fetch_business_details(business_id):
    """Fetch detailed business data."""
    endpoint = "/business-details"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }
    params = f"business_id={business_id}&extract_emails_and_contacts=true&language=en&region=us"
    return fetch_data(RAPIDAPI_HOST, endpoint, params, headers).get("data", [])

def write_to_csv(data):
    """Write data to CSV."""
    csv_file = "business_data.csv"
    print(f"Writing data to {csv_file}...")
    if data:
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully written to {csv_file}")
    else:
        print("No data to write to CSV.")

# Main Function
def fetch_all_business_data(
    query, 
    location, 
    limit=50, 
    zoom=13, 
    language="en", 
    business_status="OPEN", 
    extract_contacts=False, 
    fields=None, 
    subtypes=None, 
    verified=False
):
    """Fetch and process all business data."""
    print(f"Fetching business data for '{query}' in '{location}'...")

    # Geocode the location
    lat, lng = geocode_location(location)
    if not lat or not lng:
        print("Failed to geocode location. Exiting.")
        return

    # Fetch businesses with pagination
    endpoint = "/search-nearby"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    all_business_data = []
    next_page_token = None
    while True:
        params = f"query={quote(query)}&lat={lat}&lng={lng}&limit={limit}&language={language}&region=us&status={business_status}"
        if fields:
            params += f"&fields={quote(fields)}"
        if subtypes:
            params += f"&subtypes={quote(subtypes)}"
        if verified:
            params += "&verified=true"
        if next_page_token:
            params += f"&page_token={next_page_token}"

        response = fetch_data(RAPIDAPI_HOST, endpoint, params, headers)
        businesses = response.get("data", [])
        if not businesses:
            print("No more businesses found.")
            break

        print(f"Found {len(businesses)} businesses on this page. Fetching detailed data...")
        for business in businesses:
            details = fetch_business_details(business.get("business_id"))
            for detail in details:
                if location.lower() not in [
                    detail.get("city", "").lower(),
                    detail.get("state", "").lower(),
                    detail.get("county", "").lower(),
                ]:
                    continue  # Skip if location doesn't match

                emails_and_contacts = (detail or {}).get("emails_and_contacts", {}) or {}
                about_details = ((detail or {}).get("about") or {}).get("details", {}) or {}

                service_options = ", ".join(about_details.get("Service options", {}).keys())
                offerings = ", ".join(about_details.get("Offerings", {}).keys())
                highlights = ", ".join(about_details.get("Highlights", {}).keys())
                additional_attributes = ", ".join(about_details.keys())

                photos = detail.get("photos_sample", [])
                image_urls = [
                    photo.get("photo_url", "") for photo in photos[:5] if photo.get("photo_url")
                ]

                all_business_data.append({
                    "Business ID": (detail or {}).get("business_id", ""),
                    "Google ID": (detail or {}).get("google_id", ""),
                    "Place ID": (detail or {}).get("place_id", ""),
                    "Name": (detail or {}).get("name", ""),
                    "Phone Number": (detail or {}).get("phone_number", ""),
                    "Website": (detail or {}).get("website", ""),
                    "Full Address": (detail or {}).get("full_address", ""),
                    "Latitude": (detail or {}).get("latitude", ""),
                    "Longitude": (detail or {}).get("longitude", ""),
                    "City": (detail or {}).get("city", ""),
                    "State": (detail or {}).get("state", ""),
                    "Zipcode": (detail or {}).get("zipcode", ""),
                    "Country": (detail or {}).get("country", ""),
                    "Rating": (detail or {}).get("rating", ""),
                    "Review Count": (detail or {}).get("review_count", ""),
                    "Type": (detail or {}).get("type", ""),
                    "Subtypes": ", ".join((detail or {}).get("subtypes", [])),
                    "Verified": (detail or {}).get("verified", False),
                    "Price Level": (detail or {}).get("price_level", "Not Available"),
                    "Service Options": service_options,
                    "Offerings": offerings,
                    "Highlights": highlights,
                    "Additional Attributes": additional_attributes,
                    "Opening Status": (detail or {}).get("opening_status", ""),
                    "Working Hours": "; ".join([f"{day}: {', '.join(hours or [])}" for day, hours in ((detail or {}).get("working_hours", {}) or {}).items()]),
                    "Place Link": (detail or {}).get("place_link", ""),
                    "Reviews Link": (detail or {}).get("reviews_link", ""),
                    "Posts Link": (detail or {}).get("posts_link", ""),
                    "Owner Link": (detail or {}).get("owner_link", ""),
                    "Photos": "; ".join(image_urls),
                    "Social Media": ", ".join([f"{key}: {value}" for key, value in (emails_and_contacts or {}).items() if key not in ["emails", "phone_numbers"] and value]),
                    "Emails": ", ".join(emails_and_contacts.get("emails", [])),
                    "Contacts": ", ".join(emails_and_contacts.get("phone_numbers", [])),
                    "Posts": "; ".join([post.get("post_text", "") for post in ((detail or {}).get("posts_sample") or []) if post and post.get("post_text")]),
                    "Reviews": "; ".join([review.get("review_text", "") for review in ((detail or {}).get("reviews_sample") or []) if review and review.get("review_text")])
                })

        next_page_token = response.get("next_page_token")
        if not next_page_token:
            print("No next page token. Finished fetching.")
            break

    if not all_business_data:
        print(f"No businesses found in the exact location '{location}'. Exiting.")
    else:
        write_to_csv(all_business_data)

# Run the Script
if __name__ == "__main__":
    query = input("Enter the business query (e.g., plumber, restaurant): ").strip()
    region = input("Enter the region (e.g., Milwaukee, USA): ").strip()
    limit = int(input("Enter the maximum number of businesses per page (default 100): ").strip() or 100)
    zoom = int(input("Enter the zoom level (default 13): ").strip() or 13)
    language = input("Enter the language code (default 'en'): ").strip() or "en"
    business_status = input("Enter the business status (default 'OPEN'): ").strip() or "OPEN"
    extract_contacts = input("Extract emails and contacts? (yes or no, default 'no'): ").strip().lower() == "yes"
    fields = input("Enter specific fields to include (comma-separated, optional): ").strip() or None
    subtypes = input("Enter subtypes (comma-separated, optional): ").strip() or None
    verified = input("Only verified businesses? (yes or no, optional): ").strip().lower() == "yes"

    fetch_all_business_data(
        query=query,
        location=region,
        limit=limit,
        zoom=zoom,
        language=language,
        business_status=business_status,
        extract_contacts=extract_contacts,
        fields=fields,
        subtypes=subtypes,
        verified=verified,
    ) 
