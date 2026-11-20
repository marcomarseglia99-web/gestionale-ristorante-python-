# Questo file gestisce i tavoli del ristorante,
# la loro capienza e il loro stato (libero oppure occupato).

from exceptions import DatiNonValidiError, TavoloOccupatoError

LIBERO: str = "libero"
OCCUPATO: str = "occupato"

class Tavolo:
    """Rappresenta un tavolo con numero, capienza e stato."""

    def __init__(self, numero: int, posti: int) -> None:
        """Inizializza un tavolo verificando che abbia posti > 0."""
        # 1. Se il numero di posti non è positivo, solleva DatiNonValidiError con messaggio esplicativo.
        # 2. Assegna numero e posti ai relativi attributi d'istanza.
        # 3. Imposta lo stato iniziale del tavolo su libero.
        if posti <= 0:
            raise DatiNonValidiError("Il numero di posti deve essere maggiore di zero")
        
        self.numero = numero
        self.posti = posti
        self.stato = LIBERO

    @property
    def libero(self) -> bool:
        """True se il tavolo è nello stato LIBERO."""
        # 1. Verifica se lo stato corrente del tavolo corrisponde allo stato libero e restituisci il booleano.
        return self.stato == LIBERO

    def occupa(self) -> None:
        """Transiziona lo stato in OCCUPATO. Solleva TavoloOccupatoError se già occupato."""
        # 1. Verifica se il tavolo è già occupato facendo riferimento all'attributo d'istanza o alla property di stato.
        # 2. Se non è libero, solleva TavoloOccupatoError.
        # 3. Altrimenti aggiorna lo stato su occupato.
        if not self.libero:
            raise TavoloOccupatoError("Il tavolo è già occupato")
        
        self.stato = OCCUPATO

    def libera(self) -> None:
        """Reimposta lo stato in LIBERO (operazione idempotente)."""
        # 1. Reimposta lo stato su libero.
        # 2. L'operazione è idempotente: chiamarla più volte di seguito non produce anomalie.
        self.stato = LIBERO


    def __str__(self) -> str:
        """Descrizione user-friendly del tavolo."""
        # Mostra numero, capienza in posti e stato corrente
        return f"Tavolo {self.numero} ({self.posti} posti) - {self.stato}"

    def __repr__(self) -> str:
        """Rappresentazione di debug."""
        return f"Tavolo(numero={self.numero}, posti={self.posti}, stato={self.stato!r})"

if __name__ == "__main__":
    tavolo = Tavolo(1, 4)
    print(tavolo)
    tavolo.occupa()
    print("Occupato:", tavolo)
    tavolo.libera()
    print("Liberato:", tavolo)


        
