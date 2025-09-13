import Meta2 as mt5_broker
import Meta1 as mt5_prop
import threading
import time

def connect_prop_account(login, password, server, mt5_path):
    connected = mt5_prop.initialize(path=mt5_path, login=int(login), password=password, server=server, portable=True)
    return connected

def connect_broker_account(login, password, server, mt5_path):
    connected = mt5_broker.initialize(path=mt5_path, login=int(login), password=password, server=server, portable=True)
    return connected

def get_type_filling(mt5, filling_mode):
    type_filling = None

    if filling_mode and mt5.ORDER_FILLING_FOK:
        type_filling = mt5.ORDER_FILLING_FOK
    elif filling_mode and mt5.ORDER_FILLING_IOC:
        type_filling = mt5.ORDER_FILLING_IOC
    elif filling_mode and mt5.ORDER_FILLING_RETURN:
        type_filling = mt5.ORDER_FILLING_RETURN
    elif filling_mode and mt5.ORDER_FILLING_BOC:
        type_filling = mt5.ORDER_FILLING_BOC
    
    print(type_filling)
    return type_filling

def open_prop_order(symbol, direction, lots, tp_points, sl_points):
    symbol_info = mt5_prop.symbol_info(symbol)
    if symbol_info is None:
        print(f"Simbolo {symbol} non disponibile su PROP.")
        return None
    
    if not mt5_prop.symbol_select(symbol, True):
        print(f"Impossibile selezionare il simbolo {symbol} su PROP.")
        return None

    tick = mt5_prop.symbol_info_tick(symbol)
    if not tick:
        print("Nessun tick disponibile per il simbolo (PROP).")
        return None

    if direction == "BUY":
        price = tick.ask
        sl_price = price - sl_points * symbol_info.point
        tp_price = price + tp_points * symbol_info.point
        order_type = mt5_prop.ORDER_TYPE_BUY
    else:
        price =  tick.bid
        sl_price = price + sl_points * symbol_info.point
        tp_price = price - tp_points * symbol_info.point
        order_type = mt5_prop.ORDER_TYPE_SELL

    type_filling = get_type_filling(mt5_prop, symbol_info)

    request = {
        "action": mt5_prop.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(lots),
        "type": order_type,
        "price": price,
        "sl": sl_price,
        "tp": tp_price,
        "deviation": int(0),
        "type_filling": type_filling
    }

    print(f"PROP order: \t Price: {price}, SL: {sl_price}, TP: {tp_price}, lots: {lots}")
    result = mt5_prop.order_send(request)
    if result is None:
        return False, None
    elif result.retcode != mt5_prop.TRADE_RETCODE_DONE:
        return False, result.retcode
    else:
        return True, None

def open_broker_order(symbol, direction, lots, tp_points, sl_points):
    symbol_info = mt5_broker.symbol_info(symbol)
    if symbol_info is None:
        print(f"Simbolo {symbol} non disponibile su broker.")
        return None
    
    if not mt5_broker.symbol_select(symbol, True):
        print(f"Impossibile selezionare il simbolo {symbol} su broker.")
        return None

    tick = mt5_broker.symbol_info_tick(symbol)
    if not tick:
        print("Nessun tick disponibile per il simbolo (broker).")
        return None
    
    filling_mode = symbol_info.filling_mode
    print("Broker type filling: ", filling_mode)

    if direction == "BUY":
        price = tick.bid # fa sell, quindi l'operazione opposta
        sl_price = price + sl_points * symbol_info.point
        tp_price = price - tp_points * symbol_info.point
        order_type = mt5_broker.ORDER_TYPE_SELL
    else:
        price = tick.ask # fa buy, quindi l'operazione opposta
        sl_price = price - sl_points * symbol_info.point
        tp_price = price + tp_points * symbol_info.point
        order_type = mt5_broker.ORDER_TYPE_BUY

    type_filling = get_type_filling(mt5_broker, symbol_info)

    request = {
        "action": mt5_broker.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(lots),
        "type": order_type,
        "price": price,
        "deviation": int(0),
        "type_filling": 2
    }
    print(f"broker order: \t Price: {price}, SL: {sl_price}, TP: {tp_price}, lots: {lots}")
    result = mt5_broker.order_send(request)
    if result is None:
        return False, None
    elif result.retcode != mt5_broker.TRADE_RETCODE_DONE:
        return False, result.retcode
    else:
        return True, None
    
def close_all_prop_positions():
    positions = mt5_prop.positions_get()
    results = True
    if positions:
        for pos in positions:
            symbol = pos.symbol
            volume = pos.volume
            ticket = pos.ticket
            direction = pos.type  # 0=buy, 1=sell
            tick = mt5_prop.symbol_info_tick(symbol)
            if not tick:
                continue
            price = tick.bid if direction == 0 else tick.ask
            order_type = mt5_prop.ORDER_TYPE_SELL if direction == 0 else mt5_prop.ORDER_TYPE_BUY
            #type_filling = get_type_filling(mt5_prop, mt5_prop.symbol_info(symbol))
            close_request = {
                "action": mt5_prop.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "position": ticket,
                "price": price,
                "deviation": 0,
                #"type_filling": type_filling
            }
            result = mt5_prop.order_send(close_request)
            if result is None:
                results = False
            if result.retcode != mt5_prop.TRADE_RETCODE_DONE:
                results = False
    return results

def close_all_broker_positions():
    positions = mt5_broker.positions_get()
    results = True
    if positions:
        for pos in positions:
            symbol = pos.symbol
            volume = pos.volume
            ticket = pos.ticket
            direction = pos.type  # 0=buy, 1=sell
            tick = mt5_broker.symbol_info_tick(symbol)
            if not tick:
                continue
            price = tick.bid if direction == 0 else tick.ask
            order_type = mt5_broker.ORDER_TYPE_SELL if direction == 0 else mt5_broker.ORDER_TYPE_BUY
            #type_filling = get_type_filling(mt5_broker, mt5_broker.symbol_info(symbol))
            close_request = {
                "action": mt5_broker.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "position": ticket,
                "price": price,
                "deviation": 0,
                #"type_filling": type_filling
            }
            result = mt5_broker.order_send(close_request)
            if result is None:
                results = False
            if result.retcode != mt5_broker.TRADE_RETCODE_DONE:
                results = False
    return results

def close_last_prop_position():
    # Ottiene tutte le posizioni aperte sul conto prop
    positions = mt5_prop.positions_get()
    if not positions:
        print("Nessuna posizione aperta sul conto PROP.")
        return

    # Se ci sono posizioni, prendiamo l'ultima (in ordine di elenco)
    last_position = positions[-1]

    symbol = last_position.symbol
    volume = last_position.volume
    ticket = last_position.ticket
    direction = last_position.type  # 0=buy, 1=sell

    # Otteniamo il prezzo attuale
    tick = mt5_prop.symbol_info_tick(symbol)
    if not tick:
        print(f"Tick non disponibile per {symbol}")
        return

    # Se la posizione era un BUY (type=0), per chiuderla serve un ordine di tipo SELL
    # Se la posizione era un SELL (type=1), per chiuderla serve un ordine di tipo BUY
    price = tick.bid if direction == 0 else tick.ask
    order_type = mt5_prop.ORDER_TYPE_SELL if direction == 0 else mt5_prop.ORDER_TYPE_BUY
    #type_filling = get_type_filling(mt5_prop, mt5_prop.symbol_info(symbol))
    close_request = {
        "action": mt5_prop.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "position": ticket,
        "price": price,
        "deviation": 0,
        #"type_filling": type_filling
    }

    # Inviamo la richiesta di chiusura
    result = mt5_prop.order_send(close_request)
    if result is None or result.retcode != mt5_prop.TRADE_RETCODE_DONE:
        print(f"Errore chiusura posizione su PROP. Retcode: {result.retcode if result else 'No result'}")
        return

    print(f"Chiusura dell'ultima posizione PROP avvenuta con successo (Ticket: {ticket}).")
    return


def close_last_broker_position():
    # Ottiene tutte le posizioni aperte sul conto broker
    positions = mt5_broker.positions_get()
    if not positions:
        print("Nessuna posizione aperta sul conto broker.")
        return

    # Se ci sono posizioni, prendiamo l'ultima (in ordine di elenco)
    last_position = positions[-1]

    symbol = last_position.symbol
    volume = last_position.volume
    ticket = last_position.ticket
    direction = last_position.type  # 0=buy, 1=sell

    # Otteniamo il prezzo attuale
    tick = mt5_broker.symbol_info_tick(symbol)
    if not tick:
        print(f"Tick non disponibile per {symbol}")
        return

    # Se la posizione era un BUY (type=0), per chiuderla serve un ordine di tipo SELL
    # Se la posizione era un SELL (type=1), per chiuderla serve un ordine di tipo BUY
    price = tick.bid if direction == 0 else tick.ask
    order_type = mt5_broker.ORDER_TYPE_SELL if direction == 0 else mt5_broker.ORDER_TYPE_BUY
    #type_filling = get_type_filling(mt5_broker, mt5_broker.symbol_info(symbol))

    close_request = {
        "action": mt5_broker.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "position": ticket,
        "price": price,
        "deviation": 0,
        #"type_filling": type_filling
    }

    # Inviamo la richiesta di chiusura
    result = mt5_broker.order_send(close_request)
    if result is None or result.retcode != mt5_broker.TRADE_RETCODE_DONE:
        print(f"Errore chiusura posizione su broker. Retcode: {result.retcode if result else 'No result'}")
        return

    print(f"Chiusura dell'ultima posizione broker avvenuta con successo (Ticket: {ticket}).")
    return

def start_monitoring_prop_positions():
    """
    Thread che periodicamente controlla se su 'prop' ci sono ancora posizioni aperte.
    Se non ce ne sono più, chiude tutte le posizioni del broker.
    """
    def monitor():
        while True:
            # recupera posizioni aperte su prop
            prop_positions = mt5_prop.positions_get()
            if not prop_positions:
                print("Prop: nessuna posizione aperta -> chiudo tutte le posizioni su broker.")
                close_all_broker_positions()
                break  # esci dal loop, eventualmente puoi anche "ripetere" se vuoi
            time.sleep(0.5)  # ogni quanti secondi controllare

    t = threading.Thread(target=monitor, daemon=True)
    t.start()
