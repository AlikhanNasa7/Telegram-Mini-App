import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


def get_images(keyword: str) -> list[dict]:
    if not SERPAPI_API_KEY:
        raise ValueError("SERPAPI_API_KEY is not set. Please set it in the .env file.")

    # Make the request to SerpAPI
    search = requests.get(
        f"https://serpapi.com/search.json?q={keyword}&engine=google_images&ijn=0&api_key={SERPAPI_API_KEY}"
    )

    # Check if the request was successful
    if search.status_code != 200:
        raise Exception(f"Failed to fetch images. Status code: {search.status_code}")

    # Parse the JSON response
    results = search.json()

    # Get the image results, if they exist
    image_results = results.get("images_results", [])
    if not image_results:
        raise Exception("No image results found.")

    # Extract image titles and URLs
    images = [
        {
            "title": image_result.get("title", "No Title").replace(".", ""),
            "image": image_result["original"],
        }
        for image_result in image_results
    ]
    return images[:30]
