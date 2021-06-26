from rest_framework import serializers
from .models import Book
from .models import BookClassify
from .models import GoodReadsImport
from .models import BooksDisplayed
import io, os ,json
from rest_framework.parsers import JSONParser

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "content", "ISBN", "DDC", "date_added", "user")


class DeweyDecimalLink(serializers.ModelSerializer):

    class Meta:
        model = BookClassify
        fields = ("@author", "@editions", "@format", "@holdings", "@hyr", "@itemtype", "@lyr", "@owi", "@schemes", "@title", "@wi")


class GoodReadsImportSeralizer(serializers.ModelSerializer):
    pass


class BooksDisplayedSerlizer(serializers.ModelSerializer):


     
    class Meta:
        model = BooksDisplayed
        # fields = ("title", "author_first", "author_last", "classify_ISBN", "classify_DDC", "pages", "publish_date", "country", "tags", "date_added", "user")
        fields = "__all__"




