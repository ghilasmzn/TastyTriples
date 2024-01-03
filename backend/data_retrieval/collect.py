from SPARQLWrapper import SPARQLWrapper, POST, JSON
from jsonldconverter import JSONLDConverter
from shopsExtractor import ShopsExtractor
from fusekiLoader import FusekiLoader

import argparse
import json
import os

RAW_DATA_DIR = "./data_retrieval/raw_data/"
SERVICE_FILE_PATH = RAW_DATA_DIR + "coopcycle.jsonld"


def insert_users_graph():
    dataset_url = "http://localhost:3030/Coopcycle"
    sparql_update = dataset_url + "/update"

    sparql = SPARQLWrapper(sparql_update)
    sparql.setQuery("""
            INSERT DATA {
            GRAPH <http://localhost:3030/Coopcycle/users> {
                _:user a schema:Person ;
                schema:email "admin@gmail.com" ;
                ex:password "admin" .
            }
        }
    """)


def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def insert_data():
    converter = JSONLDConverter()
    converter.convert_to_ttl(SERVICE_FILE_PATH)

    ttl_output_path = RAW_DATA_DIR + 'coopcycle.ttl'

    converter.export_to_file(ttl_output_path, format='turtle')
    fuseki_loader = FusekiLoader('http://localhost:3030/Coopcycle')

    if not fuseki_loader.is_running():
        fuseki_loader.start_server()

    fuseki_loader.load_data(ttl_output_path)

    json_files = [os.path.join(root, file)
                  for root, _, files in os.walk(RAW_DATA_DIR)
                  for file in files if file.endswith(".jsonld")]

    for file in json_files:
        if file == SERVICE_FILE_PATH:
            continue

        fuseki_loader.load_data(file, content_type='application/ld+json')

    fuseki_loader.stop_server()


def scrap_data():
    services = load_json_data(SERVICE_FILE_PATH)
    for service in services:
        coopcycle_url = service.get("coopcycle_url")
        service_name = service.get("name")

        if coopcycle_url and service_name:
            extractor = ShopsExtractor(service_name, coopcycle_url)
            extractor.process_and_save_data()
        else:
            print(f"Skipping service {service_name} as coopcycle_url is missing.")


def main():
    parser = argparse.ArgumentParser(description='Process command-line options.')

    parser.add_argument('-i', '--inject', action='store_true',
                        help='Inject the data into the triplestore')
    parser.add_argument('-s', '--scrapping', action='store_true',
                        help='Scrap the data from the website and save it inside the raw_data folder')

    args = parser.parse_args()

    if args.inject:
        insert_data()

    if args.scrapping:
        scrap_data()


if __name__ == "__main__":
    main()
