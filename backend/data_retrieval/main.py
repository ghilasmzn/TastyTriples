import json
from jsonldconverter import JSONLDConverter
from fusekiLoader import FusekiLoader
from shopsExtractor import ShopsExtractor

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def main():
    converter = JSONLDConverter()
    # Charger les données depuis le fichier coopcycle.jsonld
    services_file_path="backend/data_retrieval/raw_data/coopcycle.jsonld"
    converter.convert_to_ttl(services_file_path)

    ttl_output_path = 'backend/data_retrieval/raw_data/coopcycle.ttl'
    # Exporter les triplets RDF dans un fichier Turtle
    converter.export_to_file(ttl_output_path, format='turtle')
    fuseki_loader = FusekiLoader('http://localhost:3030/Coopcycle')
    fuseki_loader.load_ttl_data(ttl_output_path)
    
    services = load_json_data(services_file_path)
    for service in services:
        
        coopcycle_url = service.get("coopcycle_url")  # Utiliser get pour obtenir la valeur ou None si elle n'existe pas
        service_name = service.get("name")
        if coopcycle_url and service_name:
            extractor = ShopsExtractor(service_name, coopcycle_url)
            extractor.process_and_save_data()
        else:
            print(f"Skipping service {service_name} as coopcycle_url is missing.")
    

if __name__ == "__main__":
    main()
