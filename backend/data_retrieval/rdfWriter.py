import json
from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF, RDFS, XSD
from urllib.parse import quote

# Charger le JSON
with open('coopcycle.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Créer un graph RDF
g = Graph()

# Définir le préfixe de schema.org
schema = Namespace("http://schema.org/")

# Parcourir chaque entrée dans le JSON
for entry in data:
    if 'url' in entry:
        # Créer un identifiant unique pour le service de livraison
        service_uri = URIRef(entry['url'])

    # Ajouter le type schema:ProfessionalService
    g.add((service_uri, RDF.type, schema.ProfessionalService))

    # Ajouter le nom du service
    g.add((service_uri, schema.name, Literal(entry['name'])))

    # Ajouter la description en plusieurs langues
    if 'text' in entry:
        for lang, desc in entry['text'].items():
            g.add((service_uri, schema.description, Literal(desc, lang=lang)))

    # Ajouter l'adresse
    if 'latitude' in entry and 'longitude' in entry:
        address_bnode = BNode()
        g.add((service_uri, schema.address, address_bnode))
        g.add((address_bnode, schema.addressLocality, Literal(entry['city'])))
        g.add((address_bnode, schema.addressCountry, Literal(entry['country'])))

    # Ajouter le fournisseur
    if 'provider' in entry:
        provider_uri = URIRef(entry['provider']['url'])
        g.add((service_uri, schema.provider, provider_uri))
        g.add((provider_uri, RDF.type, schema.Organization))
        g.add((provider_uri, schema.name, Literal(entry['provider']['name'])))

    # Ajouter l'adresse e-mail
    if 'mail' in entry:
        g.add((service_uri, schema.email, Literal(entry['mail'])))

    # Ajouter les liens sociaux
    if 'facebook_url' in entry:
        g.add((service_uri, schema.sameAs, URIRef(quote(entry['facebook_url']))))
    if 'twitter_url' in entry:
        g.add((service_uri, schema.sameAs, URIRef(entry['twitter_url'])))
    if 'instagram_url' in entry:
        g.add((service_uri, schema.sameAs, URIRef(entry['instagram_url'])))

        # Ajouter la localisation géographique
    if 'latitude' in entry and 'longitude' in entry:
        map_node = BNode()
        g.add((service_uri, schema.hasMap, map_node))
        g.add((map_node, schema.latitude, Literal(entry['latitude'], datatype=XSD.float)))
        g.add((map_node, schema.longitude, Literal(entry['longitude'], datatype=XSD.float)))


# Serialiser le graph en Turtle
rdf_turtle = g.serialize(destination='output.ttl',format='turtle')

