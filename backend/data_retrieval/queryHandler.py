from SPARQLWrapper import SPARQLWrapper, JSON
from prettytable import PrettyTable
from math import radians,cos

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
        table.field_names = ["Name", "Street Address"]

        for result in results:
            name = result["name"]["value"]
            street_address = result["streetAddress"]["value"]

            # Ajouter une nouvelle ligne à la table
            table.add_row([name, street_address])

        # Afficher la table dans le terminal
        print(table)

    def query_open_restaurants_by_time(self, day, time):
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
            FILTER (?opens <= "{time}" && "{time}" < ?closes)
        }}"""
        return self.execute_query(query)


    def query_combined(self, day=None, time=None, latitude=None, longitude=None, radius=None):
        # Construire la requête SPARQL en fonction des paramètres fournis
        query = """
            PREFIX schema: <http://schema.org/>
            PREFIX ns1: <http://schema.org/>
            SELECT DISTINCT ?name ?streetAddress
            WHERE {
                ?restaurant a schema:Restaurant ;
                            schema:openingHoursSpecification ?ohs ;
                            schema:name ?name ;
                            schema:address ?address .
                ?address schema:streetAddress ?streetAddress .
                ?ohs schema:dayOfWeek ?day ;
                    schema:opens ?opens ;
                    schema:closes ?closes .
        """

        if day and time:
            query += f"""
                FILTER (?day = "{day}" && ?opens <= "{time}" && "{time}" < ?closes)
            """

        if latitude and longitude and radius:
            # Filtrer par latitude et longitude
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
        
        query += "}\n"
        return self.execute_query(query)




