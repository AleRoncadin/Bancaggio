import tkinter as tk
from tkinter import ttk, messagebox
from accounts_manager import (
    load_accounts, 
    save_accounts, 
    find_account, 
    add_or_update_account)
from trading import (
    connect_prop_account,
    connect_broker_account,
    open_prop_order, 
    open_broker_order, 
    close_all_prop_positions, 
    close_all_broker_positions,
    close_last_prop_position,
    close_last_broker_position,
    start_monitoring_prop_positions
)

class App:
    _instance = None

    def __init__(self, master):
        App._instance = self
        self.master = master
        master.title("Passaggio Prop")
        master.geometry("920x700")

        self.data = load_accounts()

        main_frame = tk.Frame(master, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Prepara liste login, server e path per prop e broker
        prop_logins = list({acc["login"] for acc in self.data["prop"]})
        prop_servers = list({acc["server"] for acc in self.data["prop"]})
        prop_paths = list({acc["mt5_path"] for acc in self.data["prop"] if "mt5_path" in acc})

        broker_logins = list({acc["login"] for acc in self.data["broker"]})
        broker_servers = list({acc["server"] for acc in self.data["broker"]})
        broker_paths = list({acc["mt5_path"] for acc in self.data["broker"] if "mt5_path" in acc})

        #
        # SEZIONE PROP
        #
        prop_frame = tk.LabelFrame(main_frame, text="PROP FIRM", padx=5, pady=5)
        prop_frame.grid(row=0, column=0, sticky="nw")

        tk.Label(prop_frame, text="Login:").grid(row=0, column=0, sticky="e")
        tk.Label(prop_frame, text="Password:").grid(row=1, column=0, sticky="e")
        tk.Label(prop_frame, text="Server:").grid(row=2, column=0, sticky="e")
        tk.Label(prop_frame, text="MT5 Path:").grid(row=3, column=0, sticky="e")

        self.prop_login_var = tk.StringVar()
        self.prop_server_var = tk.StringVar()
        self.prop_password_var = tk.StringVar()
        #self.prop_phase_var = tk.StringVar(value="1")
        #self.prop_size_var = tk.StringVar(value="100k")
        self.prop_path_var = tk.StringVar()

        self.prop_login_box = ttk.Combobox(prop_frame, values=prop_logins, textvariable=self.prop_login_var)
        self.prop_login_box.grid(row=0, column=1, sticky="w")
        self.prop_login_box.bind("<<ComboboxSelected>>", self.load_prop_from_login)

        self.prop_password_entry = ttk.Entry(prop_frame, textvariable=self.prop_password_var, show="*")
        self.prop_password_entry.grid(row=1, column=1, sticky="w")

        self.prop_server_box = ttk.Combobox(prop_frame, values=prop_servers, textvariable=self.prop_server_var)
        self.prop_server_box.grid(row=2, column=1, sticky="w")

        self.prop_path_box = ttk.Combobox(prop_frame, values=prop_paths, textvariable=self.prop_path_var, width=50)
        self.prop_path_box.grid(row=3, column=1, sticky="w")

        self.prop_login_btn = ttk.Button(prop_frame, text="Login", command=self.login_prop_account)
        self.prop_login_btn.grid(row=6, column=0, columnspan=2, pady=5)

        #
        # SEZIONE broker
        #
        broker_frame = tk.LabelFrame(main_frame, text="CONTO broker", padx=5, pady=5)
        broker_frame.grid(row=0, column=1, sticky="nw")

        tk.Label(broker_frame, text="Login:").grid(row=0, column=0, sticky="e")
        tk.Label(broker_frame, text="Password:").grid(row=1, column=0, sticky="e")
        tk.Label(broker_frame, text="Server:").grid(row=2, column=0, sticky="e")
        tk.Label(broker_frame, text="MT5 Path:").grid(row=3, column=0, sticky="e")

        self.broker_login_var = tk.StringVar()
        self.broker_server_var = tk.StringVar()
        self.broker_password_var = tk.StringVar()
        self.broker_path_var = tk.StringVar()

        self.broker_login_box = ttk.Combobox(broker_frame, values=broker_logins, textvariable=self.broker_login_var)
        self.broker_login_box.grid(row=0, column=1, sticky="w")
        self.broker_login_box.bind("<<ComboboxSelected>>", self.load_broker_from_login)

        self.broker_password_entry = ttk.Entry(broker_frame, textvariable=self.broker_password_var, show="*")
        self.broker_password_entry.grid(row=1, column=1, sticky="w")

        self.broker_server_box = ttk.Combobox(broker_frame, values=broker_servers, textvariable=self.broker_server_var)
        self.broker_server_box.grid(row=2, column=1, sticky="w")

        self.broker_path_box = ttk.Combobox(broker_frame, values=broker_paths, textvariable=self.broker_path_var, width=50)
        self.broker_path_box.grid(row=3, column=1, sticky="w")

        self.broker_login_btn = ttk.Button(broker_frame, text="Login", command=self.login_broker_account)
        self.broker_login_btn.grid(row=4, column=0, columnspan=2, pady=5)

        #
        # SEZIONE INPUT
        #
        input_frame = tk.LabelFrame(main_frame, text="INPUT", padx=5, pady=5)
        input_frame.grid(row=1, column=0, sticky="nw")

        tk.Label(input_frame, text="Simbolo PROP:").grid(row=0, column=0, sticky="e")
        tk.Label(input_frame, text="Simbolo broker:").grid(row=1, column=0, sticky="e")
        tk.Label(input_frame, text="Costo prop ($):").grid(row=2, column=0, sticky="e")
        tk.Label(input_frame, text="Dimensione prop:").grid(row=3, column=0, sticky="e")
        tk.Label(input_frame, text="Numero fasi:").grid(row=4, column=0, sticky="e")
        tk.Label(input_frame, text="Target (in %):").grid(row=5, column=0, sticky="e")
        tk.Label(input_frame, text="Max DD (in %):").grid(row=6, column=0, sticky="e")
        tk.Label(input_frame, text="Target (op singola in punti):").grid(row=7, column=0, sticky="e")
        tk.Label(input_frame, text="Target (op singola in %) del capitale della prop:").grid(row=8, column=0, sticky="e")

        self.symbol_prop_var = tk.StringVar()
        self.symbol_broker_var = tk.StringVar()
        self.costo_prop_var = tk.DoubleVar()
        self.target_per_var = tk.DoubleVar()
        self.max_dd_per_var = tk.DoubleVar()
        self.target_op_singola_punti_var = tk.DoubleVar()
        self.target_op_singola_per_var = tk.DoubleVar()
        self.prop_phase_var = tk.StringVar(value="1")
        self.prop_size_var = tk.StringVar(value="100k")

        ttk.Entry(input_frame, textvariable=self.symbol_prop_var).grid(row=0, column=1, sticky="w")
        ttk.Entry(input_frame, textvariable=self.symbol_broker_var).grid(row=1, column=1, sticky="w")
        ttk.Entry(input_frame, textvariable=self.costo_prop_var).grid(row=2, column=1, sticky="w")
        self.prop_size_box = ttk.Combobox(input_frame, values=["10k", "25k", "50k", "100k", "200k", "500k"], textvariable=self.prop_size_var)
        self.prop_size_box.grid(row=3, column=1, sticky="w")
        self.prop_phase_frame = tk.Frame(input_frame)
        self.prop_phase_frame.grid(row=4, column=1, sticky="w")
        self.phase1_radio = ttk.Radiobutton(self.prop_phase_frame, text="1", variable=self.prop_phase_var, value="1")
        self.phase2_radio = ttk.Radiobutton(self.prop_phase_frame, text="2", variable=self.prop_phase_var, value="2")
        self.phase1_radio.pack(side="left")
        self.phase2_radio.pack(side="left")
        ttk.Entry(input_frame, textvariable=self.target_per_var).grid(row=5, column=1, sticky="w")
        ttk.Entry(input_frame, textvariable=self.max_dd_per_var).grid(row=6, column=1, sticky="w")
        ttk.Entry(input_frame, textvariable=self.target_op_singola_punti_var).grid(row=7, column=1, sticky="w")
        ttk.Entry(input_frame, textvariable=self.target_op_singola_per_var).grid(row=8, column=1, sticky="w")

        # Importante: qui passo la funzione, senza parentesi
        ttk.Button(input_frame, text="Calcola", command=self.calculate_outputs).grid(row=9, column=1, padx=10, pady=10)

        #
        # SEZIONE OUTPUT
        #
        output_frame = tk.LabelFrame(main_frame, text="OUTPUT", padx=5, pady=5)
        output_frame.grid(row=1, column=1, sticky="nw")

        tk.Label(output_frame, text="Rapporto Target/Max DD:").grid(row=0, column=0, sticky="e")
        tk.Label(output_frame, text="Stoploss op singola (in punti):").grid(row=1, column=0, sticky="e")
        tk.Label(output_frame, text="N. Operazioni necessarie:").grid(row=2, column=0, sticky="e")
        tk.Label(output_frame, text="").grid(row=3, column=0, sticky="e")
        tk.Label(output_frame, text="Lottaggio prop:").grid(row=4, column=0, sticky="e")
        tk.Label(output_frame, text="Target prop (in $):").grid(row=5, column=0, sticky="e")
        tk.Label(output_frame, text="Stoploss prop (in $):").grid(row=6, column=0, sticky="e")
        tk.Label(output_frame, text="Target singola prop (in %):").grid(row=7, column=0, sticky="e")
        tk.Label(output_frame, text="Stoploss singola prop (in %):").grid(row=8, column=0, sticky="e")
        tk.Label(output_frame, text="").grid(row=9, column=0, sticky="e")
        tk.Label(output_frame, text="Commissioni broker:").grid(row=10, column=0, sticky="e")
        tk.Label(output_frame, text="Deposito broker:").grid(row=11, column=0, sticky="e")
        tk.Label(output_frame, text="Target broker (in punti):").grid(row=12, column=0, sticky="e")
        tk.Label(output_frame, text="Stoploss broker (in punti):").grid(row=13, column=0, sticky="e")
        tk.Label(output_frame, text="Target broker (in dollari):").grid(row=14, column=0, sticky="e")
        tk.Label(output_frame, text="Stoploss broker (in dollari):").grid(row=15, column=0, sticky="e")
        tk.Label(output_frame, text="Lottaggio broker:").grid(row=16, column=0, sticky="e")

        # Invece di scrivere subito il valore, creo label "vuote" (o con 0) da aggiornare in calculate_outputs
        self.rapporto_label = tk.Label(output_frame, text="0")
        self.rapporto_label.grid(row=0, column=1, sticky="e")

        self.stoploss_op_singola_label = tk.Label(output_frame, text="0")
        self.stoploss_op_singola_label.grid(row=1, column=1, sticky="e")

        self.n_operazioni_label = tk.Label(output_frame, text="0")
        self.n_operazioni_label.grid(row=2, column=1, sticky="e")

        tk.Label(output_frame, text="").grid(row=3, column=1, sticky="e")

        self.lottaggio_prop_label = tk.Label(output_frame, text="0")
        self.lottaggio_prop_label.grid(row=4, column=1, sticky="e")

        self.target_dollari_prop_label = tk.Label(output_frame, text="0")
        self.target_dollari_prop_label.grid(row=5, column=1, sticky="e")

        self.stoploss_dollari_prop_label = tk.Label(output_frame, text="0")
        self.stoploss_dollari_prop_label.grid(row=6, column=1, sticky="e")

        self.target_per_op_singola_prop_label = tk.Label(output_frame, text="0")
        self.target_per_op_singola_prop_label.grid(row=7, column=1, sticky="e")

        self.stoploss_per_op_singola_prop_label = tk.Label(output_frame, text="0")
        self.stoploss_per_op_singola_prop_label.grid(row=8, column=1, sticky="e")

        tk.Label(output_frame, text="").grid(row=9, column=1, sticky="e")

        self.commissioni_label = tk.Label(output_frame, text="0")
        self.commissioni_label.grid(row=10, column=1, sticky="e")

        self.deposito_broker_label = tk.Label(output_frame, text="0")
        self.deposito_broker_label.grid(row=11, column=1, sticky="e")

        self.target_broker_punti_label = tk.Label(output_frame, text="0")
        self.target_broker_punti_label.grid(row=12, column=1, sticky="e")

        self.stoploss_broker_punti_label = tk.Label(output_frame, text="0")
        self.stoploss_broker_punti_label.grid(row=13, column=1, sticky="e")

        self.target_dollari_broker_label = tk.Label(output_frame, text="0")
        self.target_dollari_broker_label.grid(row=14, column=1, sticky="e")

        self.stoploss_dollari_broker_label = tk.Label(output_frame, text="0")
        self.stoploss_dollari_broker_label.grid(row=15, column=1, sticky="e")

        self.lottaggio_broker_label = tk.Label(output_frame, text="0")
        self.lottaggio_broker_label.grid(row=16, column=1, sticky="e")

        ttk.Button(output_frame, text="BUY", command=lambda: self.run_trade("BUY")).grid(row=17, column=0, padx=10, pady=10)
        ttk.Button(output_frame, text="SELL", command=lambda: self.run_trade("SELL")).grid(row=17, column=1, padx=10, pady=10)

        ttk.Button(main_frame, text="Chiudi ordini", command=self.close_positions_on_both).grid(row=2, column=2, padx=10, pady=10)

    @classmethod
    def get_instance(cls):
        return cls._instance

    def load_prop_from_login(self, event):
        login = self.prop_login_var.get()
        candidates = [acc for acc in self.data["prop"] if acc["login"] == login]
        if candidates:
            acc = candidates[0]
            self.prop_server_var.set(acc["server"])
            self.prop_password_var.set(acc["password"])
            self.prop_path_var.set(acc.get("mt5_path", ""))

    def load_broker_from_login(self, event):
        login = self.broker_login_var.get()
        candidates = [acc for acc in self.data["broker"] if acc["login"] == login]
        if candidates:
            acc = candidates[0]
            self.broker_server_var.set(acc["server"])
            self.broker_password_var.set(acc["password"])
            self.broker_path_var.set(acc.get("mt5_path", ""))

    def login_prop_account(self):
        login = self.prop_login_var.get()
        server = self.prop_server_var.get()
        password = self.prop_password_var.get()
        mt5_path = self.prop_path_var.get()

        if not login or not server or not password:
            messagebox.showerror("Errore", "Dati prop incompleti.")
            return

        if connect_prop_account(login, password, server, mt5_path):
            add_or_update_account(self.data["prop"], login, server, password, mt5_path)
            save_accounts(self.data)
            messagebox.showinfo("Login", "Login PROP riuscito e credenziali salvate.")
            self.update_prop_comboboxes()
            #start_prop_check_thread(account_size)
        else:
            messagebox.showerror("Errore", "Login PROP fallito.")

    def login_broker_account(self):
        login = self.broker_login_var.get()
        server = self.broker_server_var.get()
        password = self.broker_password_var.get()
        mt5_path = self.broker_path_var.get()

        if not login or not server or not password:
            messagebox.showerror("Errore", "Dati broker incompleti.")
            return

        if connect_broker_account(login, password, server, mt5_path):
            add_or_update_account(self.data["broker"], login, server, password, mt5_path)
            save_accounts(self.data)
            messagebox.showinfo("Login", "Login broker riuscito e credenziali salvate.")
            self.update_broker_comboboxes()
        else:
            messagebox.showerror("Errore", "Login broker fallito.")

    def update_prop_comboboxes(self):
        prop_logins = list({acc["login"] for acc in self.data["prop"]})
        prop_servers = list({acc["server"] for acc in self.data["prop"]})
        prop_paths = list({acc["mt5_path"] for acc in self.data["prop"] if "mt5_path" in acc})
        self.prop_login_box["values"] = prop_logins
        self.prop_server_box["values"] = prop_servers
        self.prop_path_box["values"] = prop_paths

    def update_broker_comboboxes(self):
        broker_logins = list({acc["login"] for acc in self.data["broker"]})
        broker_servers = list({acc["server"] for acc in self.data["broker"]})
        broker_paths = list({acc["mt5_path"] for acc in self.data["broker"] if "mt5_path" in acc})
        self.broker_login_box["values"] = broker_logins
        self.broker_server_box["values"] = broker_servers
        self.broker_path_box["values"] = broker_paths

    def get_selected_prop_account(self):
        login = self.prop_login_var.get()
        server = self.prop_server_var.get()
        acc = find_account(self.data["prop"], login, server)
        if not acc:
            password = self.prop_password_var.get()
            if not password:
                return None
            acc = {
                "login": login,
                "server": server,
                "password": password,
                "account_size": self.prop_size_var.get(),
                "phase": self.prop_phase_var.get(),
                "mt5_path": self.prop_path_var.get()
            }
        return acc

    def get_selected_broker_account(self):
        login = self.broker_login_var.get()
        server = self.broker_server_var.get()
        acc = find_account(self.data["broker"], login, server)
        if not acc:
            password = self.broker_password_var.get()
            if not password:
                return None
            acc = {
                "login": login,
                "server": server,
                "password": password,
                "mt5_path": self.broker_path_var.get()
            }
        return acc

    def run_trade(self, direction):
        prop_acc = self.get_selected_prop_account()
        broker_acc = self.get_selected_broker_account()

        if not prop_acc or not broker_acc:
            messagebox.showerror("Errore", "Account prop o broker non configurato correttamente.")
            return
        
        symbol_prop = self.symbol_prop_var.get()
        symbol_broker = self.symbol_broker_var.get()
        if not symbol_prop or not symbol_broker:
            messagebox.showerror("Errore", "Inserire simbolo.")
            return

        lottaggio_prop_text = self.lottaggio_prop_label.cget("text")   
        try:
            # Converte il valore in float
            lottaggio_prop = float(lottaggio_prop_text)
        except ValueError:
            # In caso di errore (es. testo vuoto o non numerico), restituisce errore
            messagebox.showerror("Errore", "Lottaggio della prop errato.")
            return

        lottaggio_broker_text = self.lottaggio_broker_label.cget("text")
        try:
            # Converte il valore in float
            lottaggio_broker = float(lottaggio_broker_text)
        except ValueError:
            # In caso di errore (es. testo vuoto o non numerico), restituisce errore
            messagebox.showerror("Errore", "Lottaggio del broker errato.")
            return

        target_broker_punti_text = self.target_broker_punti_label.cget("text")
        try:
            # Converte il valore in float
            target_broker_punti = float(target_broker_punti_text)
        except ValueError:
            # In caso di errore (es. testo vuoto o non numerico), restituisce errore
            messagebox.showerror("Errore", "Target errato")
            return

        stoploss_broker_punti_text = self.stoploss_broker_punti_label.cget("text")
        try:
            # Converte il valore in float
            stoploss_broker_punti = float(stoploss_broker_punti_text)
        except ValueError:
            # In caso di errore (es. testo vuoto o non numerico), restituisce errore
            messagebox.showerror("Errore", "Stoploss errato")
            return

        # simbolo, direction, lots, tp_points, sl_points
        apri_ordine_prop, retcode_prop = open_prop_order(symbol_prop, direction, lottaggio_prop, stoploss_broker_punti * 100, target_broker_punti * 100)
        apri_ordine_broker, retcode_broker = open_broker_order(symbol_broker, direction, lottaggio_broker, target_broker_punti, stoploss_broker_punti)

        if apri_ordine_prop and apri_ordine_broker:
            start_monitoring_prop_positions()
            messagebox.showinfo("Info", "Posizioni aperte correttamente")
        elif not apri_ordine_prop and apri_ordine_broker:
            close_last_broker_position()
            messagebox.showerror("Errore", f"Impossibile aprire su PROP, ERROR {retcode_prop}")
            return
        elif not apri_ordine_broker and apri_ordine_prop:
            close_last_prop_position()
            messagebox.showerror("Errore", f"Impossibile aprire su broker, ERROR {retcode_broker}")
            return
        else: # caso in cui non riesco ne aprire di qua ne di la
            messagebox.showerror("Errore", f"Impossibile aprire su PROP (ERROR{retcode_prop}) e broker (ERROR {retcode_broker})")  
            return   

    def close_positions_on_both(self):

        prop_acc = self.get_selected_prop_account()
        broker_acc = self.get_selected_broker_account()

        if not prop_acc or not broker_acc:
            messagebox.showerror("Errore", "Account prop o broker non configurato correttamente.")
            return

        symbol_prop = self.symbol_prop_var.get()
        symbol_broker = self.symbol_broker_var.get()
        if not symbol_prop or not symbol_broker:
            messagebox.showerror("Errore", "Inserire simbolo.")
            return
        
        confirm = messagebox.askyesno("Conferma", f"Sicuro di voler chiudere gli ordini su {symbol_prop}/{symbol_broker}?")
        if not confirm:
            return

        chiudi_ordini_prop = close_all_prop_positions()
        chiudi_ordini_broker = close_all_broker_positions()

        if chiudi_ordini_prop and chiudi_ordini_broker:
            messagebox.showinfo("Info", "Tutte le posizioni chiuse.")
            return
        elif not chiudi_ordini_prop and chiudi_ordini_broker: 
            messagebox.showerror("Errore", "Impossibile chiudere tutti gli ordini su PROP")
            return
        elif chiudi_ordini_prop and not chiudi_ordini_broker:   
            messagebox.showerror("Errore", "Impossibile chiudere tutti gli ordini su broker")
            return
        else:
            messagebox.showerror("Errore", "Impossibile chiudere tutti gli ordini su PROP e broker")
            return

    def calculate_outputs(self):
        """
        Calcola tutti i valori di output partendo dagli input.
        Poi aggiorna i Label di output per mostrare i risultati.
        """
        # Preleva i valori come float
        target_per = self.target_per_var.get()       # % target
        max_dd_per = self.max_dd_per_var.get()       # % max drawdown
        costo_prop = self.costo_prop_var.get()       # costo della prop
        target_op_singola_punti = self.target_op_singola_punti_var.get()
        target_op_singola_per = self.target_op_singola_per_var.get()

        # Per il calcolo, assumendo self.prop_size_var.get() sia tipo "100k" -> ricavo float
        # Se "100k", prendo 100000. Se "50k", 50000, ecc.
        try:
            prop_size_str = self.prop_size_var.get().lower().replace("k", "")
            prop_size = float(prop_size_str) * 1000
        except:
            messagebox.showerror("Errore", "Dimensione conto della prop errato")
            return
        
        prop_phases = float(self.prop_phase_var.get())
        
        rapporto = (target_per / 100) / (max_dd_per / 100)
        stoploss_op_singola_punti = target_op_singola_punti * (1 / rapporto)
        n_operazioni_necessarie = target_per / target_op_singola_per

        target_dollari_prop = (target_op_singola_per / 100) * prop_size

        stoploss_dollari_prop = target_dollari_prop * (1 / rapporto)

        lottaggio_prop = target_dollari_prop / (target_op_singola_punti * 100)

        target_per_op_singola_prop = target_op_singola_per

        # Stoploss (in %) operazione singola prop
        stoploss_per_op_singola_prop = target_per_op_singola_prop * (1 / rapporto)

        # Commissioni broker
        commissioni = (costo_prop * prop_phases) * 0.1

        # Target dollari broker
        target_dollari_broker = (costo_prop / n_operazioni_necessarie)

        # Stoploss dollari broker
        stoploss_dollari_broker = (target_dollari_broker * (1 / rapporto))

        # Deposito broker
        deposito_broker = (costo_prop * prop_phases) + commissioni

        # Target punti broker
        target_broker_punti = stoploss_op_singola_punti

        # Stoploss punti broker
        stoploss_broker_punti = target_op_singola_punti

        # Lottaggio broker
        lottaggio_broker = (target_dollari_broker / target_broker_punti) / 100

        # Arrotonda lottaggio
        seconda_cifra = int((lottaggio_broker * 100) % 10)
        terza_cifra = int((lottaggio_broker * 1000) % 10)
        if terza_cifra > 0:
            seconda_cifra += 1
            # Aggiorna il numero con la nuova seconda cifra
            lottaggio_broker = int(lottaggio_broker * 10) / 10 + seconda_cifra / 100
        lottaggio_broker = int(lottaggio_broker * 100) / 100            

        #
        # Aggiorna le label
        #
        self.rapporto_label.config(text=f"{rapporto:.2f}")
        self.stoploss_op_singola_label.config(text=f"{stoploss_op_singola_punti:.2f}")
        self.n_operazioni_label.config(text=f"{n_operazioni_necessarie:.2f}")

        self.lottaggio_prop_label.config(text=f"{lottaggio_prop:.2f}")
        self.target_dollari_prop_label.config(text=f"{target_dollari_prop:.2f}")
        self.stoploss_dollari_prop_label.config(text=f"{stoploss_dollari_prop:.2f}")
        self.target_per_op_singola_prop_label.config(text=f"{target_per_op_singola_prop:.2f}")
        self.stoploss_per_op_singola_prop_label.config(text=f"{stoploss_per_op_singola_prop:.2f}")

        self.commissioni_label.config(text=f"{commissioni:.2f}")
        self.deposito_broker_label.config(text=f"{deposito_broker:.2f}")
        self.target_broker_punti_label.config(text=f"{target_broker_punti:.2f}")
        self.stoploss_broker_punti_label.config(text=f"{stoploss_broker_punti:.2f}")
        self.target_dollari_broker_label.config(text=f"{target_dollari_broker:.2f}")
        self.stoploss_dollari_broker_label.config(text=f"{stoploss_dollari_broker:.2f}")
        self.lottaggio_broker_label.config(text=f"{lottaggio_broker:.3f}")
