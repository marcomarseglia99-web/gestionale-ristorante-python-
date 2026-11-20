# Servizio per la gestione degli ordini del ristorante

from exceptions import OrdineNonTrovatoError, PiattoNonDisponibileError
from models import tavolo
from models import ordine
from models.ordine import Ordine
from models.piatto import Piatto
from models.tavolo import Tavolo
from services.menu_service import MenuService
from services.tavoli_service import TavoliService

class OrdiniService:
    """Gestisce l'apertura, l'aggiornamento e la chiusura degli ordini sui tavoli."""

    def __init__(self, menu_service: MenuService, tavoli_service: TavoliService) -> None:
        """Riceve i servizi dipendenti e inizializza il registro ordini aperti e lo storico."""

        # 1. Memorizza i riferimenti ai servizi collaboratori nei relativi attributi d'istanza.
        self._menu_service = menu_service
        self._tavoli_service = tavoli_service

        # 2. Inizializza la collezione per tracciare gli ordini attualmente in corso (chiave: numero del tavolo).
        self._ordini_aperti = {}       

       # 3. Inizializza la collezione per conservare lo storico degli ordini chiusi.
        self._storico_ordini = []

        # 4. Perché ricevere i servizi come parametri (Dependency Injection) invece di crearli dentro la classe?
        # Risposta: Per utilizzare servizi già creati, rendendo il codice più organizzato,
        # riutilizzabile e facile da modificare e testare.

    
    def apri_ordine(self, numero_tavolo: int) -> Ordine:
        """Occupa il tavolo e apre un nuovo ordine associato."""

        # 1. Recupera il tavolo tramite il servizio tavoli.
        tavolo = self._tavoli_service.trova(numero_tavolo)

        # 2. Occupa il tavolo PRIMA di creare l'ordine.
        #    Se il tavolo è già occupato, solleverà l'errore bloccando l'operazione in modo atomico.
        tavolo.occupa()

        # 3. Crea il nuovo ordine per quel tavolo.
        ordine = Ordine(tavolo)

        # 4. Registra l'ordine tra quelli aperti e restituiscilo.
        self._ordini_aperti[numero_tavolo] = ordine
        return ordine


    def ordine_aperto(self, numero_tavolo: int) -> Ordine:
        """Restituisce l'ordine aperto per il tavolo indicato o solleva OrdineNonTrovatoError."""

        # 1. Cerca l'ordine corrispondente al numero del tavolo tra quelli aperti.
        ordine = self._ordini_aperti.get(numero_tavolo)

        # 2. Se non presente, solleva OrdineNonTrovatoError.
        if ordine is None:
            raise OrdineNonTrovatoError(f"Nessun ordine aperto per il tavolo {numero_tavolo}")

        return ordine


    def aggiungi_piatto(
        self,
        numero_tavolo: int,
        id_piatto: int,
        quantita: int = 1,
    ) -> Ordine:
        """Aggiunge un piatto all'ordine se esiste ed è disponibile."""

        # 1. Recupera l'ordine aperto del tavolo indicato.
        ordine = self.ordine_aperto(numero_tavolo)

        # 2. Recupera il piatto dal servizio menù tramite l'ID.
        piatto = self._menu_service.trova(id_piatto)

        # 3. Controlla che il piatto sia disponibile; se non lo è, solleva PiattoNonDisponibileError.
        if not piatto.disponibile:
            raise PiattoNonDisponibileError(f"Il piatto {piatto.nome} non è disponibile")
       
       # 4. Aggiungi il piatto all'ordine e restituisci l'ordine aggiornato.
        ordine.aggiungi(piatto, quantita)
        return ordine


    def rimuovi_piatto(
        self,
        numero_tavolo: int,
        id_piatto: int,
        quantita: int | None = None,
    ) -> Ordine:
        """Rimuove porzioni o l'intero piatto dall'ordine."""

        # 1. Recupera l'ordine aperto del tavolo indicato.
        ordine = self.ordine_aperto(numero_tavolo)

        # 2. Rimuovi il piatto dall'ordine e restituisci l'ordine aggiornato.
        ordine.rimuovi(id_piatto, quantita)
        return ordine


    def chiudi_ordine(self, numero_tavolo: int) -> Ordine:
        """Chiude l'ordine, libera il tavolo, lo rimuove dagli aperti e lo archivia nello storico."""

        # 1. Recupera l'ordine aperto del tavolo indicato.
        ordine = self.ordine_aperto(numero_tavolo)
        
        # 2. Chiudi l'ordine (se l'ordine è vuoto solleverà eccezione e il tavolo rimarrà occupato).
        ordine.chiudi()
        
        # 3. Libera il tavolo associato all'ordine.
        ordine.tavolo.libera()

        # 4. Rimuovi l'ordine da quelli aperti.
        del self._ordini_aperti[numero_tavolo]

        # 5. Archivia l'ordine nello storico e restituiscilo.
        self._storico_ordini.append(ordine)
        return ordine

    @property
    def storico(self) -> list[Ordine]:
        """Restituisce una copia della lista degli ordini chiusi."""

        # 1. Restituisci una copia della lista dello storico per proteggere la collezione interna.
        return self._storico_ordini.copy()

    def ordini_aperti(self) -> list[Ordine]:
        """Restituisce la lista di tutti gli ordini aperti al momento."""

        # 1. Restituisci la lista di tutti gli ordini attualmente in corso.
        return list(self._ordini_aperti.values())