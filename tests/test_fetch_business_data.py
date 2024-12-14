import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys

# Add parent directory to path to import main script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fetch_full_business_data import geocode_location, fetch_data, fetch_business_details

class TestBusinessDataFetcher(unittest.TestCase):
    def setUp(self):
        """Set up test environment variables"""
        os.environ['RAPIDAPI_KEY'] = 'test_rapidapi_key'
        os.environ['GOOGLE_API_KEY'] = 'test_google_api_key'

    def test_geocode_location(self):
        """Test geocoding functionality"""
        with patch('http.client.HTTPSConnection') as mock_connection:
            # Mock successful response
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps({
                "status": "OK",
                "results": [{
                    "geometry": {
                        "location": {
                            "lat": 43.0389,
                            "lng": -87.9065
                        }
                    }
                }]
            }).encode()
            mock_connection.return_value.getresponse.return_value = mock_response

            lat, lng = geocode_location("Milwaukee, WI")
            self.assertEqual(lat, 43.0389)
            self.assertEqual(lng, -87.9065)

    def test_fetch_data(self):
        """Test API data fetching"""
        with patch('http.client.HTTPSConnection') as mock_connection:
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps({
                "data": [{"business_id": "test123"}]
            }).encode()
            mock_connection.return_value.getresponse.return_value = mock_response

            result = fetch_data(
                "test.api.com",
                "/endpoint",
                "param=value",
                {"header": "value"}
            )
            self.assertIn("data", result)
            self.assertIsInstance(result["data"], list)

    def test_fetch_business_details(self):
        """Test business details fetching"""
        with patch('fetch_full_business_data.fetch_data') as mock_fetch:
            mock_fetch.return_value = {
                "data": [{
                    "business_id": "test123",
                    "name": "Test Business",
                    "address": "123 Test St"
                }]
            }
            
            result = fetch_business_details("test123")
            self.assertIsInstance(result, list)
            self.assertTrue(len(result) > 0)
            self.assertEqual(result[0]["business_id"], "test123")

if __name__ == '__main__':
    unittest.main()
