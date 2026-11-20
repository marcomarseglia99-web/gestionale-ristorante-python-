# Servizio per la gestione del menu del ristorante

from models import piatto
from models.menu import Menu
from models.piatto import Piatto

class MenuService:
    """Interfaccia operativa per il catalogo piatti del ristorante."""

    def __init__(
        self,
        piatti_iniziali: list[dict[str, str | float]] | list[tuple[str, str, float]] | None = None,
    ) -> None:
        """Inizializza il Menu interno e carica gli eventuali piatti iniziali."""

        # 1. Inizializza l'istanza del menù nel relativo attributo d'istanza protetto.
        self._menu = Menu()
        
        # 2. Se vengono forniti dati iniziali, itera sui record (estraendo nome, categoria/portata e prezzo)
        #e registrali nel menù richiamando il metodo di aggiunta.
        if piatti_iniziali is not None:
            for record in piatti_iniziali:
                if isinstance(record, dict):
                    nome = record["nome"]
                    categoria = record["portata"]
                    prezzo = record["prezzo"]
                else:
                    nome, categoria, prezzo = record

                self.aggiungi_piatto(nome, categoria, prezzo)

    def aggiungi_piatto(self, nome: str, categoria: str, prezzo: float) -> Piatto:
        """Crea un piatto con prossimo ID libero, lo registra e lo restituisce."""

        # 1. Richiedi al menù il prossimo identificativo progressivo disponibile.
        id_piatto = self._menu.prossimo_id()

        # 2. Crea la nuova istanza di Piatto con i parametri forniti.
        piatto = Piatto(id_piatto, nome, categoria, prezzo)

        # 3. Registra il piatto nel menù e restituisci l'oggetto creato.
        self._menu.aggiungi(piatto)
        return piatto

    def modifica_prezzo(self, id_piatto: int, nuovo_prezzo: float) -> Piatto:
        """Trova il piatto per ID e ne aggiorna il prezzo."""

        # 1. Individua il piatto tramite il suo ID.
        piatto = self._menu.trova(id_piatto)
        
        # 2. Aggiorna il prezzo del piatto (la validazione scatterà nella property).
        piatto.prezzo = nuovo_prezzo

        # 3. Restituisci il piatto aggiornato.
        return piatto

    def imposta_disponibilita(self, id_piatto: int, disponibile: bool) -> Piatto:
        """Trova il piatto per ID e ne modifica il flag disponibile."""

        # 1. Individua il piatto tramite il suo ID.
        piatto = self._menu.trova(id_piatto)

        # 2. Aggiorna lo stato di disponibilità del piatto.
        piatto.disponibile = disponibile

        # 3. Restituisci il piatto aggiornato.
        return piatto

    def rimuovi_piatto(self, id_piatto: int) -> Piatto:
        """Rimuove un piatto dal menù dato il suo identificativo."""

        # 1. Rimuovi il piatto delegando l'operazione al menù e restituisci il piatto rimosso.
        return self._menu.rimuovi(id_piatto)

    def trova(self, id_piatto: int) -> Piatto:
        """Trova un piatto per ID o solleva PiattoNonTrovatoError."""

        # 1. Delega la ricerca per ID al menù sottostante.
        return self._menu.trova(id_piatto)

    def elenco(self) -> list[Piatto]:
        """Restituisce la lista di tutti i piatti presenti a menù."""

        # 1. Delega al menù la restituzione di tutti i piatti.
        return self._menu.tutti()

    def per_categoria(self, categoria: str) -> list[Piatto]:
        """Filtra i piatti per categoria."""

        # 1. Delega al menù il filtro per categoria.
        return self._menu.per_categoria(categoria)

    def cerca(self, testo: str) -> list[Piatto]:
        """Cerca i piatti per sottostringa nel nome."""

        # 1. Delega al menù la ricerca per testo.
        return self._menu.cerca(testo)

if __name__ == "__main__":
    servizio_menu = MenuService([{"nome": "Pizza Margherita", "portata": "primo", "prezzo": 8.0}])
    print("Piatti caricati:", len(servizio_menu.elenco()))

    
        

