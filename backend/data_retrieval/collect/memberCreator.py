import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from geopy.geocoders import Nominatim
from fusekiLoader import FusekiLoader

class MemberCreator:
    def __init__(self, uri):
        self.uri = uri
        self.name = urlparse(self.uri).hostname.split('.')[0].capitalize()
    def get_name(self):
        return self.name
    def get_html_content(self, uri):
        try:
            response = requests.get(uri)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching HTML content from {uri}: {e}")
            return None

    def extract_location(self, soup):
        # Essayez de trouver l'élément avec l'ID 'geocode-earth'
        location_element = soup.find('div', id='geocode-earth')
        if location_element:
            location_data = location_element.get('data-boundary-circle-latlon', '').split(',')
            latitude = location_data[0] if location_data else ''
            longitude = location_data[1] if len(location_data) > 1 else ''
        else:
            # Si 'geocode-earth' n'est pas trouvé, essayez avec 'google'
            location_element = soup.find('div', id='google')
            location_data = location_element.get('data-location', '').split(',')
            latitude = location_data[0] if location_data else ''
            longitude = location_data[1] if len(location_data) > 1 else ''

        return latitude, longitude
    
    def extract_description_from_aboutUs(self, uri):
        html_content = self.get_html_content(f"{uri}/fr/a-propos")
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            description = ' '.join(p.text.strip() for p in soup.select('.about-us p'))
            return description.strip()
        except Exception as e:
            print(f"Error fetching description from aboutUs: {e}")
            return None

    def extract_description_from_banner(self, soup):
        description_element = soup.find('h1', class_='banner-title text-center')
        if description_element:
            return description_element.get_text(strip=True)
        return ''

    def extract_country(self, soup):
        body_element = soup.find('body')
        if body_element:
            return body_element.get('data-country', '')
        return ''
    
    def get_city(self, latitude, longitude):
        # Initialise le géocodeur Nominatim
        geolocator = Nominatim(user_agent="your_app_name")

        # Obtient l'adresse en utilisant les coordonnées géographiques
        location = geolocator.reverse((latitude, longitude), language='fr')  # Assurez-vous de spécifier la langue si nécessaire

        # Récupère la ville à partir de l'adresse
        city = location.raw.get('address', {}).get('city', '')

        return city
    
    def create_member(self):
        html_content = self.get_html_content(self.uri)
        if not html_content:
            print("Failed to fetch HTML content. Exiting.")
            return

        soup = BeautifulSoup(html_content, 'html.parser')

        description = (
            self.extract_description_from_aboutUs(self.uri) or
            self.extract_description_from_banner(soup) or ''
        )

        footer = soup.find('footer')
        mail_element = footer.find('a', href=re.compile(r'mailto:'))
        mail = mail_element.get_text(strip=True) if mail_element else ''

        phone_element = footer.find('span', text=re.compile(r'^\d'))
        phone = phone_element.get_text() if phone_element else ''

        latitude, longitude = self.extract_location(soup)
        print(latitude, longitude)
        country = self.extract_country(soup)
        if latitude and longitude :
            city = self.get_city(latitude, longitude)

        # Générer le graph RDF sous forme de chaîne TTL
        ttl_graph = f"""
            @prefix ns1: <http://schema.org/> .
            <{self.uri}> a ns1:ProfessionalService ;
                ns1:city "{city}" ;
                ns1:coopcycle_url "{self.uri}" ;
                ns1:country "{country}" ;
                ns1:description "{description}" ;
                ns1:latitude {latitude} ;
                ns1:longitude {longitude} ;
                ns1:mail "{mail}" ;
                ns1:name "{self.name}" ;
                ns1:sameAs "{phone}" .
        """
        ttl_output_path="data_retrieval/raw_data/"+self.name+".ttl"
        print(ttl_graph,file=open(ttl_output_path,"w"))
        fuseki_loader = FusekiLoader('http://localhost:3030/Coopcycle')
        fuseki_loader.load_data_from_file(ttl_output_path)

