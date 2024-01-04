from SPARQLWrapper import SPARQLWrapper, JSON
import argparse
from queryHandler import QueryHandler  # Assurez-vous d'avoir le bon import du module


def combine_results(open_restaurants_results, location_results):
    # Vous pouvez ajuster cela selon vos besoins, par exemple, utiliser intersection, union, etc.
    return open_restaurants_results.intersection(location_results)

def main():
    parser = argparse.ArgumentParser(description='Find open restaurants at a given date and time.')
    parser.add_argument('-t', '--time', help='Time to check in the format "HH:MM".')
    parser.add_argument('-d', '--day', help='Day of the week.')
    parser.add_argument('-l', '--location', nargs=2, type=float, metavar=('LATITUDE', 'LONGITUDE'),
                        help='Filter restaurants by location. Specify latitude and longitude.')
    parser.add_argument('-r', '--radius', type=float, help='Radius (in meters) for location-based filtering.')
    
    args = parser.parse_args()

    query_handler = QueryHandler()

    open_restaurants_results = set()
    location_results = set()

    if args.time and args.day and args.location and args.radius:
        # Si le temps, le jour, la localisation et le rayon sont fournis, exécuter la requête combinant les deux conditions
        results = query_handler.query_combined(args.day, args.time, args.location[0], args.location[1], args.radius)
    elif args.time and args.day:
        # Si le temps et le jour sont fournis, exécuter la requête pour trouver les restaurants ouverts à cette date et heure
        results = query_handler.query_combined(args.day, args.time)
    elif args.location and args.radius:
        # Si la localisation et le rayon sont fournis exécuter la requête pour trouver les restaurants dans ce rayon
        results = query_handler.query_combined(latitude=args.location[0], longitude=args.location[1], radius=args.radius)
    else:
        # Aucun des cas ci-dessus n'est rempli, afficher un message d'erreur ou gérer de manière appropriée
        print("Veuillez fournir des arguments valides.")
        return

    query_handler.display_results(results)

if __name__ == "__main__":
    main()
