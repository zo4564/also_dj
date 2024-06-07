
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import upload_sim_data

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:species_id>/", views.detail, name="detail"),
    path("<int:species_id>/vote/", views.vote, name="vote"),
    path("species_list/", views.species_list, name="species_list"),
    path("rules/", views.rules, name="rules"),
    path("play/", views.play, name="play"),
    path("about/", views.about, name="about"),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user_page/', views.user_page, name='user_page'),
    path('upload_sim_data/', upload_sim_data, name='upload_sim_data'),
    path('add/', views.add_species, name='add_species'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
