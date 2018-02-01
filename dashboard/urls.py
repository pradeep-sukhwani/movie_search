from django.conf.urls import url
from .views import index, home_page, add_update_movie_details_modal, delete_movie_id


urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^home/$', home_page, name='home-page'),
    url(r'^add-update-movie-details/$', add_update_movie_details_modal, name='add-update-movie-details'),
    url(r'^delete-movie-id/$', delete_movie_id, name='delete-movie-id'),
]
