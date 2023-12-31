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
    jsonld_file_path="backend/data_retrieval/raw_data/coopcycle.jsonld"
    converter.convert_to_rdf(jsonld_file_path)

    rdf_output_path = 'backend/data_retrieval/raw_data/coopcycle.ttl'
    # Exporter les triplets RDF dans un fichier Turtle
    converter.export_to_file(rdf_output_path, format='turtle')
    fuseki_loader = FusekiLoader('http://localhost:3030/Coopcycle')
    fuseki_loader.load_data(rdf_output_path)
    
    shopsExtractor = ShopsExtractor("biclooo","https://biclooo.coopcycle.org/fr/shops")
    shopsExtractor.process_and_save_data()

if __name__ == "__main__":
    main()
