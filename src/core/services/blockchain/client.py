from web3 import Web3
from web3.middleware import geth_poa_middleware
from django.conf import settings


__all__ = ["w3"]

w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URI))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

