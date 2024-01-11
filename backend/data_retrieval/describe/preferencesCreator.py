from rdflib import Graph, URIRef, Literal, BNode, RDF, XSD, Namespace

class PreferencesCreator:
    def __init__(self):
        self.g = Graph()
        self.schema = Namespace("http://schema.org/")

    def add_person_preferences(self, name, postal_code, locality, seller_uri, max_price, currency, latitude, longitude, radius):
        person_uri = URIRef(f"http://localhost:3000/{name}")

        # Add person information
        self.g.add((person_uri, RDF.type, self.schema.Person))
        self.g.add((person_uri, self.schema.name, Literal(name)))
        
        address_node = BNode()
        self.g.add((person_uri, self.schema.address, address_node))
        self.g.add((address_node, RDF.type, self.schema.PostalAddress))
        self.g.add((address_node, self.schema.postalCode, Literal(postal_code)))
        self.g.add((address_node, self.schema.addressLocality, Literal(locality)))

        # Add seeking information
        seeking_node = BNode()
        self.g.add((person_uri, self.schema.seeks, seeking_node))
        self.g.add((seeking_node, self.schema.seller, URIRef(seller_uri)))

        # Add price specification
        price_spec_node = BNode()
        self.g.add((seeking_node, self.schema.priceSpecification, price_spec_node))
        self.g.add((price_spec_node, self.schema.maxPrice, Literal(max_price, datatype=XSD.float)))
        self.g.add((price_spec_node, self.schema.priceCurrency, Literal(currency)))

        # Add availableAtOrFrom information
        available_at_node = BNode()
        self.g.add((seeking_node, self.schema.availableAtOrFrom, available_at_node))

        # Add geoWithin information
        geo_circle_node = BNode()
        self.g.add((available_at_node, self.schema.geoWithin, geo_circle_node))
        self.g.add((geo_circle_node, RDF.type, self.schema.GeoCircle))

        # Add geoMidpoint information
        geo_midpoint_node = BNode()
        self.g.add((geo_circle_node, self.schema.geoMidpoint, geo_midpoint_node))
        self.g.add((geo_midpoint_node, self.schema.latitude, Literal(latitude, datatype=XSD.float)))
        self.g.add((geo_midpoint_node, self.schema.longitude, Literal(longitude, datatype=XSD.float)))

        self.g.add((geo_circle_node, self.schema.geoRadius, Literal(radius, datatype=XSD.float)))
        turtle_file_path = 'preferences_utilisateur'+name+'.ttl'
        self.g.serialize(destination=turtle_file_path, format="turtle")
        return turtle_file_path




