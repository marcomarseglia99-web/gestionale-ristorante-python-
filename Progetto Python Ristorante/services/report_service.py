# Questo file gestisce i report e le statistiche del ristorante utilizzando lo storico degli ordini.

from models.ordine import Ordine
from services.ordini_service import OrdiniService

class ReportService:
    """Statistiche aggregate e report di vendita del ristorante."""

    def __init__(self, ordini_service: OrdiniService) -> None:
        """Inizializza il servizio memorizzando il riferimento al servizio ordini."""

        # 1. Salva il riferimento al servizio ordini nell'apposito attributo d'istanza.
        self._ordini_service = ordini_service

    def _ordini(self) -> list[Ordine]:
        """Restituisce lo storico aggiornato degli ordini chiusi."""

        # 1. Recupera la lista aggiornata degli ordini chiusi interrogando il servizio ordini.
        return self._ordini_service.storico

    def incasso_totale(self) -> float:
        """Somma i totali di tutti gli ordini chiusi."""

        # 1. Calcola la somma dei totali di tutti gli ordini chiusi e arrotonda a due decimali il risultato.
        return round(sum(ordine.totale for ordine in self._ordini()), 2)

    def scontrino_medio(self) -> float:
        """Importo medio per ordine chiuso (0.0 se non ci sono ordini nello storico)."""
        
        # 1. Recupera gli ordini chiusi dallo storico.
        ordini = self._ordini()

        # 2. Se non ci sono ordini, restituisci 0.0 per evitare la divisione per zero.
        if not ordini:
            return 0.0

        # 3. Altrimenti calcola l'incasso totale diviso per il numero di ordini e arrotonda a due decimali il risultato.
        return round(self.incasso_totale() / len(ordini), 2)

    def incasso_per_categoria(self) -> dict[str, float]:
        """Dizionario categoria -> totale incassato, ordinato in modo decrescente."""

        # 1. Inizializza una struttura per accumulare gli incassi raggruppati per categoria.
        incassi = {}

        # 2. Itera su ciascun ordine chiuso e sulle relative righe, accumulando i subtotali nella rispettiva categoria.
        for ordine in self._ordini():
            for riga in ordine.righe:
                categoria = riga.piatto.categoria
                incassi[categoria] = incassi.get(categoria, 0) + riga.subtotale
        
        # 3. Ordina le categorie per incasso decrescente.
        incassi_ordinati = sorted(incassi.items(), key=lambda elemento: elemento[1], reverse=True)

        # 4. Restituisci il dizionario con gli importi arrotondati a due decimali.
        return {categoria: round(totale, 2) for categoria, totale in incassi_ordinati}

    def quantita_per_piatto(self) -> dict[str, int]:
        """Dizionario nome_piatto -> totale porzioni vendute."""
        
        # 1. Inizializza una struttura per conteggiare le porzioni vendute per ciascun piatto.
        quantita = {}
        
        # 2. Itera su tutti gli ordini chiusi e sulle rispettive righe, sommando le quantità per ciascun nome di piatto.
        for ordine in self._ordini():
            for riga in ordine.righe:
                nome = riga.piatto.nome
                quantita[nome] = quantita.get(nome, 0) + riga.quantita

        # 3. Restituisci il dizionario delle quantità vendute.
        return quantita

    def classifica_piatti(self, n: int = 3) -> list[tuple[str, int]]:
        """Restituisce le prime n posizioni di (nome_piatto, porzioni_vendute)."""

        # 1. Ottieni il conteggio delle porzioni vendute per piatto.
        quantita = self.quantita_per_piatto()
        
        # 2. Ordina gli elementi per quantità venduta decrescente.
        classifica = sorted(quantita.items(), key=lambda elemento: elemento[1], reverse=True)

        # 3. Estrai e restituisci i primi n elementi.
        return classifica[:n]

    def piatto_piu_venduto(self) -> tuple[str, int] | None:
        """Restituisce la tupla del piatto più venduto, o None se non ci sono vendite."""

        # 1. Richiedi la classifica per il primo elemento.
        classifica = self.classifica_piatti(1)

        # 2. Se la classifica non è vuota restituisci il primo elemento, altrimenti restituisci None.
        if classifica:
            return classifica[0]
        return None

    