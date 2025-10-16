from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests

app = FastAPI(title="Address Lookup API", version="1.0")

def get_real_addresses(address: str, iso: str):
    """
    Fetch real addresses from OpenStreetMap (Nominatim API).
    Returns a list of display names or an error message.
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": address, "format": "json", "limit": 1, "accept-language": "en", "countrycodes": iso}
        headers = {"User-Agent": "address-checker"}  # Required by Nominatim
        
        response = requests.get(url, params=params, headers=headers, timeout=3)
        response.raise_for_status()
        
        data = response.json()
        display_names = [item["display_name"] for item in data if "display_name" in item]
        return display_names

    except requests.exceptions.Timeout:
        print('TIMEOUT')
        return []
    except requests.exceptions.RequestException as e:
        print(e)
        return []

@app.get("/get_addresses")
def get_addresses(address: str = Query(..., description="Address to search for"), iso: str = ""):
    """
    Get address variations from Nominatim.
    Example: /get_addresses?address=Baghdad
    """
    results = get_real_addresses(address, iso)
    return JSONResponse(content={"address": address, "results": results})
