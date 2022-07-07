from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry_content>", views.entry, name = "entry"),
    path("search", views.search , name= "search")
]
