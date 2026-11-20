
# Test automatici per verificare i report delle vendite del ristorante.

import unittest

from unittest.mock import Mock

from models.piatto import Piatto
from models.tavolo import Tavolo
from models.ordine import Ordine
from services.report_service import ReportService


class TestReport(unittest.TestCase):

    def setUp(self):
        # Crea due piatti e un ordine chiuso per i test.
        tavolo = Tavolo(1, 4)

        carbonara = Piatto(1, "Carbonara", "primo", 10.50)
        acqua = Piatto(2, "Acqua", "bevanda", 2.00)

        ordine = Ordine(tavolo)
        ordine.aggiungi(carbonara, 2)
        ordine.aggiungi(acqua, 1)
        ordine.chiudi()

        # Simula lo storico degli ordini chiusi.
        ordini_service = Mock()
        ordini_service.storico = [ordine]

        self.report = ReportService(ordini_service)

    def test_incasso_totale(self):
        # Verifica l'incasso complessivo.
        self.assertEqual(self.report.incasso_totale(), 23.00)

    def test_scontrino_medio(self):
        # Verifica il valore medio degli ordini.
        self.assertEqual(self.report.scontrino_medio(), 23.00)

    def test_incasso_per_categoria(self):
        # Verifica l'incasso suddiviso per categoria.
        risultato = self.report.incasso_per_categoria()

        self.assertEqual(risultato["primo"], 21.00)
        self.assertEqual(risultato["bevanda"], 2.00)

    def test_quantita_per_piatto(self):
        # Verifica il numero di porzioni vendute.
        risultato = self.report.quantita_per_piatto()

        self.assertEqual(risultato["Carbonara"], 2)
        self.assertEqual(risultato["Acqua"], 1)

    def test_classifica_piatti(self):
        # Verifica il primo piatto nella classifica.
        risultato = self.report.classifica_piatti(1)

        self.assertEqual(risultato, [("Carbonara", 2)])

    def test_piatto_piu_venduto(self):
        # Verifica il piatto con più porzioni vendute.
        risultato = self.report.piatto_piu_venduto()

        self.assertEqual(risultato, ("Carbonara", 2))


if __name__ == "__main__":
    unittest.main()
