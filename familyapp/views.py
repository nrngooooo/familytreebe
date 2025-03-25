from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Person, Place, User
from .serializers import LoginSerializer, PersonSerializer, PlaceSerializer, UserSerializer
from django.contrib.auth.hashers import make_password, check_password

class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access to registration
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        repassword = request.data.get("repassword")

        if not username or not email or not password or not repassword:
            return Response({"error": "Бүх талбаруудыг бөглөнө үү"}, status=status.HTTP_400_BAD_REQUEST)

        if password != repassword:
            return Response({"error": "Нууц үг таарахгүй байна"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Бүртгэл амжилттай!", "element_id": user.get_element_id()},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access to registration
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = User.nodes.filter(username=username).first()
            if user and check_password(password, user.password):
                return Response(
                    {"message": "Login successful", "element_id": user.get_element_id()},
                    status=status.HTTP_200_OK
                )
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
