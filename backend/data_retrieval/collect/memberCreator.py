import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from geopy.geocoders import Nominatim
from fusekiLoader import FusekiLoader
import pyshacl

from colorama import init, Fore, Back, Style

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
    
    def write_shacl_shapes(self, output_path):
        shacl_shapes = """
            @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix sh: <http://www.w3.org/ns/shacl#> .
            @prefix ns1: <http://schema.org/> .
            @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

            ns1:ProfessionalServiceShape
                a sh:NodeShape ;
                sh:targetClass ns1:ProfessionalService ;
                sh:property [
                    sh:path ns1:city ;
                    sh:datatype xsd:string ;
                    sh:minCount 1 ;
                    sh:message "City is required." ;
                ] ;
                sh:property [
                    sh:path ns1:coopcycle_url ;
                    sh:datatype xsd:string ;
                    sh:minCount 1 ;
                    sh:message "Coopcycle URL is required." ;
                ] ;
                sh:property [
                    sh:path ns1:country ;
                    sh:datatype xsd:string ;
                    sh:minCount 1 ;
                    sh:message "Country is required." ;
                ] ;
                sh:property [
                    sh:path ns1:description ;
                    sh:datatype xsd:string ;
                    sh:minCount 1 ;
                    sh:message "Description is required." ;
                ] ;
                sh:property [
                    sh:path ns1:latitude ;
                    sh:datatype xsd:float ;
                    sh:minCount 1 ;
                    sh:message "Latitude is required." ;
                ] ;
                sh:property [
                    sh:path ns1:longitude ;
                    sh:datatype xsd:float ;
                    sh:minCount 1 ;
                    sh:message "Longitude is required." ;
                ] ;
                sh:property [
                    sh:path ns1:mail ;
                    sh:datatype xsd:string ;
                    sh:minCount 1 ;
                    sh:message "Mail is required." ;
                ] ;
                sh:property [
                    sh:path ns1:name ;
                    sh:datatype xsd:string ;
                    sh:minCount 1 ;
                    sh:message "Name is required." ;
                ] ;
                sh:property [
                    sh:path ns1:sameAs ;
                    sh:datatype xsd:string ;
                    sh:message "SameAs is optional." ;
                ] .
        """

        with open(output_path, "w") as shacl_file:
            shacl_file.write(shacl_shapes)
    
    def validate_rdf_graph(self, graph_path, shacl_shapes_path):
        """Valide le RDF graph avec les formes SHACL."""
        rdf_graph = open(graph_path, 'rb').read()
        shacl_shapes = open(shacl_shapes_path, 'rb').read()

        conforms, report_graph, _ = pyshacl.validate(
            data_graph=rdf_graph,
            shacl_graph=shacl_shapes,
            format="turtle",
            inference="rdfs",
            debug=True
        )

        if not conforms:
            print("Validation failed. SHACL Errors:")
            print(report_graph.serialize(format="turtle").decode())
        else:
            print("Validation succeeded.")


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

        # remove all non alphanumeric characters
        description = re.sub(r'\W+', ' ', description)
        
        # remove the new line characters
        description = description.replace(u'\n', ' ').replace(u'\r', ' ')

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
            @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

            <{self.uri}> a ns1:ProfessionalService ;
                ns1:city '{city}'^^xsd:string ;
                ns1:coopcycle_url '{self.uri}'^^xsd:string ;
                ns1:country '{country}'^^xsd:string ;
                ns1:description '{description}'^^xsd:string ;
                ns1:latitude '{latitude}'^^xsd:float ;
                ns1:longitude '{longitude}'^^xsd:float ;
                ns1:mail '{mail}'^^xsd:string ;
                ns1:name '{self.name}'^^xsd:string ;
                ns1:sameAs '{phone}'^^xsd:string .
        """
        ttl_output_path="data_retrieval/raw_data/"+ self.name +".ttl"
        print(ttl_graph, file=open(ttl_output_path,"w", encoding="utf-8"))

        shacl_output_path="data_retrieval/raw_data/coopcycle_member.shacl"
        self.write_shacl_shapes(shacl_output_path)
        try :
            self.validate_rdf_graph(ttl_output_path, shacl_output_path)
        except Exception as e:
            print(f"{Fore.RED}Error validating RDF graph: {e}{Style.RESET_ALL}")
            return False

        return True