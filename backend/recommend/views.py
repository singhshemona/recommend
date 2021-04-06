from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookSerializer
from .models import Book
from django.http import HttpResponse

# Create your views here.

# def index(response, id):
# 	ls = ToDoList.objects.get(id=id)
# 	return render(response, "recommend/list.html", {"ls":ls})

def home(response):
	return render(response, "recommend/home.html", {})
class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

def bookClassifyView(request):
    link = 'http://classify.oclc.org/classify2/Classify?owi=5418887444'
    return HttpResponse(link)
