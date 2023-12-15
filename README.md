# TastyTriples

TastyTriples est un projet académique qui explore les technologies du web sémantique dans le domaine de la livraison de nourriture. Dans une ère dominée par l'interconnectivité des données, notre projet utilise les Linked Data, JSON-LD, et SPARQL pour créer un service de découverte de livraison de nourriture.

## Fonctionnalités

- Découverte de restaurants qui utilisent la livraison à vélo.
- Prise en compte des préférences des clients.
- Modélisation des commandes et stockage dans notre espace de données. Nous avons une base de données avec les restaurants et les descriptions des services, et une autre base de données avec les préférences des clients où nous stockons les commandes.
- Les commandes ne sont pas saisies directement, mais par un algorithme de décision qui prend en compte les préférences de nos clients. Vous pouvez avoir une liste de restaurants préférés, une préférence pour les restaurants les plus proches, et une préférence pour les restaurants les moins chers. Les combinaisons de préférences sont possibles.

## Travail en cours

Aujourd'hui, notre point de départ est d'examiner la description des services de CoopCycle. Notre premier objectif est d'obtenir les données de la fédération CoopServices, de les traduire en RDF en utilisant schema.org, et de mettre les données résultantes dans des triplestores.

Astuce : utilisez la carte pour obtenir des données.

## Architecture du projet

Le projet est divisé en deux parties principales : la récupération des données et l'interface web (frontend et backend). Le backend est écrit en Python et le frontend utilise un framework JavaScript. Pour plus de détails sur l'architecture du projet, veuillez consulter la structure du dossier dans le dépôt.

```
TastyTriples/
    backend/
        data_retrieval/
            coopcycle.json
            htmlParser.py
            json_ld_output_13-l-adresse.json
            json_ld_output_15-cafe-litha.json
            json_ld_output_18-au-passage.json
            json_ld_output_21-robin-room.json
            json_ld_output_22-moana-poke.json
            json_ld_output_23-la-manufacture.json
            json_ld_output_28-la-mamma-mia.json
            json_ld_output_30-mealk.json
            json_ld_output_30-you-beauty.json
            json_ld_output_31-via-pizza.json
            json_ld_output_34-chez-rosa.json
            json_ld_output_35-le-teuf.json
            ...
        api/
            api.py
            models/
                restaurant.py
                menu.py
                ...
            services/
                triplestore_service.py
                ...
    frontend/
        js/
            components/
                restaurant_list.js
                restaurant_detail.js
                ...
            services/
                api_service.js
                ...
        css/
            main.css
            ...
        index.html
    README.md
```