# Questo file gestisce la collezione dei piatti del ristorante,
# permettendo di aggiungere, cercare, filtrare e rimuovere i piatti dal menù.

from collections.abc import Iterator
from modulefinder import test
from operator import le
from exceptions import DatiNonValidiError, PiattoNonTrovatoError
from models.piatto import Piatto

class Menu:
    """Collezione dei piatti del ristorante indicizzati per ID."""

    def __init__(self) -> None:
        """Inizializza una collezione vuota per i piatti."""
        # 1. Inizializza un dizionario nell'attributo d'istanza protetto (chiave: ID, valore: istanza del piatto).
        self._piatti: dict[int, Piatto] = {}

        # 2. Perché è fondamentale renderlo protetto (_) anziché esporlo pubblicamente?
        # L'attributo è protetto per favorire l'incapsulamento e gestire
        # le modifiche ai piatti attraverso i metodi della classe.
        
    def aggiungi(self, piatto: Piatto) -> None:
        """Aggiunge un piatto al menù. Solleva DatiNonValidiError se l'ID esiste già."""
        # 1. Controlla se l'ID del piatto è già presente nella collezione dei piatti.
        if piatto.id in self._piatti:

            # 2. Se è già presente, solleva DatiNonValidiError.
            raise DatiNonValidiError("Esiste già un piatto con questo ID")

        # 3. Altrimenti memorizza il piatto nella collezione associandolo al suo ID.
        self._piatti[piatto.id] = piatto

    def rimuovi(self, id_piatto: int) -> Piatto:
        """Rimuove e restituisce il piatto con l'ID specificato."""
        # 1. Recupera il piatto tramite il metodo di ricerca interno (in questo modo riusi il controllo di esistenza).
        piatto = self.trova(id_piatto)

        # 2. Rimuovi l'elemento dalla collezione interna.
        del self._piatti[id_piatto]

        # 3. Restituisci il piatto appena rimosso.
        return piatto

    def trova(self, id_piatto: int) -> Piatto:
        """Cerca un piatto per ID. Solleva PiattoNonTrovatoError se assente."""
        # 1. Cerca il piatto nella collezione interna tramite il suo identificativo.
        try:
            return self._piatti[id_piatto]
        
        # 2. Se non presente, intercetta l'errore e solleva l'eccezione di dominio PiattoNonTrovatoError.
        except KeyError:
            raise PiattoNonTrovatoError("Piatto non trovato")

        # 3. Perché sollevare un'eccezione personalizzata invece di restituire semplicemente None?
        # Un'eccezione personalizzata segnala chiaramente che il piatto
        # non esiste e permette di gestire questo errore in modo specifico.

    def tutti(self) -> list[Piatto]:
        """Restituisce una copia a lista di tutti i piatti."""
        # 1. Estrai e restituisci una nuova lista contenente tutti i piatti presenti.
        return list(self._piatti.values())

        # 2. Perché restituire una copia e non esporre la collezione interna direttamente?
        # Restituire una nuova lista protegge la struttura interna del menù,
        # evitando che venga modificata direttamente dall'esterno.
        
    def per_categoria(self, categoria: str) -> list[Piatto]:
        """Restituisce la lista dei piatti filtrati per categoria (case-insensitive)."""
        # 1. Normalizza la stringa della categoria ripulendola da spazi e convertendola in minuscolo.
        categoria = categoria.strip().lower()

        # 2. Filtra e restituisci la lista dei piatti corrispondenti.
        return [piatto for piatto in self._piatti.values() if piatto.categoria == categoria]

    def disponibili(self) -> list[Piatto]:
        """Restituisce solo i piatti attualmente disponibili."""
        # 1. Filtra e restituisci solo i piatti che risultano disponibili.
        return [piatto for piatto in self._piatti.values() if piatto.disponibile]   

    def cerca(self, testo: str) -> list[Piatto]:
        """Restituisce i piatti il cui nome contiene 'testo' (case-insensitive)."""
        # 1. Normalizza il testo cercato in minuscolo.
        testo = testo.lower()

        # 2. Filtra e restituisci i piatti il cui nome contiene la porzione di testo cercata.
        return [piatto for piatto in self._piatti.values() if testo in piatto.nome.lower()]   

    def prossimo_id(self) -> int:
        """Restituisce il prossimo ID progressivo libero (max ID + 1, oppure 1 se vuoto)."""
        # 1. Calcola il massimo tra gli ID presenti maggiorato di 1.
        return max(self._piatti.keys(), default=0) + 1

        # 2. Assicurati di gestire correttamente il caso in cui la collezione sia ancora vuota.
        # Se il dizionario è vuoto, default=0 permette di restituire 1
        # come primo ID disponibile, evitando un errore di max().

    def __len__(self) -> int:
        """Numero totale di piatti nel menù."""
        # 1. Restituisci il numero totale di piatti memorizzati nella collezione interna.
        return len(self._piatti)

    def __iter__(self) -> Iterator[Piatto]:
        """Iteratore sui piatti ordinati per ID crescente."""
        # 1. Ordina i piatti per ID crescente e restituisci il relativo iteratore per consentire il ciclo for.
        return iter(self._piatti[id_piatto] for id_piatto in sorted(self._piatti)) 


if __name__ == "__main__":
    menu = Menu()
    menu.aggiungi(Piatto(1, "Margherita", "primo", 8.0))
    print("Totale piatti:", len(menu))
    print("Piatto 1:", menu.trova(1))


