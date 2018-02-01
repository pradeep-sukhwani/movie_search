from django.conf.urls import url
from .views import index, home_page, get_existing_movie_id


urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^home/$', home_page, name='home-page'),
    url(r'^get-existing-movie-id/$', get_existing_movie_id, name='get-existing-movie-id'),
]
