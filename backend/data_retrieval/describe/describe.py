from preferencesCreator import PreferencesCreator
from colorama import Fore, Style
from data_retrieval.collect.fusekiLoader import FusekiLoader

def main():
    print(Fore.GREEN +"Creation des preferences utilisateur"+ Style.RESET_ALL)
    name = input("Entrez votre nom : ")
    postal_code = input("Entrez votre code postal : ")
    locality = input("Entrez votre ville : ")
    latitude = input("Entrez la latitude : ")
    longitude = input("Entrez la longitude : ")
    radius = input("Entrez le rayon de recherche : ")
    max_price = input("Entrez le prix maximum : ")
    currency = input("Entrez la devise : ")
    seller_uri = input("Entrez l'URI du restaurant : ")
    preferences_creator= PreferencesCreator()
    preferences_file_path = preferences_creator.add_person_preferences(name, postal_code, locality, seller_uri, max_price, currency, latitude, longitude, radius)
    #preferences_creator.add_person_preferences("Meziane", "42000", "Saint-Etienne", "https://coursiers-stephanois.coopcycle.org/api/restaurants/24", 4.5, "EUR", 5.03942, 47.3238, 10.0)
    fusekiLoader = FusekiLoader('http://localhost:3030/Coopcycle')
    fusekiLoader.load_data_from_file(preferences_file_path)
if __name__ == "__main__":
    main()