# Bancaggio

> Sincronizza operazioni tra un **conto Prop Firm** e un **conto Reale** su **due istanze distinte di MetaTrader 5**.  
> Aperture coordinate, chiusure di emergenza, calcoli automatici (lotti/target/stop) e packaging in eseguibile Windows.

![OS](https://img.shields.io/badge/OS-Windows%2010%2F11-blue)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![MT5](https://img.shields.io/badge/MetaTrader%205-2%20istanze-important)
![UI](https://img.shields.io/badge/UI-Tkinter-lightgrey)

---

## Indice
- [Caratteristiche](#caratteristiche)
- [Requisiti](#requisiti)
- [Installazione e build (Windows)](#installazione-e-build-windows)
- [Configurazione degli account](#configurazione-degli-account)
- [Utilizzo](#utilizzo)
- [Logica dei calcoli](#logica-dei-calcoli)
- [Sicurezza e privacy](#sicurezza-e-privacy)
- [Troubleshooting](#troubleshooting)

---

## Caratteristiche

- **Doppia connessione MT5**: una istanza per **Prop** e una per **Broker**, in modalità **portable**, con stato indipendente.
- **Apertura sincronizzata**: apre un’operazione sulla Prop e l’operazione **opposta** sul Broker (copertura/hedge).
- **Chiusure automatiche**: se non ci sono più posizioni aperte sulla Prop, **chiude tutte** le posizioni sul Broker.
- **Pannello unico (Tkinter)** per:
  - Login e selezione account (Prop/Broker)
  - Parametri operativi e **calcoli automatici** (lotti, target, stop, rapporto target/DD, n° operazioni, commissioni, deposito, …)
  - Azioni rapide: **BUY**, **SELL**, **Chiudi ordini**.
- **Persistenza** delle credenziali e dei percorsi MT5 in `accounts.json` (locale).
- **Packaging** one-file con **PyInstaller**, includendo **due copie** del pacchetto Python `MetaTrader5` rinominate in `Meta1` e `Meta2`.

> **Nota fondamentale**  
> Per gestire **due istanze** di MT5 nella stessa macchina, il progetto include **due copie** del modulo Python `MetaTrader5` rinominate in **`Meta1`** (Prop) e **`Meta2`** (Broker). In `trading.py`:
> ```python
> import Meta2 as mt5_broker
> import Meta1 as mt5_prop
> ```
> In questo modo le due sessioni MT5 mantengono **stato separato**.

---

## Requisiti

- **Sistema**: Windows 10/11  
- **MetaTrader 5**: **2 installazioni distinte**  
  - Esempio: `C:\Program Files\MetaTrader 5` e `C:\Program Files\MetaTrader 5_1`
- **Permessi di scrittura** sulle cartelle MT5  
  - Proprietà → Sicurezza → **Controllo completo** agli utenti pertinenti
- **Python 3.12+** e **pip**
- **Pacchetti Python**:
  - `numpy==1.26.4`
  - `pyinstaller`

---

## Installazione e build (Windows)

- **Duplica MT5** (vedi `istruzioni.txt`)  
  - Copia `C:\Program Files\MetaTrader 5` in `C:\Program Files\MetaTrader 5_1`.  
  - Su **entrambe**: Proprietà → Sicurezza → **Controllo completo** → Applica.  
  - Avvia **entrambi** i terminali e **fai login** ai rispettivi conti.
- **Clona la repository** e apri un **Prompt dei comandi** nella cartella del progetto.
- **Esegui**:
   ```bat
   install.bat

  Lo script:
  - Verifica Python 3.12+
  - Verifica/installa pip
  - Verifica/installa numpy==1.26.4
  - Verifica/installa pyinstaller
  - Pulisce build/ e dist/
  - Crea un .exe one-file includendo Meta1/ e Meta2/
- L'eseguibile sarà in **dist\main.exe**.

## Configurazione e Utilizzo del Sistema Prop/Broker

### Configurazione degli account

Il file `accounts.json` salva le credenziali **in chiaro** (solo in locale).  
**Non commitare credenziali reali** nei repository pubblici.

#### Esempio di `accounts.json`

```json
{
  "prop": [
    {
      "login": "1520607116",
      "server": "FTMO-Demo2",
      "password": "",
      "mt5_path": "C:\\Program Files\\MetaTrader 5\\terminal64.exe"
    }
  ],
  "broker": [
    {
      "login": "5032295218",
      "server": "MetaQuotes-Demo",
      "password": "",
      "mt5_path": "C:\\Program Files\\MetaTrader 5_1\\terminal64.exe"
    }
  ]
}
```
Compila le password e verifica i percorsi **mt5_path**.
Prop e Broker devono puntare a istanze diverse di MetaTrader 5.

## Utilizzo

- Avvia entrambi gli MT5 e fai login (Prop e Broker).
- Avvia l’app
- Login:
  - PROP: inserisci login, server, password, path → Login
  - BROKER: stesso procedimento
- Inserisci:
  - Simbolo Prop / Simbolo Broker
  - Costo Prop ($)
  - Dimensione (10k–500k)
  - Fasi (1/2)
  - Target %, Max DD %, Target per operazione (punti e %)
- Clicca **Calcola** per ottenere:
  - Rapporto target/DD
  - SL operazione singola (punti)
  - Numero operazioni
  - Lotti Prop, Target/SL Prop ($ e %)
  - Commissioni stimate, deposito Broker
  - Target/SL Broker (punti e $), lotti Broker

### BUY / SELL
- **Prop**: apre nella direzione richiesta (TP/SL calcolati da punti → prezzo)
- **Broker**: apre nella direzione opposta (hedge)
- Chiusura ordini
  - **Monitor automatico**: Se la Prop non ha più posizioni aperte, il sistema chiude tutte le posizioni su Broker.
  - **Chiudi ordini**: pulsante che appena premuto chiude tutte le posizioni su Prop e Broker.

## Logica dei calcoli
Le formule principali sono contenute in **app.py::calculate_outputs**.
**Nota**: I lotti Broker sono arrotondati alla seconda/terza cifra decimale

## Sicurezza e privacy
- **accounts.json** contiene password in chiaro:
- Implementare cifratura locale (es. **DPAPI**, **Keyring**) per future versioni

## Troubleshooting
- **Login MT5 fallito**: verifica **mt5_path**, credenziali, server, avvio in portable, permessi cartella
- **symbol_info è None**: aggiungi il simbolo al Market Watch e abilitalo
- **order_send retcode != DONE**: controlla spread, deviation, orari mercato, regole di esecuzione (**FOK/IOC/RETURN/BOC**)
- **Permessi**: inizializzazione spesso fallisce per permessi insufficienti su cartelle MT5
- **Doppia istanza**: verifica che Prop punti a **MetaTrader 5** e Broker a **MetaTrader 5_1** con relativi **mt5_path**
