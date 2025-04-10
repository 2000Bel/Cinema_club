from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Movie, Actor
from .forms import MovieForm
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Home(LoginView):
    template_name = 'home.html'

def home(request):
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def movie_index(request):
    movies = Movie.objects.filter(user=request.user)
    return render(request, 'movies/index.html', { 'movies': movies })

@login_required
def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    actors_not_in_movie = Actor.objects.exclude(id__in=movie.actors.all().values_list('id'))
    movie_form = MovieForm()
    return render(request, 'movies/detail.html', {
        'movie': movie,
        'movie_form': movie_form,
        'actors': actors_not_in_movie
})

class MovieCreate(LoginRequiredMixin, CreateView):
    model = Movie
    fields = ['title', 'genre', 'year', 'description', 'poster']

def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class MovieUpdate(LoginRequiredMixin, UpdateView):
    model = Movie
    fields = ['description', 'poster']

class MovieDelete(LoginRequiredMixin, DeleteView):
    model = Movie
    success_url = '/movies/'

class ActorCreate(LoginRequiredMixin, CreateView):
    model = Actor
    fields = ['name', 'bio']

class ActorList(LoginRequiredMixin, ListView):
    model = Actor

class ActorDetail(LoginRequiredMixin, DetailView):
    model = Actor
    template_name = 'actors/detail.html'
    context_object_name = 'actor'

class ActorUpdate(LoginRequiredMixin, UpdateView):
    model = Actor
    fields = ['name', 'bio']

class ActorDelete(LoginRequiredMixin, DeleteView):
    model = Actor
    success_url = '/actors/'
    template_name = 'actors/actor_confirm_delete.html'

@login_required
def associate_actor(request, movie_id, actor_id):
    Movie.objects.get(id=movie_id).actors.add(actor_id)
    return redirect('movie-detail', movie_id=movie_id)

@login_required
def remove_actor(request, movie_id, actor_id):
    movie = Movie.objects.get(id=movie_id)
    actor = Actor.objects.get(id=actor_id)
    movie.actors.remove(actor_id)
    return redirect('movie-detail', movie_id=movie.id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movie-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
