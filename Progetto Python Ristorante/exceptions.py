"""Eccezioni del dominio del ristorante."""

class RistoranteError(Exception):
    """Classe base per tutti gli errori specifici del dominio ristorante"""
    pass


class DatiNonValidiError(RistoranteError):
    """Sollevata quando un dato non rispetta i vincoli(es.prezzo <= 0, nome vuoto, posti <=0)."""
    pass


class PiattoNonTrovatoError(RistoranteError):
    """Sollevata quando si cerca un piatto con un ID non presente a menu."""

    def __init__(self, id_piatto: int) -> None:
        """Inizializza l'eccezzione salvando l'id_piatto e componendo il messaggio."""
        # 1. Salva l'id del piatto come attributo pubblico
        self.id_piatto = id_piatto

        # 2. Richiama il costruttore superiore e formatta un messaggio di feedback leggibile
        super().__init__(f"Piatto con ID{id_piatto} non trovato.")


class PiattoNonDisponibileError(RistoranteError):
    """Sollevata quando si ordina un piatto presente a menu ma non disponbile/esaurito."""
    pass


class TavoloNonTrovatoError(RistoranteError):
    """Sollevata quando si cerca un tavolo con un numero inesistente."""
    pass


class TavoloOccupatoError(RistoranteError):
    """Sollevata quando si tenta di occupare o aprire un ordine su un tavolo già occupato."""
    pass


class OrdineChiusoError(RistoranteError):
    """Sollevata quando si tenta di modificare o chiudere un ordine già saldato."""
    pass


class OrdineNonTrovatoError(RistoranteError):
    """Sollevata quando si cerca l'ordine di un tavolo che non ne ha uno aperto."""
    pass


