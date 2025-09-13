import json
import os

ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    """Carica i dati degli account da ACCOUNTS_FILE."""
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as f:
            return json.load(f)
    return {"prop": [], "broker": []}

def save_accounts(data):
    """Salva i dati degli account su ACCOUNTS_FILE."""
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def find_account(data_list, login, server):
    """Ritorna l'account con login e server specificati, oppure None."""
    for acc in data_list:
        if acc["login"] == login and acc["server"] == server:
            return acc
    return None

def add_or_update_account(data_list, login, server, password, mt5_path=None):
    """Aggiunge o aggiorna un account nella lista data_list."""
    acc = find_account(data_list, login, server)
    if acc:
        acc["password"] = password
        if mt5_path is not None:
            acc["mt5_path"] = mt5_path
    else:
        new_acc = {
            "login": login,
            "server": server,
            "password": password
        }
        if mt5_path is not None:
            new_acc["mt5_path"] = mt5_path
        data_list.append(new_acc)
