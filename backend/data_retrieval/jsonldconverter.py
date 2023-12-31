import json
from rdflib import Graph, Namespace, URIRef, Literal, BNode, RDF
from urllib.parse import quote

class JSONLDConverter:
    def __init__(self):
        self.graph = Graph()
        self.schema = Namespace("http://schema.org/")

    def generate_service_uri(self, entry):
        # Utiliser 'coopcycle_url' s'il existe
        coopcycle_url = entry.get('coopcycle_url')
        if coopcycle_url:
            return URIRef(coopcycle_url)

        # Utiliser 'name' comme base pour créer l'URI
        service_name = entry.get('name', '')
        return URIRef(f"{self.schema}#{quote(service_name, safe='/:?=&')}")

    def convert_to_rdf(self, jsonld_file):
        with open(jsonld_file, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        for entry in json_data:
            service_uri = self.generate_service_uri(entry)

            self.graph.add((service_uri, RDF.type, self.schema.ProfessionalService))

            for prop, value in entry.items():
                if prop == 'text':
                    for lang, desc in value.items():
                        self.graph.add((service_uri, self.schema.description, Literal(desc, lang=lang)))
                elif prop in ['facebook_url', 'twitter_url', 'instagram_url']:
                    encoded_url = quote(value, safe='/:?=&')
                    self.graph.add((service_uri, self.schema.sameAs, URIRef(encoded_url)))
                elif isinstance(value, list):
                    for item in value:
                        self.graph.add((service_uri, self.schema[prop], Literal(item) if not isinstance(item, dict) else BNode()))
                else:
                    self.graph.add((service_uri, self.schema[prop], Literal(value) if not isinstance(value, dict) else BNode()))

    def serialize_rdf(self, format='turtle'):
        return self.graph.serialize(format=format)

    def export_to_file(self, filename, format='turtle'):
        with open(filename, 'wb') as file:
            file.write(self.serialize_rdf(format).encode('utf-8'))
