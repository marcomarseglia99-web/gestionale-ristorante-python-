# Questo file gestisce il menu testuale e l'interazione con l'utente.

from typing import Callable
from cli.input_utils import (
    chiedi_conferma,
    chiedi_intero,
    chiedi_prezzo,
    chiedi_testo,
)
from exceptions import RistoranteError
from models.piatto import CATEGORIE
from services.menu_service import MenuService
from services.ordini_service import OrdiniService
from services.report_service import ReportService
from services.tavoli_service import TavoliService
from utils.formattatori import (
    formatta_classifica,
    formatta_euro,
    formatta_incassi,
    formatta_menu,
    formatta_tavoli,
    titolo,
)

class Interfaccia:
    """Menu interattivo a terminale del ristorante."""

    def __init__(
        self,
        menu_service: MenuService,
        tavoli_service: TavoliService,
        ordini_service: OrdiniService,
        report_service: ReportService,
    ) -> None:
        """Inietta i servizi applicativi."""

        # 1. Salva i quattro servizi nei relativi attributi d'istanza protetti.
        self._menu_service = menu_service
        self._tavoli_service = tavoli_service
        self._ordini_service = ordini_service
        self._report_service = report_service


    def _esegui(self, azione: Callable[[], None]) -> None:
        """Esegue un'azione catturando SOLO RistoranteError per stampare messaggi amichevoli."""

        # 1. Esegui l'azione all'interno di un blocco di protezione.
        try:
            azione ()

        # 2. Intercetta esclusivamente gli errori del dominio ristorante e mostra un messaggio amichevole all'utente.
        except RistoranteError as errore:
            print(f"Errore: {errore}")
        
        

    def _ciclo_menu(
        self,
        intestazione: str,
        voci: dict[str, tuple[str, Callable[[], None]]],
        etichetta_zero: str,
    ) -> None:
        """Visualizza un menu da un dizionario scelta -> (descrizione, callback) e smista la chiamata."""
        
        # 1. Avvia il ciclo del menu.
        while True:
            # 2. Mostra l'intestazione formattata e l'elenco delle opzioni con le descrizioni, includendo l'opzione di uscita con etichetta_zero.
            print(titolo(intestazione))
            for scelta, (descrizione, _) in voci.items():
                print(f"{scelta}. {descrizione}")
            print(f"0. {etichetta_zero}")
            # 3. Acquisisci la scelta dell'utente.
            scelta = input("Scegli un'opzione: ").strip()
            # 4. Se l'utente seleziona "0", esci dal ciclo del menu corrente.
            if scelta == "0":
                break
            # 5. Se la scelta non appartiene alle voci previste, avvisa l'utente e richiedi nuovamente.
            if scelta not in voci:
                print("Opzione non valida.")
                continue
            # 6. Altrimenti esegui in modo protetto la funzione associata alla voce selezionata.
            self._esegui(voci[scelta][1])

    def avvia(self) -> None:
        """Avvia il menu principale dell'applicazione gestendo l'uscita pulita con Ctrl+C / Ctrl+D."""
        # 1. Configura le voci del menu principale collegandole ai rispettivi sottomenu:
        # Menù, Tavoli, Ordini e Report.
        voci = {
            "1": ("Menù", self._menu_piatti),
            "2": ("Tavoli", self._menu_tavoli),
            "3": ("Ordini", self._menu_ordini),
            "4": ("Report", self._menu_report),
        }
        # 2. Avvia il ciclo del menu gestendo l'interruzione da tastiera per un'uscita pulita senza messaggi anomali.
        try:
            self._ciclo_menu("MENU PRINCIPALE", voci, "Esci")
        except (KeyboardInterrupt, EOFError):
            pass
              
        # 3. Mostra un messaggio di saluto all'uscita.
        print("Arrivederci!")



    # ==================================================================
    # SEZIONE MENÙ
    # ==================================================================
    def _menu_piatti(self) -> None:
        # 1. Configura le voci del sottomenu piatti e avvia il relativo ciclo di menu.
        voci = {
            "1": ("Mostra menù", self._mostra_menu),
            "2": ("Mostra per categoria", self._mostra_per_categoria),
            "3": ("Cerca piatto", self._cerca_piatto),
            "4": ("Aggiungi piatto", self._aggiungi_piatto),
            "5": ("Modifica prezzo", self._modifica_prezzo),
            "6": ("Cambia disponibilità", self._cambia_disponibilita),
            "7": ("Rimuovi piatto", self._rimuovi_piatto),
        }
        self._ciclo_menu("MENÙ PIATTI", voci, "Torna indietro")

    def _mostra_menu(self) -> None:
        # 1. Recupera tutti i piatti dal servizio menù e mostrali formattati a video.
        piatti = self._menu_service.elenco()
        print(formatta_menu(piatti))

    def _mostra_per_categoria(self) -> None:
        # 1. Mostra all'utente le categorie disponibili.
        print("Categorie disponibili:")
        for categoria in CATEGORIE:
            print(categoria)
        # 2. Acquisisci la categoria desiderata.
        categoria = chiedi_testo("Inserisci la categoria: ")
        # 3. Recupera i piatti filtrati dal servizio menù e mostrali a video formattati.
        piatti = self._menu_service.per_categoria(categoria)
        print(formatta_menu(piatti))

    def _cerca_piatto(self) -> None:
        # 1. Acquisisci il testo da cercare.
        testo = chiedi_testo("Inserisci il nome del piatto da cercare: ")
        # 2. Cerca i piatti tramite il servizio menù e mostrali a video formattati.
        piatti = self._menu_service.cerca(testo)
        print(formatta_menu(piatti))

    def _aggiungi_piatto(self) -> None:
        # 1. Acquisisci nome, categoria e prezzo del piatto usando le apposite funzioni di input.
        nome = chiedi_testo("Inserisci il nome del piatto: ")
        categoria = chiedi_testo("Inserisci la categoria: ")
        prezzo = chiedi_prezzo("Inserisci il prezzo: ")
        # 2. Richiedi al servizio menù di aggiungere il piatto con i dati raccolti.
        piatto = self._menu_service.aggiungi_piatto(nome, categoria, prezzo)
        # 3. Mostra un messaggio di conferma con il piatto appena creato.
        print(f"Piatto aggiunto: {piatto}")

    def _modifica_prezzo(self) -> None:
        # 1. Acquisisci l'identificativo del piatto e il nuovo prezzo.
        id_piatto = chiedi_intero("Inserisci l'ID del piatto: ", minimo=1)
        nuovo_prezzo = chiedi_prezzo("Inserisci il nuovo prezzo: ")
        # 2. Richiedi al servizio menù di aggiornare il prezzo e mostra il piatto aggiornato.
        piatto = self._menu_service.modifica_prezzo(id_piatto, nuovo_prezzo)
        print(f"Piatto aggiornato: {piatto}")

    def _cambia_disponibilita(self) -> None:
        # 1. Acquisisci l'identificativo del piatto e la nuova disponibilità.
        id_piatto = chiedi_intero("Inserisci l'ID del piatto: ", minimo=1)
        disponibile = chiedi_conferma("Il piatto è disponibile? (s/n): ")
        # 2. Richiedi al servizio menù di aggiornare la disponibilità e mostra la conferma.
        piatto = self._menu_service.imposta_disponibilita(id_piatto, disponibile)
        print(f"Disponibilità aggiornata: {piatto}")

    def _rimuovi_piatto(self) -> None:
        # 1. Acquisisci l'identificativo del piatto e chiedi conferma dell'operazione.
        id_piatto = chiedi_intero("Inserisci l'ID del piatto da rimuovere: ", minimo=1)
        conferma = chiedi_conferma("Confermi la rimozione del piatto? (s/n): ")
        # 2. Se confermato, richiedi al servizio menù la rimozione e mostra un messaggio di avvenuta cancellazione.
        if conferma:
            self._menu_service.rimuovi_piatto(id_piatto)
            print("Piatto rimosso correttamente.")

    # ==================================================================
    # SEZIONE TAVOLI
    # ==================================================================

    def _menu_tavoli(self) -> None:
        # 1. Configura le voci per il sottomenu tavoli e avvia il relativo ciclo di menu.
        voci = {
            "1": ("Mostra tavoli", self._mostra_tavoli),
            "2": ("Mostra tavoli liberi", self._mostra_tavoli_liberi),
        }
        self._ciclo_menu("MENÙ TAVOLI", voci, "Torna indietro")

    def _mostra_tavoli(self) -> None:
        # 1. Recupera tutti i tavoli dal servizio tavoli e mostrali a video formattati.
        tavoli = self._tavoli_service.elenco()
        print(formatta_tavoli(tavoli))

    def _mostra_tavoli_liberi(self) -> None:
        # 1. Recupera solo i tavoli liberi dal servizio tavoli e mostrali a video formattati.
        tavoli = self._tavoli_service.liberi()
        print(formatta_tavoli(tavoli))

    # ==================================================================
    # SEZIONE ORDINI
    # ==================================================================
    def _menu_ordini(self) -> None:
        # 1. Configura le voci per il sottomenu ordini e avvia il relativo ciclo di menu.
        voci = {
            "1": ("Apri ordine", self._apri_ordine),
            "2": ("Aggiungi piatto all'ordine", self._aggiungi_a_ordine),
            "3": ("Togli piatto dall'ordine", self._togli_da_ordine),
            "4": ("Vedi conto", self._vedi_conto),
            "5": ("Chiudi ordine", self._chiudi_ordine),
            "6": ("Mostra ordini aperti", self._mostra_ordini_aperti),
        }
        self._ciclo_menu("MENÙ ORDINI", voci, "Torna indietro")

    def _apri_ordine(self) -> None:
        # 1. Acquisisci il numero del tavolo.
        numero_tavolo = chiedi_intero("Inserisci il numero del tavolo: ", minimo=1)

        # 2. Richiedi al servizio ordini di aprire un ordine per quel tavolo e mostra conferma.
        ordine = self._ordini_service.apri_ordine(numero_tavolo)
        print(f"Ordine aperto per il tavolo {numero_tavolo}.")

    def _aggiungi_a_ordine(self) -> None:
        # 1. Acquisisci il numero del tavolo e mostra il menù per facilitare la scelta.
        numero_tavolo = chiedi_intero("Inserisci il numero del tavolo: ", minimo=1)
        piatti = self._menu_service.elenco()
        print(formatta_menu(piatti))

        # 2. Acquisisci l'identificativo del piatto e la quantità desiderata.
        id_piatto = chiedi_intero("Inserisci l'ID del piatto: ", minimo=1)
        quantita = chiedi_intero("Inserisci la quantità: ", minimo=1)

        # 3. Aggiungi il piatto all'ordine tramite il servizio ordini e mostra il totale parziale formattato.
        ordine = self._ordini_service.aggiungi_piatto(numero_tavolo, id_piatto, quantita)
        print(f"Totale parziale: {formatta_euro(ordine.totale)}")

    def _togli_da_ordine(self) -> None:
        # 1. Acquisisci il numero del tavolo, l'identificativo del piatto e quante porzioni togliere (indicando che 0 rimuove tutto).
        numero_tavolo = chiedi_intero("Inserisci il numero del tavolo: ", minimo=1)
        id_piatto = chiedi_intero("Inserisci l'ID del piatto: ", minimo=1)
        quantita = chiedi_intero("Quante porzioni vuoi togliere? (0 per tutte): ", minimo=0)

        # 2. Se l'utente indica 0 imposta la rimozione totale, altrimenti passa la quantità specificata.
        quantita_da_togliere = None if quantita == 0 else quantita
        
        # 3. Richiedi la rimozione al servizio ordini e mostra il totale parziale aggiornato.
        ordine = self._ordini_service.rimuovi_piatto(numero_tavolo, id_piatto, quantita_da_togliere)
        print(f"Totale parziale aggiornato: {formatta_euro(ordine.totale)}")

    def _vedi_conto(self) -> None:
        # 1. Acquisisci il numero del tavolo.
        numero_tavolo = chiedi_intero("Inserisci il numero del tavolo: ", minimo=1)

        # 2. Recupera l'ordine aperto del tavolo dal servizio ordini e stampalo a video.
        ordine = self._ordini_service.ordine_aperto(numero_tavolo)
        print(ordine)

    def _chiudi_ordine(self) -> None:
        # 1. Acquisisci il numero del tavolo e mostra lo scontrino corrente.
        numero_tavolo = chiedi_intero("Inserisci il numero del tavolo: ", minimo=1)
        ordine = self._ordini_service.ordine_aperto(numero_tavolo)
        print(ordine)

        # 2. Chiedi conferma all'utente per procedere con la chiusura e il pagamento.
        conferma = chiedi_conferma("Confermi la chiusura e il pagamento dell'ordine? (s/n): ")

        # 3. Se confermato, chiudi l'ordine tramite il servizio ordini e mostra il totale incassato e la liberazione del tavolo.
        if conferma:
            ordine = self._ordini_service.chiudi_ordine(numero_tavolo)
            print(f"Totale incassato: {formatta_euro(ordine.totale)}")
            print(f"Tavolo {numero_tavolo} liberato.")

    def _mostra_ordini_aperti(self) -> None:
        # 1. Recupera la lista degli ordini aperti dal servizio ordini.
        ordini = self._ordini_service.ordini_aperti()

        # 2. Se non vi sono ordini aperti mostra un avviso, altrimenti stampa ciascun ordine.
        if not ordini:
            print("Non ci sono ordini aperti.")
        else:
            for ordine in ordini:
                print(ordine)


    # ==================================================================
    # SEZIONE REPORT
    # ==================================================================
    def _menu_report(self) -> None:
        # 1. Configura le voci del sottomenu report e avvia il relativo ciclo di menu.
        voci = {
            "1": ("Incasso totale", self._report_incasso),
            "2": ("Incassi per categoria", self._report_categorie),
            "3": ("Classifica piatti", self._report_classifica),
            "4": ("Scontrino medio", self._report_medio),
        }
        self._ciclo_menu("MENÙ REPORT", voci, "Torna indietro")

    def _report_incasso(self) -> None:
        # 1. Recupera l'incasso totale dal servizio report e stampalo formattato in euro.
        incasso = self._report_service.incasso_totale()
        print(f"Incasso totale: {formatta_euro(incasso)}")

    def _report_categorie(self) -> None:
        # 1. Recupera gli incassi per categoria dal servizio report e stampali formattati a video.
        incassi = self._report_service.incasso_per_categoria()
        print(formatta_incassi(incassi))

    def _report_classifica(self) -> None:
        # 1. Recupera la classifica dei primi 3 piatti dal servizio report e stampala formattata a video.
        classifica = self._report_service.classifica_piatti(3)
        print(formatta_classifica(classifica))

    def _report_medio(self) -> None:
        # 1. Recupera lo scontrino medio dal servizio report e stampalo formattato in euro.
        media = self._report_service.scontrino_medio()
        print(f"Scontrino medio: {formatta_euro(media)}")