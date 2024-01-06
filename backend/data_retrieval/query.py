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
    parser.add_argument('-l', '--location', nargs=3, type=float, metavar=('LATITUDE', 'LONGITUDE','RADIUS'),
                        help='Filter restaurants by location. Specify latitude and longitude.')
    parser.add_argument('-m', '--max', type=float, help='max delivery price.')
    parser.add_argument('-r', '--rankBy', type=int, help='rank by price or rating.')
    
    args = parser.parse_args()

    query_handler = QueryHandler()

    if args.time and not (args.day or args.location or args.max or args.rankBy):
        results = query_handler.query_by_time(args.day, args.time)
    elif args.day and not (args.time or args.location or args.max or args.rankBy):
        # Seulement le jour est défini
        results = query_handler.query_by_day(args.day)
    elif args.location and not (args.time or args.day or args.max or args.rankBy):
        # Seulement la localisation et le rayon sont définis
        results = query_handler.query_by_location(latitude=args.location[0], longitude=args.location[1], radius=args.location[2])
    elif args.max and not (args.time or args.day or args.location, args.rankBy):
        print("APPEL DE QUERY BY PRICE")
        # Seulement le prix est défini
        results = query_handler.query_by_price(max_delivery_price=args.max)
    else:
        results = query_handler.query_combined(args.day, args.time, location=args.location, max_delivery_price=args.max, rank_by=args.rankBy)

    print("Bienvenue sur TastyTriples! \nVotre recherche vient d'être lancée")
    
    print(f"Filtres utilisés.\nTemps: {(args.time if args.time else 'Non spécifiée')}\nJour: {(args.day if args.day else 'Non spécifiée')}\nLocalisation: {(args.location if args.location else 'Non spécifiée')}\nRayon: {(args.location[2] if args.location else 'Non spécifié')}\nPrix de livraison maximum: {(args.max if args.max else 'Non spécifié')}\nrankBy: {(args.rankBy if args.rankBy else 'Non spécifié')}")


    query_handler.display_results(results)
   
    

if __name__ == "__main__":
    main()
