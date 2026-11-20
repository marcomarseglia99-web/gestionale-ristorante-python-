# Questo file contiene le funzioni per acquisire e verificare gli input inseriti dall'utente.

def chiedi_testo(messaggio: str) -> str:
    """Chiede una stringa non vuota all'utente, ripetendo in caso di input vuoto."""

    # 1. Avvia un ciclo per continuare a richiedere l'input finché non è valido.
    while True:
        # 2. Acquisisci l'input ripulendolo dagli spazi periferici.
        testo = input(messaggio).strip()

        # 3. Se la stringa contiene testo restituiscila, altrimenti mostra un messaggio di errore e richiedi nuovamente.
        if testo:
            return testo
        print("L'input non può essere vuoto.")


def chiedi_intero(
    messaggio: str,
    minimo: int | None = None,
    massimo: int | None = None,
) -> int:
    """Chiede un intero, verificando opzionalmente l'intervallo [minimo, massimo]."""

    # 1. Avvia un ciclo di richiesta.
    while True:
        # 2. Tenta la conversione dell'input in intero; se fallisce con errore di conversione, avvisa l'utente e richiedi di nuovo.
        try:
            numero = int(input(messaggio))
        except ValueError:
            print("Inserisci un numero intero valido")
            continue

        # 3. Se è impostato un valore minimo e il numero è inferiore, avvisa l'utente.
        if minimo is not None and numero < minimo:
            print(f"Inserisci un numero maggiore o uguale a {minimo}.")
            continue

        # 4. Se è impostato un valore massimo e il numero è superiore, avvisa l'utente.
        if massimo is not None and numero > massimo:
            print(f"Inserisci un numero minore o uguale a {massimo}.")
            continue

        # 5. Se tutti i vincoli sono rispettati, restituisci il numero.
        return numero

def chiedi_prezzo(messaggio: str) -> float:
    """Chiede un prezzo positivo (> 0), gestendo sia la virgola sia il punto decimale."""
    
    # 1. Avvia un ciclo di richiesta.
    while True:
        # 2. Acquisisci l'input gestendo sia il punto che l'eventuale virgola decimale.
        testo = input(messaggio).strip().replace(",", ".")
    

        # 3. Tenta la conversione a numero decimale; se fallisce, avvisa l'utente e richiedi nuovamente.
        try:
            prezzo = float(testo)
        except ValueError:
            print("Inserisci un prezzo valido.")
            continue


        # 4. Verifica che il valore sia strettamente maggiore di zero; se non lo è, avvisa l'utente.
        if prezzo <= 0:
            print("Il prezzo deve essere maggiore di zero.")
            continue

        # 5. Restituisci il prezzo valido e arrotonda a due decimali il risultato.
        return round(prezzo, 2)

def chiedi_conferma(messaggio: str) -> bool:
    """Chiede una risposta (s/n). Restituisce True per sì/s, False per no/n."""

    # 1. Avvia un ciclo di richiesta normalizzando la risposta in minuscolo.
    while True:
        risposta = input(messaggio).strip().lower()

        # 2. Se la risposta corrisponde a un'affermazione (es. 's', 'si', 'sì'), restituisci True.
        if risposta in ("s", "si", "sì"):
            return True

        # 3. Se corrisponde a una negazione (es. 'n', 'no'), restituisci False.
        if risposta in ("n", "no"):
            return False

        # 4. Altrimenti avvisa l'utente della risposta non valida e ripeti.
        print("Risposta non valida, Inserisci s/n.")
        