import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import json
import re


class ShopsExtractor:
    def __init__(self, service_name, base_url):
        self.service_name = self.normalize_service_name(service_name)
        self.base_url = base_url
        self.restaurant_links = []
        self.service_data = []

    def extract_json_ld_from_page(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            json_ld_scripts = soup.find_all("script", type="application/ld+json")
            json_ld_data = [script.string for script in json_ld_scripts]
            return json_ld_data
        else:
            print(url)
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None

    def extract_restaurant_links(self):
        response = requests.get(self.base_url + "/fr/shops")
        if response.status_code == 200:

            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            restaurant_items = soup.find_all("div", class_="restaurant-item")

            if not restaurant_items:
                print("No restaurant items found. Exiting.")
                return

            for restaurant_item in restaurant_items:
                link = restaurant_item.find("a")
                href = link.get("href") if link else None
                self.restaurant_links.append(urljoin(self.base_url + "/fr", href))
        else:
            print(f"Failed to retrieve the base page. Status code: {response.status_code}")

    def normalize_service_name(self, service_name):
        normalized_name = re.sub(r'[^\w\s]', '', service_name.strip())
        normalized_name = re.sub(r'\s+', '_', normalized_name)

        return normalized_name

    def process_and_save_data(self):
        self.extract_restaurant_links()

        for restaurant_link in self.restaurant_links:
            json_ld_data = self.extract_json_ld_from_page(restaurant_link)
            restaurant_id = restaurant_link.split("/")[-1]

            if json_ld_data:

                service_directory = os.path.join("data_retrieval", "raw_data", self.service_name)
                os.makedirs(service_directory, exist_ok=True)

                with open(os.path.join(service_directory, f"{restaurant_id}.jsonld"), "w", encoding="utf-8") as output_file:
                    for data in json_ld_data:
                        data_dict = json.loads(data)
                        data_dict["@id"] = self.base_url + data_dict["@id"]

                        if "address" in data_dict:
                            data_dict["address"]["@id"] = self.base_url + data_dict["address"]["@id"]

                        data_dict["belongsToService"] = {"@id": self.base_url}
                        output_file.write(json.dumps(data_dict, indent=2))
                        output_file.close()
