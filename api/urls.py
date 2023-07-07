from django.urls import path
from .views import OnePieceCapituloMangaListView

urlpatterns = [
    path('onepiece/', OnePieceCapituloMangaListView.as_view(), name='onepiece-list'),
]
