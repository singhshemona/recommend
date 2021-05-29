from rest_framework import serializers
from .models import Book
from .models import BookClassify

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "content", "ISBN", "DDC", "date_added", "user")


class DeweyDecimalLink(serializers.ModelSerializer):

    class Meta:
        model = BookClassify
        fields = ("@author", "@editions", "@format", "@holdings", "@hyr", "@itemtype", "@lyr", "@owi", "@schemes", "@title", "@wi")