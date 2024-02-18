from django.urls import path

from tokens.views import TokenViewSet

urlpatterns = [
    path("list", TokenViewSet.as_view({"get": "list"})),
    path("create", TokenViewSet.as_view({"post": "create"})),
    path("total_supply", TokenViewSet.as_view({"get": "get_total_supply"})),
]
