import requests
import os
from dotenv import load_dotenv

load_dotenv()
UNSPLASH_ACCESS_KEY = os.getenv("UNSPALSH_ACCESS_KEY")


def search_unsplash_images(keyword, client_id, per_page=5):
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {client_id}"}
    params = {"query": keyword, "per_page": per_page}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        results = response.json()
        image_urls = [result["urls"]["regular"] for result in results["results"]]
        return image_urls
    else:
        print(f"Error: {response.status_code}")
        return []


# client_id = UNSPLASH_ACCESS_KEY
# keyword = "next js"
# images = search_unsplash_images(keyword, client_id)
