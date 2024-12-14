# Local Business Data Fetcher

A Python tool that fetches comprehensive business data using Google Maps Geocoding API and RapidAPI's Local Business Data API. The tool retrieves detailed information about businesses including contact details, operating hours, reviews, social media presence, and more.

## 🌟 Features

- Geocoding of location queries using Google Maps API
- Comprehensive business data extraction including:
  - Basic details (name, address, contact info)
  - Operating hours and status
  - Ratings and reviews
  - Social media presence
  - Photos and posts
  - Service offerings and highlights
- CSV export functionality
- Pagination support for handling large datasets
- Configurable search parameters
- Location-based filtering

## 📋 Prerequisites

- Python 3.6+
- RapidAPI account and key
- Google Maps API key

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/local-business-data-fetcher.git
cd local-business-data-fetcher
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your API keys:
```
RAPIDAPI_KEY=your_rapidapi_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

## 📖 Usage

Run the script:
```bash
python fetch_full_business_data.py
```

Follow the interactive prompts to:
1. Enter business query (e.g., "restaurant", "plumber")
2. Specify location (e.g., "Milwaukee, USA")
3. Configure optional parameters:
   - Results per page limit
   - Zoom level
   - Language
   - Business status
   - Contact extraction preferences
   - Field filters
   - Business subtypes
   - Verification status

The script will create a `business_data.csv` file with the fetched data.

## 📁 Project Structure

```
local-business-data-fetcher/
├── fetch_full_business_data.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
├── LICENSE
└── tests/
    └── test_fetch_business_data.py
```

## 📄 Configuration

The script uses two main API keys:
- RapidAPI key for the Local Business Data API
- Google Maps API key for geocoding

These should be stored in environment variables or a `.env` file.

## 🔍 Sample Output Fields

The CSV output includes:
- Business ID and Google/Place IDs
- Name and contact information
- Full address and coordinates
- Ratings and review count
- Business type and subtypes
- Service options and offerings
- Working hours
- Social media links
- Sample reviews and posts
- And more...

## ⚠️ Rate Limits and API Usage

- Be mindful of API rate limits
- Google Maps Geocoding API has daily quota limits
- RapidAPI may have request limits based on your subscription

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
