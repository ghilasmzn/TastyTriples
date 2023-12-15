import requests
from bs4 import BeautifulSoup
import json

def extract_json_ld_from_page(url):
    # Effectuer une requête GET pour récupérer le contenu HTML de la page
    response = requests.get(url)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        html_content = response.text
        # Analyser le HTML avec BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Trouver les balises script avec le type "application/ld+json" sur la page du restaurant
        json_ld_scripts = soup.find_all("script", type="application/ld+json")

        # Parcourir les scripts et retourner le contenu JSON-LD
        json_ld_data = []
        for script in json_ld_scripts:
            json_ld_data.append(script.string)

        return json_ld_data
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


# L'URI de la coopérative Beefast
coopcycle_url = "https://biclooo.coopcycle.org"

# Effectuer une requête GET pour récupérer le contenu HTML de la page
response = requests.get(coopcycle_url)
html_content = response.text

# Analyser le HTML avec BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Trouver tous les éléments div avec la classe "restaurant-item"
restaurant_items = soup.find_all("div", class_="restaurant-item")

restaurant_links = []
# Parcourir les éléments et extraire le lien et le titre
for restaurant_item in restaurant_items:
    # Extraire le lien
    link = restaurant_item.find("a")
    href = link.get("href") if link else None
    restaurant_links.append("https://biclooo.coopcycle.org"+href)
    # Extraire le titre
    title = restaurant_item.find("h4", class_="restaurant-item__title").text if restaurant_item.find("h4", class_="restaurant-item__title") else None

    # Afficher les résultats
    print(f"Link: {href}")
    print(f"Title: {title}")
    print("\n---\n")


# Parcourir les liens des restaurants et écrire les données JSON-LD dans un fichier

for restaurant_link in restaurant_links:
    json_ld_data = extract_json_ld_from_page(restaurant_link)
    restaurant_id = restaurant_link.split("/")[-1]
    if json_ld_data:
        with open(f"json_ld_output_{restaurant_id}.json", "w", encoding="utf-8") as output_file:
            # Écrire les résultats dans le fichier
            for data in json_ld_data:
                output_file.write(json.dumps(json.loads(data), indent=2))

