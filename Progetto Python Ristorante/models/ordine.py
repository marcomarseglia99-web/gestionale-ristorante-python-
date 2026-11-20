# Questo file gestisce gli ordini del ristorante e le relative righe.
# Memorizza i prezzi al momento dell'ordine e impedisce modifiche agli ordini chiusi.

from exceptions import DatiNonValidiError, OrdineChiusoError, PiattoNonTrovatoError
from models.piatto import Piatto
from models.tavolo import Tavolo

APERTO: str = "aperto"
CHIUSO: str = "chiuso"

class RigaOrdine:
    """Una riga dello scontrino: conserva piatto, quantità e prezzo congelato."""

    def __init__(self, piatto: Piatto, quantita: int) -> None:
        """Memorizza il piatto, la quantità e congela piatto.prezzo."""
        # 1. Assegna il piatto e la quantità ai rispettivi attributi d'istanza.
        self.piatto = piatto
        self.quantita = quantita
        
        # 2. Salva il prezzo unitario del piatto in un apposito attributo d'istanza.
        self.prezzo_unitario = piatto.prezzo
        
        # 3. Perché è fondamentale "congelare" il prezzo al momento dell'ordine anziché leggerlo sempre dal piatto?
      
    @property
    def subtotale(self) -> float:
        """Calcola prezzo_unitario * quantita arrotondato a 2 decimali."""
        # 1. Calcola il prezzo unitario moltiplicato per la quantità e arrotonda a due decimali il risultato.
        return round(self.prezzo_unitario * self.quantita, 2)


class Ordine:
    """Gestisce le righe d'ordine associate a un tavolo."""

    def __init__(self, tavolo: Tavolo) -> None:
        """Inizializza un ordine per il tavolo specificato in stato APERTO."""
        # 1. Salva il tavolo di riferimento nel relativo attributo d'istanza.
        self.tavolo = tavolo

        # 2. Inizializza la collezione delle righe d'ordine come lista vuota.
        self.righe: list[RigaOrdine] = []

        # 3. Imposta lo stato iniziale dell'ordine su aperto.
        self.stato = APERTO

    def _verifica_modificabile(self) -> None:
        """Solleva OrdineChiusoError se lo stato dell'ordine è CHIUSO."""
        # 1. Controlla lo stato dell'ordine: se è chiuso, solleva OrdineChiusoError.
        # 2. Perché centralizzare questo controllo in un metodo protetto con prefisso underscore (_)?
        if self.stato == CHIUSO:
            raise OrdineChiusoError("Non è possibile modificare un ordine chiuso")

    def _trova_riga(self, id_piatto: int) -> RigaOrdine | None:
        """Cerca una riga con il piatto specificato per ID, oppure restituisce None."""
        # 1. Itera sulle righe dell'ordine presenti nella collezione d'istanza.
        # 2. Se trovi una riga con il piatto avente l'ID richiesto, restituiscila.
        # 3. Se la ricerca termina senza riscontri, restituisci None.
        for riga in self.righe:
            if riga.piatto.id == id_piatto:
                return riga

        return None

    def aggiungi(self, piatto: Piatto, quantita: int = 1) -> None:
        """Aggiunge una quantità di un piatto (se presente incrementa, altrimenti crea nuova riga)."""
        # 1. Verifica che l'ordine sia modificabile chiamando il controllo dedicato.
        self._verifica_modificabile()
        
        # 2. Valida la quantità: se non è positiva, solleva DatiNonValidiError.
        if quantita <= 0:
            raise DatiNonValidiError("La quantita deve essere maggiore di zero")

        # 3. Cerca se il piatto è già presente tra le righe dell'ordine.
        riga = self._trova_riga(piatto.id)

        # 4. Se la riga esiste già incrementa la quantità, altrimenti crea una nuova riga d'ordine e aggiungila alla collezione.
        if riga is not None:
            riga.quantita += quantita

        else:
            self.righe.append(RigaOrdine(piatto, quantita))

    def rimuovi(self, id_piatto: int, quantita: int | None = None) -> None:
        """Rimuove porzioni o l'intera riga di un piatto dall'ordine."""
        # 1. Verifica che l'ordine sia modificabile.
        self._verifica_modificabile()
        
        # 2. Cerca la riga corrispondente all'ID del piatto; se non presente, solleva PiattoNonTrovatoError.
        riga = self._trova_riga(id_piatto)
        if riga is None:
            raise PiattoNonTrovatoError(f"Piatto con ID {id_piatto} non trovato nell'ordine")
        
        # 3. Se la quantità da togliere non è indicata oppure supera o eguaglia le porzioni presenti, rimuovi l'intera riga.
        if quantita is None or quantita >= riga.quantita:
            self.righe.remove(riga)
            return

        # 4. Se la quantità da togliere è minore o uguale a zero, solleva DatiNonValidiError.
        if quantita <= 0:
            raise DatiNonValidiError("La quantita da rimuovere deve essere maggiore di zero")
        
        # 5. Negli altri casi decrementa la quantità della riga.
        riga.quantita -= quantita

    @property
    def totale(self) -> float:
        """Calcola la somma monetaria di tutti i subtotali delle righe."""
        # 1. Calcola la somma dei subtotali di ogni riga presente e arrotonda a due decimali il risultato.
        return round(sum(riga.subtotale for riga in self.righe), 2)

    def chiudi(self) -> None:
        """Chiude l'ordine. Solleva eccezioni se già chiuso o se privo di righe."""
        # 1. Verifica che l'ordine sia modificabile.
        self._verifica_modificabile()
        # 2. Se l'ordine non ha alcuna riga, solleva DatiNonValidiError (non è consentito chiudere un ordine vuoto).
        if not self.righe:
            raise DatiNonValidiError("Non è possibile chiudee un ordine vuoto")

        # 3. Aggiorna lo stato dell'ordine su chiuso.
        self.stato = CHIUSO

    def __str__(self) -> str:
        """Genera lo scontrino testuale dell'ordine con tutte le voci e il totale finale."""
        # Intestazione con identificativo tavolo e stato dell'ordine
        linee: list[str] = [f"--- Tavolo {self.tavolo.numero} ({self.stato}) ---"]
        # Per ogni riga d'ordine: quantità allineata a destra, nome piatto a sinistra, subtotale
        for riga in self.righe:
            linee.append(
                f"{riga.quantita:>2} x {riga.piatto.nome:<24} {riga.subtotale:>8.2f} €"
            )

        # Linea divisoria di 40 trattini
        linee.append("-" * 40)
        # Riga finale del totale complessivo
        linee.append(f"{'TOTALE':<29} {self.totale:>8.2f} €")
        return "\n".join(linee)

if __name__ == "__main__":
    tavolo = Tavolo(1, 4)
    ordine = Ordine(tavolo)
    piatto = Piatto(1, "Carbonara", "primo", 10.5)
    ordine.aggiungi(piatto, 2)
    print(ordine)

        


            

