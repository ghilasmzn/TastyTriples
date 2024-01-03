from SPARQLWrapper import SPARQLWrapper, JSON
import argparse

def query_open_restaurants(day, time):
    sparql = SPARQLWrapper("http://localhost:3030/Coopcycle/query")
    sparql.setQuery(f"""
        PREFIX schema: <http://schema.org/>
        SELECT ?restaurant ?name
        WHERE {{
            ?restaurant a schema:Restaurant ;
                        schema:openingHoursSpecification ?ohs ;
                        schema:name ?name .
            ?ohs schema:dayOfWeek "{day}" ;
                 schema:opens ?opens ;
                 schema:closes ?closes .
            FILTER (?opens <= "{time}" && "{time}" < ?closes)
        }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)

    for result in results["results"]["bindings"]:
        print(result["restaurant"]["value"], result["name"]["value"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find open restaurants at a given date and time.')
    parser.add_argument('-t', '--time', help='Inject the data into the triplestore')
    parser.add_argument('-d', '--day', help='Inject the data into the triplestore')
    args = parser.parse_args()
    if args.time and args.day:
        query_open_restaurants(args.day,args.time)
        