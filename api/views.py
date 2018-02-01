from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import authentication, permissions
from django.core import serializers

from core.models import MovieDetail, Genre


class MovieSearch(APIView):
    # API for movie search
    parser_classes = (JSONParser,)

    def get(self, request):
        data = {}
        request_params = request.query_params
        if request_params.get("search"):
            search_field = request_params.get("search")
            search_field = search_field.title()
            show_details = MovieDetail.objects.filter(
                Q(director__icontains=search_field) | Q(name__icontains=search_field) |
                Q(genre__name__in=[search_field])).distinct()
            if show_details:
                data["show_details"] = serializers.serialize("json", show_details)
                genre_data = {}
                for movie_obj in show_details:
                    genre_data.update(
                        {movie_obj.id: ", ".join([genre_obj.name for genre_obj in movie_obj.genre.all()])})
                data["genre"] = genre_data
                data["success"] = True
            else:
                data["success"] = False
                data["message"] = "Could not find any movie please try again."
        else:
            data["success"] = False
            data["message"] = "Please write something!!"
        return JsonResponse(data)


class UserMovieSearch(APIView):
    # API for movie search for a specific user
    parser_classes = (JSONParser,)

    def get(self, request):
        data = {}
        movie_data = MovieDetail.objects.filter(user__username=request.user.username)
        request_params = request.query_params
        if request_params.get("search"):
            search_field = request_params.get("search")
            search_field = search_field.title()
            show_details = movie_data.filter(Q(director__icontains=search_field) | Q(name__icontains=search_field) |
                                             Q(genre__name__in=[search_field])).distinct()
            if show_details:
                data["show_details"] = serializers.serialize("json", show_details)
                genre_data = {}
                for movie_obj in show_details:
                    genre_data.update(
                        {movie_obj.id: ", ".join([genre_obj.name for genre_obj in movie_obj.genre.all()])})
                data["genre"] = genre_data
                data["success"] = True
            else:
                data["success"] = False
                data["message"] = "Could not find any movie please try again."
        else:
            data["success"] = False
            data["message"] = "Please write something!!"
        return JsonResponse(data)


class SaveMovie(APIView):
    # Checks whether it's a new movie to create or update existing movie details for a specific user
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = {}
        movie_data = MovieDetail.objects.filter(user__username=request.user.username)
        post_request_data = request.POST
        name = post_request_data.get("movie_name")
        genre = post_request_data.getlist("genre")
        director_name = post_request_data.get("director_name")
        popularity = post_request_data.get("popularity")
        imdb_score = post_request_data.get("imdb_score")
        if post_request_data.get("movie_id"):
            movie_data = movie_data.get(id=post_request_data.get("movie_id"))
        else:
            movie_data = MovieDetail()
            movie_data.user = User.objects.get(username=request.user.username)
        movie_data.name = name
        movie_data.popularity = float(popularity)
        movie_data.score = float(imdb_score)
        movie_data.director = director_name
        movie_data.save()
        for genre_id in genre:
            try:
                movie_data.genre.add(Genre.objects.get(id=int(genre_id)))
            except:
                pass
        data["success"] = True
        return Response(data)


class DeleteMovie(APIView):
    # Delete movie details for a specific user
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = {}
        try:
            MovieDetail.objects.get(id=int(request.POST.get("movie_id")), user__username=request.user.username).delete()
            data["success"] = True
        except:
            data["success"] = False
            data["message"] = "That movie detail does not exist please refresh the page"
        return Response(data)
