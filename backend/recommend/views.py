# from ..backend import wsgi

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookSerializer
from .models import Book
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
import xml.etree.ElementTree as ET

from urllib.parse import urlencode
# from backend import deweyDecimalScript

# Create your views here.

# def index(response, id):
# 	ls = ToDoList.objects.get(id=id)
# 	return render(response, "recommend/list.html", {"ls":ls})

def home(response):
	return render(response, "recommend/home.html", {})
class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

# def bookClassifyView(request):
#     # linkPrefix = 'http://classify.oclc.org/classify2/Classify?title='
#     # linkPostfix = 'the%20essential%20rumi&summary=true'
#     userTitleInput = 'the essential Rumi'
    
#     linkToBooks = deweyDecimalScript("hello") > 'etext.txt'
#     return HttpResponse(linkToBooks)


# take user's book title input and attach to the base url to display search result link
def deweyDecimalLink(request):
    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType = 'title'
    parmValue = request.GET.get('q')
    searchURL = base + urlencode({parmType:parmValue.encode('utf-8')})
    
    # json = classifyXMLdata(searchURL)
    
    # return json

    redirect = HttpResponseRedirect(searchURL)
    return redirect



def classifyXMLdata(request):

    HttpResponseRedirect(request)

    # bookXML = request.GET.get(request)

