from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from core.models import MovieDetail, Genre
import json


def index(request):
    # showing top 10 rated/popular movie details
    movie_data = MovieDetail.objects.filter(Q(popularity__gte=70.0) | Q(score__gte=7.0)).distinct()[:10]
    data = {"movie_data": movie_data}
    return render(request, "index.html", data)


def import_json_data():
    # import script to import movie details from json
    with open("/home/family/movie/imdb.json") as data:  # edit file url as per your json file location
        json_data = json.loads(data.read())
        for count, item in enumerate(json_data):
            if item.get("name"):
                try:
                    detail = MovieDetail.objects.get(name=item.get("name"))
                except MovieDetail.DoesNotExist:
                    detail = MovieDetail.objects.create(name=item.get("name"))
                detail.director = item.get("director")
                detail.user = User.objects.get(email="ps.sukhwani@gmail.com")
                detail.score = item.get("imdb_score")
                detail.popularity = item.get("99popularity")
                detail.save()

                if item.get("genre"):
                    for genre_data in item.get("genre"):
                        # used lstrip() to remove white space from the beginning of every string
                        try:
                            detail.genre.add(Genre.objects.get(name=genre_data.lstrip()))
                        except Genre.DoesNotExist:
                            detail.genre.add(Genre.objects.create(name=genre_data.lstrip()))
                        except:
                            pass
                print("Completed count no. {0} with movie name {1}". format(count, item.get("name")))


def home_page(request):
    # after login it redirects on this page, showing all movie details of that particular user
    movie_data = MovieDetail.objects.filter(user__username=request.user.username).order_by("-created_on")
    data = {"movie_data": movie_data}
    return render(request, "home.html", data)


def get_existing_movie_id(request):
    # opening modal to add new or edit existing movie details of that particular user
    data = {"data_id": False}
    if request.GET.get("id"):
        show_details = MovieDetail.objects.get(id=request.GET.get("id"))
        data["movie_data"] = show_details
        data["selected_genre"] = [genre.id for genre in show_details.genre.all()]
        data["data_id"] = True
    data["genre"] = Genre.objects.all()
    return render(request, "movie_modal.html", data)
