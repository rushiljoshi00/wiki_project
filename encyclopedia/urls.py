from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #we had to add wiki/ here because before in the search function
    #when we tried to redirect from the home page by typing in the word css, it was conflicting with the /search
    #and whatever we typed in, ex CSS. Before 
    path("wiki/<str:entry_content>", views.entry, name = "entry"),
    path("search", views.search , name= "search"),
    path("random", views.random_function , name= "random"),
    path("create", views.create , name= "create"),
    path("wiki/<str:entry>/edit", views.edit , name= "edit")
]
