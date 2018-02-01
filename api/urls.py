from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^movie-search/$', views.MovieSearch.as_view(), name="movie-search"),
    url(r'^movie-save/$', views.SaveMovie.as_view(), name="movie-save"),
    url(r'^user-movie-search/$', views.UserMovieSearch.as_view(), name="user-movie-search"),
]
