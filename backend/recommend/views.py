# from ..backend import wsgi

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookSerializer, DeweyDecimalLink
from .models import Book
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import xml.etree.ElementTree as ET
import xmltodict, json
from urllib.request import urlopen
from urllib.parse import urlencode
from json2table import convert
import json
import os

# Create your views here.


# def index(response, id):
# 	ls = ToDoList.objects.get(id=id)
# 	return render(response, "recommend/list.html", {"ls":ls})

def home(response):
	return render(response, "recommend/home.html", {})
class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()






# isbn to Dewey decimal
def deweyDecimalLink(request):


    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType = 'isbn'
    parmValue = request.GET.get('q')
    searchURL = base + urlencode({parmType:parmValue.encode('utf-8')})

    
    # redirect to OCLC's site to extract XML file of book
    xmlContent = urlopen(searchURL)
    xmlFile = xmlContent.read()
    xmlDict = xmltodict.parse(xmlFile)
    jsonDumps = json.dumps(xmlDict)
    jsonContent = json.loads(jsonDumps)

    # items = jsonContent.get("classify").get('works').get('work')
    base = jsonContent.get("classify").get('editions').get('edition')[0]
    # deweyNumber = base.get('classifications').get('class')[0].get('@sfa')

    # pets_data = open("data.json", "w")
    # json.dump(xmlDict, pets_data)
    # pets_data.close()


    '''
    # Need to searlize the data! Then return JSON
    '''
    return JsonResponse(base, safe=False)





def owiToDDC(request):
    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType = 'title'
    parmValue = None
    searchURL = base + urlencode({parmType:parmValue.encode('utf-8')})
    # http://classify.oclc.org/classify2/Classify?owi=263706&summary=true








jsonData = 'bookMockData.json'
def showStaticMock(request):

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, jsonData)

    with open(my_file) as f:
        data = json.load(f)
    return JsonResponse(data, safe=False)




'''

# Search by title
# take user's book title input and attach to the base url to display search result link
base = 'http://classify.oclc.org/classify2/Classify?'
parmType = 'title'
parmValue = request.GET.get('q')
searchURL = base + urlencode({parmType:parmValue.encode('utf-8')})
# http://classify.oclc.org/classify2/Classify?title=into+the+wild
# http://127.0.0.1:8000/bookclassify/?q=into+the+wild

'''