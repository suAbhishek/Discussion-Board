from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.models import User
# from django.http import HttpResponse
# Create your views here.
from django.http import Http404
from .models import Board, Topic, Post
from .forms import NewTopicForm


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, pk):  # pk --- unique identifier for a item in a model
    try:
        boards = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404
    return render(request, 'topics.html', {'boards': boards})


def new_topic(request, pk):
    boards = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # to get currrently logged in User
    # post = Post()
    if (request.method == 'POST'):
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = boards
            topic.starter = user
            topic.save()

            post = Post.objects.create(message=form.cleaned_data.get('message'), topic=topic, created_by=user)

            return redirect('board_topics', pk=boards.pk)

    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': boards, 'form': form})
