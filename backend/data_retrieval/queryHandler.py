from SPARQLWrapper import SPARQLWrapper, JSON
from prettytable import PrettyTable
from math import radians, sin, cos, sqrt, atan2

from rdflib import XSD
class QueryHandler:
    def __init__(self):
        self.sparql = SPARQLWrapper("http://localhost:3030/Coopcycle/query")

    def execute_query(self, query):
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        return results["results"]["bindings"]

    def display_results(self, results):
        # Utiliser PrettyTable pour afficher les résultats dans une table
        table = PrettyTable()
        table.field_names = ["Name", "Street Address", "Price"]

        for result in results:
            name = result["name"]["value"]
            street_address = result["streetAddress"]["value"]
            price = result.get("price", {}).get("value", "N/A")

            # Ajouter une nouvelle ligne à la table
            table.add_row([name, street_address, price])

        # Afficher la table dans le terminal
        print(table)

    def query_by_day(self, day):
        query = f"""
        PREFIX schema: <http://schema.org/>
        SELECT ?restaurant ?name ?streetAddress
        WHERE {{
            ?restaurant a schema:Restaurant ;
                        schema:openingHoursSpecification ?ohs ;
                        schema:name ?name ;
                        schema:address ?address .
            ?address schema:streetAddress ?streetAddress .
            ?ohs schema:dayOfWeek "{day}" ;
                 schema:opens ?opens ;
                 schema:closes ?closes .
        }}"""
        return self.execute_query(query)
    
    def query_by_time(self, time):
        query = f"""
        PREFIX schema: <http://schema.org/>
        SELECT ?restaurant ?name ?streetAddress
        WHERE {{
            ?restaurant a schema:Restaurant ;
                        schema:openingHoursSpecification ?ohs ;
                        schema:name ?name ;
                        schema:address ?address .
            ?address schema:streetAddress ?streetAddress .
            ?ohs schema:opens ?opens ;
                 schema:closes ?closes .
            FILTER (?opens <= "{time}" && "{time}" < ?closes)
        }}"""
        return self.execute_query(query)
    
    def query_by_price(query_handler, max_delivery_price=None, rank_by=None):
        query = """
            PREFIX schema: <http://schema.org/>
            PREFIX ns1: <http://schema.org/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT DISTINCT ?restaurant ?name ?streetAddress ?price
            WHERE {
                ?restaurant a schema:Restaurant ;
                            schema:address ?address ;
                            schema:potentialAction ?potentialAction .
                ?address schema:streetAddress ?streetAddress .
                ?potentialAction ns1:priceSpecification/ns1:price ?price .
                ?restaurant schema:name ?name .
        """

        # Ajouter un filtre pour le prix de livraison si le paramètre est fourni
        if max_delivery_price:
            query += f"""
                FILTER (xsd:float(?price) >= 0 && xsd:float(?price) <= {max_delivery_price})
            """
        query += "}\n"
        # Ajouter le classement par prix si l'argument est fourni
        if rank_by==1:
            query += "ORDER BY xsd:float(?price)"
        return query_handler.execute_query(query)
    
    def query_by_location(self, latitude, longitude, radius):
        # Approximation de la conversion en degrés pour un rayon donné en kilomètres
        latitude_approximation = radius / 111
        longitude_approximation = radius / (111 * cos(radians(latitude)))

        query = f"""
            PREFIX schema: <http://schema.org/>
            SELECT ?restaurant ?name ?streetAddress
            WHERE {{
                ?restaurant a schema:Restaurant ;
                            schema:address ?address ;
                            schema:name ?name .
                ?address schema:streetAddress ?streetAddress ;
                         schema:geo ?geo .
                ?geo schema:latitude ?restaurantLatitude ;
                     schema:longitude ?restaurantLongitude .

                FILTER (
                    ?restaurantLatitude >= {latitude - latitude_approximation} &&
                    ?restaurantLatitude <= {latitude + latitude_approximation} &&
                    ?restaurantLongitude >= {longitude - longitude_approximation} &&
                    ?restaurantLongitude <= {longitude + longitude_approximation}
                )
            }}
        """
        return self.execute_query(query)
    
    def query_combined(query_handler, day=None, time=None, location=None, max_delivery_price=None, rank_by=None):
        # Construire la requête SPARQL en fonction des paramètres fournis
        query = """
            PREFIX schema: <http://schema.org/>
            PREFIX ns1: <http://schema.org/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX geof: <http://www.opengis.net/def/function/geosparql/>

            SELECT DISTINCT ?restaurant ?name ?streetAddress ?price
            WHERE {
                ?restaurant a schema:Restaurant ;
                            schema:openingHoursSpecification ?ohs ;
                            schema:name ?name ;
                            schema:address ?address ;
                            schema:potentialAction ?potentialAction .
                ?address schema:streetAddress ?streetAddress .
                ?ohs schema:dayOfWeek ?day ;
                    schema:opens ?opens ;
                    schema:closes ?closes .
                ?potentialAction ns1:priceSpecification/ns1:price ?price .
        """

        # Ajouter des filtres pour la localisation si les paramètres sont fournis
        if location:
            latitude = location[0]
            longitude = location[1]
            radius = location[2]
            query += f"""
                ?address ns1:geo ?geo .
                ?geo ns1:latitude ?latitude ;
                    ns1:longitude ?longitude .

                # Filtrer par rayon
                FILTER (
                    ?latitude >= {latitude - (radius / 111)} &&
                    ?latitude <= {latitude + (radius / 111)} &&
                    ?longitude >= {longitude - (radius / (111 * cos(radians(latitude))))} &&
                    ?longitude <= {longitude + (radius / (111 * cos(radians(latitude))))}
                )
            """

        if day and time:
            query += f"""
                FILTER (?day = "{day}" && ?opens <= "{time}" && "{time}" < ?closes)
            """

        # Ajouter des filtres pour le prix de livraison si le paramètre est fourni
        if max_delivery_price:
            query += f"""
                FILTER (xsd:float(?price) >= 0 && xsd:float(?price) <= {max_delivery_price})
            """

        query += "}\n"

        # Ajouter le classement par prix ou par distance si l'argument est fourni
        if int(rank_by) == 1:
            query += "ORDER BY ?price\n"
        

        return query_handler.execute_query(query)


    
    

    