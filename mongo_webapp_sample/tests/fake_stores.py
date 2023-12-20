# some fake stores used for testing purposes
los_pollos_store = {
    "name": "Los Pollos Hermanos",
    "description": "Los Pollos Hermanos, where something delicious "
                   "is always cooking.",
    "location": {
        "coordinates": [-106.668038, 35.1247337]
    },
    "tags": ["restaurant", "food"]
}

olivanders_store = {
    "name": "Ollivanders Wand Shop",
    "description": "Fine Wands since 382 BC.",
    "location": {
        "coordinates": [21.2228283, 45.743279]
    }
}

wonkas_store = {
    "name": "Wonkas Chocolate Factory",
    "description": "This little piece of gum is a three-course dinner.",
    "location": {
        "coordinates": [21.2470794, 45.7536246]
    }
}

mos_eisley_store = {
    "name": "Mos Eisley Cantina",
    "description": "Tentacles, claws and hands... "
                   "wrapped around drinking utensils.",
    "location": {
        "coordinates": [21.2399956, 45.7484419]
    },
    "tags": ["restaurant", "food", "drinks"],
    "address": "Mos Eisley, Tatooine"
}

stores_dict = {
    wonkas_store['name']: wonkas_store,
    los_pollos_store['name']: los_pollos_store,
    olivanders_store['name']: olivanders_store,
    mos_eisley_store['name']: mos_eisley_store
}
