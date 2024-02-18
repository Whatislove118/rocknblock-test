from django.db import models
import shortuuid

def generate_unique_hash() -> str:
    return shortuuid.ShortUUID().random(length=20)

class TokenModel(models.Model):
    unique_hash = models.TextField(null=False, blank=False, unique=True, default=generate_unique_hash)
    # по тз обьект вначале сохраняется, а потом в него записывается tx_hash
    # по этому данное поле может быть null
    tx_hash = models.TextField(null=True, blank=True) 
    media_url = models.URLField(null=False, blank=False, unique=True)
    owner = models.CharField(max_length=42, null=False, blank=False)