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



# class DeweyView(viewsets.ModelViewSet):
#     serializer_class = DeweyDecimalLink
#     queryset = DeweyDecimalLink.objects.all()


# take user's book title input and attach to the base url to display search result link
def deweyDecimalLink(request):

    # Search by title
    base = 'http://classify.oclc.org/classify2/Classify?'
    parmType = 'title'
    parmValue = request.GET.get('q')
    searchURL = base + urlencode({parmType:parmValue.encode('utf-8')})
    # http://classify.oclc.org/classify2/Classify?title=into+the+wild
    # http://127.0.0.1:8000/bookclassify/?q=into+the+wild

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



    # jsonDict = {}
    # jsonDict["works"] = jsonContent.get('classify')

    # result = []
    # for item in jsonContent:
    #     my_dict = {}
    #     my_dict['owi']=item.get("classify").get
    #     result.append(my_dict)
    # back_json=json.dumps(jsonDict)

    # books = jsonContent['work']

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








# fldr = os.path.basename('./bookMockData.json')
'/home/taniya/Projects/bookRec/recommend/backend/recommend'
# fldr = os.path.basename('/recommend/backend/recommend/')
jsonData = 'bookMockData.json'

# __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# f = open(os.path.join(__location__, jsonData))

def showStaticMock(request):

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, jsonData)

    # file = open(mockDataPath)  
    # with open(jsonData) as file:
    #     try:
    #         data = json.load(file)
    #     except:
    #         data = {}  


    with open(my_file) as f:
        data = json.load(f)
    return JsonResponse(data, safe=False)
