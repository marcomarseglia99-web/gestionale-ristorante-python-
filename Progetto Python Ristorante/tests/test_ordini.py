
# Test automatici per verificare il funzionamento degli ordini.

import unittest

from models.piatto import Piatto
from models.tavolo import Tavolo
from models.ordine import Ordine
from exceptions import DatiNonValidiError, OrdineChiusoError


class TestOrdine(unittest.TestCase):

    def test_creazione_ordine(self):
        # Verifica che un nuovo ordine sia aperto e abbia totale zero.
        tavolo = Tavolo(1, 4)
        ordine = Ordine(tavolo)

        self.assertEqual(ordine.stato, "aperto")
        self.assertEqual(ordine.totale, 0)

    def test_aggiunta_piatto(self):
        # Verifica l'aggiunta di due porzioni di un piatto.
        tavolo = Tavolo(1, 4)
        ordine = Ordine(tavolo)
        piatto = Piatto(1, "Carbonara", "primo", 10.50)

        ordine.aggiungi(piatto, 2)

        self.assertEqual(ordine.totale, 21.00)

    def test_rimozione_piatto(self):
        # Verifica la rimozione di un piatto dall'ordine.
        tavolo = Tavolo(1, 4)
        ordine = Ordine(tavolo)
        piatto = Piatto(1, "Carbonara", "primo", 10.50)

        ordine.aggiungi(piatto, 2)
        ordine.rimuovi(1)

        self.assertEqual(ordine.totale, 0)

    def test_chiusura_ordine(self):
        # Verifica che un ordine con un piatto possa essere chiuso.
        tavolo = Tavolo(1, 4)
        ordine = Ordine(tavolo)
        piatto = Piatto(1, "Carbonara", "primo", 10.50)

        ordine.aggiungi(piatto, 1)
        ordine.chiudi()

        self.assertEqual(ordine.stato, "chiuso")

    def test_ordine_vuoto(self):
        # Verifica che non sia possibile chiudere un ordine vuoto.
        tavolo = Tavolo(1, 4)
        ordine = Ordine(tavolo)

        with self.assertRaises(DatiNonValidiError):
            ordine.chiudi()

    def test_modifica_ordine_chiuso(self):
        # Verifica che un ordine chiuso non possa essere modificato.
        tavolo = Tavolo(1, 4)
        ordine = Ordine(tavolo)
        piatto = Piatto(1, "Carbonara", "primo", 10.50)

        ordine.aggiungi(piatto, 1)
        ordine.chiudi()

        with self.assertRaises(OrdineChiusoError):
            ordine.aggiungi(piatto, 1)


if __name__ == "__main__":
    unittest.main()
