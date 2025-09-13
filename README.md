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
- [Integrazione con MetaTrader 5](#integrazione-con-metatrader-5)
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

1. **Duplica MT5** (vedi `istruzioni.txt`)  
   - Copia `C:\Program Files\MetaTrader 5` in `C:\Program Files\MetaTrader 5_1`.  
   - Su **entrambe**: Proprietà → Sicurezza → **Controllo completo** → Applica.  
   - Avvia **entrambi** i terminali e **fai login** ai rispettivi conti.

2. **Clona la repository** e apri un **Prompt dei comandi** nella cartella del progetto.

3. **Esegui**:
   ```bat
   install.bat

  Lo script:
  - Verifica Python 3.12+
  - Verifica/installa pip
  - Verifica/installa numpy==1.26.4
  - Verifica/installa pyinstaller
  - Pulisce build/ e dist/
  - Crea un .exe one-file includendo Meta1/ e Meta2/

4. L'eseguibile sarà in **dist\main.exe**.

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

