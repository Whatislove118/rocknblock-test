from django.conf import settings
from web3 import Web3

from core.services.blockchain.client import w3


class ContractManager:
    def __init__(
        self,
        abi: str = settings.CONTRACT_ABI,
        address: str = settings.CONTRACT_ADDRESS,
        wallet_private_key: str = settings.WALLET_PRIVATE_KEY,
        w3: Web3 = w3,
    ) -> None:
        self.w3 = w3
        self.contract = w3.eth.contract(address=address, abi=abi)  # type: ignore
        self.wallet_private_key = wallet_private_key

    def get_total_supply(self) -> int:
        """Возвращает число токенов в сети."""
        return self.contract.functions.totalSupply().call()

    def send_token(self, owner: str, unique_hash: str, media_url: str) -> str:
        """Создает транзакцию по токены и возвращает хэш транзакции."""
        nonce = w3.eth.get_transaction_count(owner)  # type: ignore
        tx = self.contract.functions.mint(
            owner,
            unique_hash,
            media_url,
        ).build_transaction({"nonce": nonce})
        signed_tx = self.w3.eth.account.sign_transaction(
            tx,
            private_key=self.wallet_private_key,
        )
        return w3.eth.send_raw_transaction(signed_tx.rawTransaction).hex()
