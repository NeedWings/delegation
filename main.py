from time import sleep
from random import shuffle
import asyncio
import pickle
from asyncio import Event
from threading import Thread

import inquirer
from termcolor import colored
from eth_account import Account as ethAccount
from inquirer.themes import load_theme_from_dict as loadth
from starknet_py.net.full_node_client import FullNodeClient

try:
    from modules.utils.utils import get_random_value, get_random_value_int, gas_locker, normalize_to_32_bytes
    from modules.routers.activity.main_router import MainRouter
    from modules.config import autosoft, subs_text, RPC_LIST, SETTINGS_PATH, PUBLIC_KEYS_PAIRS
    from modules.utils.starter import *
    


    def get_action() -> str:
        theme = {
            "Question": {
                "brackets_color": "bright_yellow"
            },
            "List": {
                "selection_color": "bright_blue"
            }
        }

        question = [
            inquirer.List(
                "action",
                message=colored("Choose soft work task", 'light_yellow'),
                choices=[
                    "delegator"
                ],
            )
        ]
        action = inquirer.prompt(question, theme=loadth(theme))['action']
        return action

    def main():
        with open(f"{SETTINGS_PATH}starkstats.csv", "w") as f:
            f.write("address;txn count;ETH balance;USDC balance;USDT balance;DAI balance;WBTC balance;WSTETH balance;LORDS balance;Have liq;Have lend")
        global RPC_LIST
        gas_lock = Event()
        one_thread_lock = Event()

        print(autosoft)
        print(subs_text)
        print("\n")
        f = open(f"{SETTINGS_PATH}to_run_addresses.txt", "r")
        addresses = f.read().lower().split("\n")
        f.close()
        action = get_action()
        if action == "delegator":
            task_number = 1
        for i in range(len(addresses)):
            if len(addresses[i]) < 50:
                addresses[i] = "0x" + "0"*(42-len(addresses[i])) + addresses[i][2::]
            else:
                addresses[i] = "0x" + "0"*(66-len(addresses[i])) + addresses[i][2::]
        if 0:
            pass
        else:    
            private_keys = decode_secrets()
            accounts, counter = transform_keys(private_keys, addresses)
            with open(f"{SETTINGS_PATH}wallets_data.ser", "wb") as f:
                f.write(pickle.dumps(PUBLIC_KEYS_PAIRS))
            print(f"Soft found {counter} keys to work")
            tasks = []

                

            
            print(f"Bot found {counter} private keys to work")
            if SETTINGS["useProxies"]:
                loop = asyncio.new_event_loop()

                f = open(f"{SETTINGS_PATH}proxies.txt", "r")
                proxies_raw = f.read().split("\n")
                f.close()

                proxies = []

                for proxy in proxies_raw:
                    proxies.append(proxy.split("@"))
                if task_number != 10 and task_number != 16:
                    shuffle(proxies)
                proxy_dict = {}
                args = []
                for proxy in proxies:
                    if proxy == "":
                        continue
                    if f"http://{proxy[0]}@{proxy[1]}" in proxy_dict.keys():
                        proxy_dict[f"http://{proxy[0]}@{proxy[1]}"].append(('0x' + '0'*(66-len(proxy[2])) + proxy[2][2::]).lower())
                    else:
                        proxy_dict[f"http://{proxy[0]}@{proxy[1]}"] = [('0x' + '0'*(66-len(proxy[2])) + proxy[2][2::]).lower()]

                counter = 1
                delay = 0
                for proxy in proxy_dict:

                    addresses = proxy_dict[proxy]
                    for key in accounts:
                        address =  Account.get_starknet_address_from_private(key)
                        
                        if address in addresses:
                            print(f"[{address}] connected to proxy: {proxy}")
                            tasks.append(loop.create_task(MainRouter(key, delay, task_number, proxy=proxy).start(gas_lock=gas_lock, one_thread_lock=one_thread_lock)))
                            delay += get_random_value_int(SETTINGS["ThreadRunnerSleep"])
                
            else:
                loop = asyncio.new_event_loop()

                delay = 0
                for account in accounts:
                    tasks.append(loop.create_task(MainRouter(account, delay, task_number).start(gas_lock=gas_lock, one_thread_lock=one_thread_lock)))
                    delay += 0
            #tasks.append(loop.create_task(gas_locker(gas_lock=gas_lock)))

            loop.run_until_complete(asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED))

           
    if __name__ == "__main__":
        while True:
            main()
            input("Soft successfully end work")

except Exception as e:
    console_log.error(f"Unexpected error: {e}")

input("Soft successfully end work")
