import asyncio
import time

from starknet_py.net.client_models import Call
from starknet_py.hash.selector import get_selector_from_name

from modules.base_classes.base_account import BaseAccount
from modules.config import SETTINGS_PATH, SETTINGS 
from modules.utils.utils import sleeping, get_pair_for_address_from_file
from modules.utils.logger import logger


STRK_CONTRACT_ADDRESS = 0x04718f5a0fc34cc1af16a1cdee98ffb20c31f5cd61d6ab07201858f4287c938d
VSTRK_CONTRACT_ADDRESS = 0x0782f0ddca11d9950bc3220e35ac82cf868778edb67a5e58b39838544bc4cd0f

class Delegator:

    def get_lock_call(self, amount: float, sender: BaseAccount):

        call = Call(
            STRK_CONTRACT_ADDRESS,
            get_selector_from_name('lock_and_delegate'),
            [
                sender.stark_native_account.address,
                int(amount * 1e18), 0
            ]
        )
        return call
    
    def get_delegate_call(self):
        call = Call(
            VSTRK_CONTRACT_ADDRESS,
            get_selector_from_name('delegate'),
            [0x3c86520094a9c74c6c88b6e41711cb2f51b68edee8a8a9aa5fffcbc5ae336b8]
        )
        
        return call

    async def get_lock_and_delegate_txn(self, sender: BaseAccount):
        lock = SETTINGS["lock"]
        delegate = SETTINGS["delegate"]
        amount = SETTINGS["amount"]
        if lock and delegate:
            call1 = self.get_lock_call(amount, sender)
            call2 = self.get_delegate_call()
            await sender.send_txn_starknet([call1, call2])
    
            return
        if lock:
            call1 = self.get_lock_call(amount, sender)
            await sender.send_txn_starknet([call1])
            return
        if delegate:
            call2 = self.get_delegate_call()

            await sender.send_txn_starknet([call2])
            return



