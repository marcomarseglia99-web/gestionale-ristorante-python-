# Servizio per la gestione dei tavoli del ristorante

from exceptions import TavoloNonTrovatoError
from models import tavolo
from models.tavolo import Tavolo

class TavoliService:
    """Gestisce la sala e lo stato di disponibilità dei tavoli."""

    def __init__(
        self,
        tavoli_iniziali: tuple[dict[str, int]] | list[dict[str, int]] | list[tuple[int, int]] | None = None,
    ) -> None:
        """Inizializza il dizionario dei tavoli e popola la sala dai dati iniziali."""
        
        # 1. Inizializza la collezione interna per memorizzare i tavoli (chiave: numero tavolo, valore: istanza Tavolo).
        self._tavoli = {}

        # 2. Itera sui dati iniziali forniti (estraendo numero e posti), istanzia ciascun Tavolo e salvalo nella collezione.
        if tavoli_iniziali is not None:
            for record in tavoli_iniziali:
                if isinstance(record, dict):
                    numero = record["numero"]
                    posti = record["posti"]
                else:
                    numero, posti = record

                tavolo = Tavolo(numero, posti)
                self._tavoli[numero] = tavolo


    def elenco(self) -> list[Tavolo]:
        """Restituisce tutti i tavoli ordinati per numero crescente."""

        # 1. Restituisci la lista di tutti i tavoli ordinati per numero progressivo.
        return sorted(self._tavoli.values(), key=lambda tavolo: tavolo.numero)


    def trova(self, numero: int) -> Tavolo:
        """Restituisce il tavolo per numero o solleva TavoloNonTrovatoError."""

        # 1. Cerca il tavolo nella collezione interna tramite il numero identificativo.
        tavolo = self._tavoli.get(numero)

        # 2. Se non presente, solleva TavoloNonTrovatoError.
        if tavolo is None:
            raise TavoloNonTrovatoError(f"Tavolo {numero} non trovato")

        return tavolo


    def liberi(self) -> list[Tavolo]:
        """Restituisce l'elenco dei soli tavoli che risultano liberi."""

        # 1. Filtra e restituisci solo i tavoli della sala che risultano attualmente liberi.
        return [tavolo for tavolo in self.elenco() if tavolo.libero]


if __name__ == "__main__":
    servizio_tavoli = TavoliService([{"numero": 1, "posti": 2}, {"numero": 2, "posti": 4}])
    print("Liberi:", [t.numero for t in servizio_tavoli.liberi()])
    