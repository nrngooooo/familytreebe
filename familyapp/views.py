import logging
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from .models import Person, Place, User
from .serializers import PersonSerializer, PlaceSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            # Create and save the user
            user = serializer.save()  # Saves the user using the custom serializer's create method
            
            # Return the created user data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
logger = logging.getLogger(__name__)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')

        if not username_or_email or not password:
            return Response({'detail': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        try:
            # Check if the input is email or username
            if '@' in username_or_email:
                user = User.nodes.filter(email=username_or_email).first()  # Check user by email
            else:
                user = authenticate(username=username_or_email, password=password)  # Check user by username

            if user is None:
                return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

            # Create refresh token using the user's element_id
            refresh = RefreshToken.for_user(user)

            # Explicitly set user_id as element_id for the refresh token if necessary
            refresh.user_id = user.element_id  # Ensure you are using element_id here

            access_token = str(refresh.access_token)
            return Response({'access': access_token}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error in LoginView: {str(e)}")
            return Response({'detail': 'An internal server error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
