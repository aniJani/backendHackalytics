from fastapi import APIRouter, HTTPException
import requests
import os
from app.config import settings

router = APIRouter()

# Base URL for FRED API
FRED_BASE_URL = "https://api.stlouisfed.org/fred"

# Get the FRED API key from environment variables
FRED_API_KEY = settings.FRED_API_KEY
if not FRED_API_KEY:
    raise Exception("FRED_API_KEY is not set in environment variables.")


@router.get("/datasets", tags=["fred"])
def get_fred_datasets(series_id: str, limit: int = 5):
    """
    Retrieves a list of related datasets from the FRED API for the given series_id.

    - **series_id**: The FRED series ID (e.g., "GDP").
    - **limit**: Optional number of datasets to return.
    """
    # Build the URL for the FRED 'series/search' endpoint (or another relevant endpoint)
    # See: https://fred.stlouisfed.org/docs/api/fred/series_search.html
    url = f"{FRED_BASE_URL}/series/search"
    params = {
        "api_key": FRED_API_KEY,
        "search_text": series_id,
        "file_type": "json",
        "limit": limit,
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error fetching data from FRED API"
        )

    data = response.json()
    # Optionally, extract and transform the data as needed
    # For example, we can return the list of series found:
    return data
