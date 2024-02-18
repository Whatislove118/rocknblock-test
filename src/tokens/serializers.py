from rest_framework.serializers import ModelSerializer

from tokens.models import TokenModel


class TokenCreateSerializer(ModelSerializer):
    
    class Meta:
        model = TokenModel
        fields = ["media_url", "owner"]

class TokenDetailSerializer(ModelSerializer):
    
    class Meta:
        model = TokenModel
        fields = "__all__"