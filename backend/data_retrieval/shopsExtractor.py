import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

class ShopsExtractor:
    def __init__(self, service_name,base_url):
        self.service_name = service_name
        self.base_url = base_url
        self.restaurant_links = []

    def extract_json_ld_from_page(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            json_ld_scripts = soup.find_all("script", type="application/ld+json")
            json_ld_data = [script.string for script in json_ld_scripts]
            return json_ld_data
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None

    def extract_restaurant_links(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            restaurant_items = soup.find_all("div", class_="restaurant-item")

            for restaurant_item in restaurant_items:
                link = restaurant_item.find("a")
                href = link.get("href") if link else None
                self.restaurant_links.append(urljoin(self.base_url, href))
        else:
            print(f"Failed to retrieve the base page. Status code: {response.status_code}")

    def process_and_save_data(self):
        self.extract_restaurant_links()

        for restaurant_link in self.restaurant_links:
            json_ld_data = self.extract_json_ld_from_page(restaurant_link)
            restaurant_id = restaurant_link.split("/")[-1]

            if json_ld_data:
                # Create a directory for each service if it doesn't exist
                service_directory = os.path.join("backend", "data_retrieval", "raw_data", self.service_name)
                os.makedirs(service_directory, exist_ok=True)

                with open(os.path.join(service_directory, f"{restaurant_id}.jsonld"), "w", encoding="utf-8") as output_file:
                    for data in json_ld_data:
                        output_file.write(json.dumps(json.loads(data), indent=2))

