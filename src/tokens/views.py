from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from core.services.blockchain import ContractManager
from tokens.models import TokenModel
from tokens.pagination import TokenListPagination
from tokens.serializers import TokenCreateSerializer, TokenDetailSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema, inline_serializer
from rest_framework.response import Response
from rest_framework import serializers as drf_serializer
from django.db.transaction import atomic


@extend_schema_view(
    create=extend_schema(
        description="Cоздание токена",
        responses={200: TokenDetailSerializer},
    ),
    
)
class TokenViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    queryset = TokenModel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TokenDetailSerializer
    pagination_class = TokenListPagination
    
    def get_serializer_class(self) -> type[BaseSerializer]:
        match self.action:
            case "create":
                return TokenCreateSerializer
        return self.serializer_class

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        serializer = TokenDetailSerializer(instance=serializer.instance)
        return Response(serializer.data, status=201, headers=headers)

    @atomic
    def perform_create(self, serializer: TokenCreateSerializer) -> None:
        super().perform_create(serializer)
        obj: TokenModel = serializer.instance
        manager = ContractManager()
        tx_hash = manager.send_token(owner=obj.owner, unique_hash=obj.unique_hash, media_url=obj.media_url)
        obj.tx_hash = tx_hash
        obj.save(update_fields=["tx_hash"])
        
        
    @extend_schema(
        responses={200: inline_serializer(
            name="TotalSupplySerializer",
            fields={
                "result": drf_serializer.IntegerField()
            }
        )}
    )
    @action(methods=["GET"], detail=False, url_path="total_supply", url_name="total_supply")
    def get_total_supply(self, request, *args, **kwargs):
        manager = ContractManager()
        resp_data = {
            "result": manager.get_total_supply()
        }
        return Response(data=resp_data)