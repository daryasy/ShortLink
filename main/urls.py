from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="main_short_link"),
    path('links/', views.show_all_links, name="all_links"),
    path('created/<int:link_id>/', views.created, name="created"),
    path('<str:link_hash>/', views.redirect_link, name="redirect_link"),

]
