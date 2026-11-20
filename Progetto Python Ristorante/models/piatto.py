# SCOPO:
# Questo file definisce le classi Piatto e Bevanda.
#
# In particolare:
# - Piatto: rappresenta un piatto del menu.
# - Bevanda: rappresenta una bevanda del ristorante.
# - Controlla che nome, categoria e prezzo siano validi.
# - Gestisce la disponibilita dei piatti.
#
# Utilizzeremo classi, ereditarieta e property.

from typing import Literal, get_args

from exceptions import DatiNonValidiError

Categoria = Literal["antipasto", "primo", "secondo", "dolce", "bevanda"]
CATEGORIE: tuple[str, ...] = get_args(Categoria)

class Piatto:
    """Rappresenta un piatto del menù con validazione interna dei campi."""

    def __init__(
        self,
        id_piatto: int,
        nome: str,
        categoria: Categoria,
        prezzo: float,
        disponibile: bool = True,
    ) -> None:
        """Inizializza un piatto assegnando i campi attraverso le relative property."""
        # crea attributo di istanza id del tipo 001 (come gestisci il contatore?) usa il metodo zfill() delle stringhe
        self.id = id_piatto

        # crea e assegna gli altri attributi di istanza
        self.nome = nome
        self.categoria = categoria
        self.prezzo = prezzo
        self.disponibile = disponibile

    @property
    def nome(self) -> str:
        """Restituisce il nome del piatto."""
        return self._nome

    @nome.setter
    def nome(self, valore: str) -> None:
        """Valida e imposta il nome (stringa non vuota dopo lo strip)."""
        # 1. Converti il valore in stringa e ripuliscilo dagli spazi periferici.
        valore = str(valore).strip()

        # 2. Se la stringa risultante è vuota, solleva DatiNonValidiError.
        if not valore:
            raise DatiNonValidiError("Il nome del piatto non può essere vuoto.")

        # 3. Assegna il valore al relativo attributo d'istanza protetto.
        self._nome = valore

    @property
    def categoria(self) -> str:
        """Restituisce la categoria del piatto in minuscolo."""
        return self._categoria 

    @categoria.setter
    def categoria(self, valore: Categoria) -> None:
        """Valida e imposta la categoria (deve appartenere alla tupla CATEGORIE)."""

        # 1. Rimuovi spazi e converti in caratteri minuscoli.
        valore = str(valore).strip().lower()

        # 2. Controlla se il valore appartiene alle categorie ammesse; altrimenti solleva DatiNonValidiError.
        if valore not in CATEGORIE:
            raise DatiNonValidiError("Categoria del piatto non valida.")

        # 3. Assegna il valore al relativo attributo d'istanza protetto.
        self._categoria = valore

    @property
    def prezzo(self) -> float:
        """Restituisce il prezzo corrente in euro."""
        return self._prezzo 

    @prezzo.setter
    def prezzo(self, valore: float) -> None:
        """Valida e imposta il prezzo (deve essere convertibile a float e > 0)."""
        # 1. Prova la conversione a decimale; se fallisce solleva DatiNonValidiError.
        try:
            prezzo_convertito = float(valore)
        except (ValueError, TypeError):
            raise DatiNonValidiError("Il prezzo deve essere un numero valido. ")  
          
        # 2. Verifica che il valore convertito sia strettamente positivo, altrimenti solleva DatiNonValidiError.
        if prezzo_convertito <= 0:
            raise DatiNonValidiError("Il prezzo deve essere maggiore di zero.")

        # 3. Assegna il valore al relativo attributo d'istanza protetto e arrotonda a due decimali il risultato.
        self._prezzo = round(prezzo_convertito, 2)

        # 4. In un caso reale in che formato salveresti i dati relativi ad un prezzo? Motiva la risposta.
        #Decimal, perché permette di rappresentare i valori monetari evitando gli errori di precisione tipici dei numeri float.

    def __str__(self) -> str:
        """Rappresentazione leggibile per il menù a terminale."""
        # Se il piatto non è disponibile, prepara un'etichetta di avviso
        stato: str = "" if self.disponibile else "  [non disponibile]"

        # Allinea l'ID a destra su 3 spazi, il nome a sinistra su 26 spazi e il prezzo con 2 decimali
        return f"{self.id:>3}. {self.nome:<26} {self.prezzo:>7.2f} €{stato}"

    def __repr__(self) -> str:
        """Rappresentazione tecnica dettagliata per lo sviluppatore."""
        return (
            f"Piatto(id_piatto={self.id}, nome={self.nome!r}, "
            f"categoria={self.categoria!r}, prezzo={self.prezzo}, "
            f"disponibile={self.disponibile})"   
        )

class Bevanda(Piatto):
    """Sottoclasse di Piatto che aggiunge l'attributo booleano alcolica."""

    def __init__(
        self,
        id_piatto: int,
        nome: str,
        prezzo: float,
        alcolica: bool = False,
        disponibile: bool = True,
    ) -> None:
        """Inizializza una bevanda richiamando la classe superiore e imposta la categoria fissa 'bevanda'."""
        # 1. Richiama il costruttore della classe superiore impostando la categoria fissa a bevanda.
        super().__init__(id_piatto, nome, "bevanda", prezzo, disponibile)


        # 2. Assegna l'attributo d'istanza per indicare se la bevanda è alcolica.
        self.alcolica = alcolica

    def __str__(self) -> str:
        """Aggiunge l'indicazione '(alcolica)' se previsto."""
        etichetta: str = "  (alcolica)" if self.alcolica else ""
        return super().__str__() + etichetta

if __name__ == "__main__":
    piatto = Piatto(1, "Carbonara", "primo", 10.5)
    print(piatto)
    bevanda = Bevanda(2, "Vino rosso", 4.5, alcolica=True)
    print(bevanda)





