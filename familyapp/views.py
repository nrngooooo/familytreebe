from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person, Place, User
from .serializers import PersonSerializer, PlaceSerializer, UserSerializer

# 🟢 List & Create Persons
class PersonListCreateView(APIView):
    def get(self, request):
        persons = Person.nodes.all()  # Get all Persons
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# 🟢 Retrieve, Update, Delete Person
class PersonDetailView(APIView):
    def get_object(self, pk):
        return Person.nodes.get_or_none(id=pk)

    def get(self, request, pk):
        person = self.get_object(pk)
        if not person:
            return Response({"error": "Not Found"}, status=404)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    def put(self, request, pk):
        person = self.get_object(pk)
        if not person:
            return Response({"error": "Not Found"}, status=404)
        serializer = PersonSerializer(person, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        person = self.get_object(pk)
        if not person:
            return Response({"error": "Not Found"}, status=404)
        person.delete()
        return Response({"message": "Deleted Successfully"}, status=204)

# 🟢 List & Create Places
class PlaceListCreateView(APIView):
    def get(self, request):
        places = Place.nodes.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# 🟢 List & Create Users
class UserListCreateView(APIView):
    def get(self, request):
        users = User.nodes.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
