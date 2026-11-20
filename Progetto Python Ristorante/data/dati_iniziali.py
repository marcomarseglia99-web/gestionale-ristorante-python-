# SCOPO:
# Questo file contiene i dati iniziali del ristorante.
#
# In particolare:
# - MENU: elenco dei piatti con nome, portata e prezzo.
# - TAVOLI: elenco dei tavoli con numero e posti disponibili.
#
# I dati vengono conservati in memoria durante l'esecuzione.
# Questo file non contiene funzioni o logica di gestione.
# ============================================================

"""Dati di avvio in memoria per il ristorante."""


# Lista che conterrà i piatti iniziali del ristorante.
# Ogni piatto sarà rappresentato da un dizionario.

MENU: list[dict[str, str | float]] = [
    {"nome": "Bruschetta", "portata": "antipasto", "prezzo": 5.50},
    {"nome": "Tagliere misto", "portata": "antipasto", "prezzo": 12.00},
    {"nome": "Carbonara", "portata": "primo", "prezzo": 10.50},
    {"nome": "Lasagna", "portata": "primo", "prezzo": 11.00},
    {"nome": "Risotto ai funghi", "portata": "primo", "prezzo": 12.50},
    {"nome": "Tagliata di manzo", "portata": "secondo", "prezzo": 18.00},
    {"nome": "Cotoletta alla milanese", "portata": "secondo", "prezzo": 15.00},
    {"nome": "Tiramisù", "portata": "dolce", "prezzo": 6.00},
    {"nome": "Panna cotta", "portata": "dolce", "prezzo": 5.50},
    {"nome": "Acqua naturale", "portata": "bevanda", "prezzo": 2.00},
    {"nome": "Vino della casa", "portata": "bevanda", "prezzo": 4.50},
]


TAVOLI: tuple[dict[str, int]] = (
    {"numero": 1, "posti": 2},
    {"numero": 2, "posti": 2},
    {"numero": 3, "posti": 4},
    {"numero": 4, "posti": 4},
    {"numero": 5, "posti": 6},
)
