from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Person, Place, User
from .serializers import LoginSerializer, PersonSerializer, PlaceSerializer, UserSerializer
from django.contrib.auth.hashers import make_password, check_password


class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        repassword = request.data.get("repassword")

        if not username or not email or not password or not repassword:
            return Response({"error": "Бүх талбаруудыг бөглөнө үү"}, status=status.HTTP_400_BAD_REQUEST)

        if password != repassword:
            return Response({"error": "Нууц үг таарахгүй байна"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username is already taken
        try:
            existing_user = User.nodes.filter(username=username).first()
        except User.DoesNotExist:
            existing_user = None  # If no user exists, safely set it to None

        if existing_user:  # Check if a user already exists
            return Response({"error": "Ийм нэртэй хэрэглэгч аль хэдийн бүртгэгдсэн байна"}, status=status.HTTP_400_BAD_REQUEST)

        # Create user with serializer
        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            user = user_serializer.save()

            # Create corresponding Person node
            person_data = {
                "name": username,  # Using username as default first name
                "birthdate": "2000-01-01",  # Default birthdate
                "gender": "Эр",  # Default gender
                "namtar": "",
            }
            person_serializer = PersonSerializer(data=person_data)

            if person_serializer.is_valid():
                person = person_serializer.save()

                # Link the user to the person
                user.created_people.connect(person)

                return Response(
                    {
                        "message": "Бүртгэл амжилттай!",
                        "element_id": user.get_element_id(),
                        "person_id": person.get_element_id(),
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access to registration
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = User.nodes.filter(username=username).first()
            if user and check_password(password, user.password):
                # Generate a simple token (you might want to use JWT or another token system in production)
                token = f"{user.get_element_id()}:{username}"  # Simple token format
                return Response(
                    {
                        "message": "Login successful", 
                        "element_id": user.get_element_id(),
                        "token": token
                    },
                    status=status.HTTP_200_OK
                )
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 🟢 List & Create Persons
class UpdatePersonView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is logged in

    def put(self, request, person_id):
        try:
            person = Person.nodes.get_or_none(uid=person_id)  # Fetch by unique identifier
            if not person:
                return Response({"error": "Хүн олдсонгүй"}, status=status.HTTP_404_NOT_FOUND)

            serializer = PersonSerializer(person, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Мэдээлэл шинэчлэгдлээ", "person": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Серверийн алдаа: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Make sure user is authenticated

    def get(self, request):
        try:
            person = request.user.created_people.first()  # Ensure you're fetching the correct person
            if not person:
                return Response({"error": "Person information not found"}, status=status.HTTP_404_NOT_FOUND)
            person_serializer = PersonSerializer(person)
            return Response({"profile": person_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            person = request.user.created_people.first()  # Ensure the correct person is fetched
            if not person:
                return Response({"error": "Person information not found"}, status=status.HTTP_404_NOT_FOUND)

            person_serializer = PersonSerializer(person, data=request.data, partial=True)
            if person_serializer.is_valid():
                person_serializer.save()
                return Response({"message": "Profile updated successfully", "profile": person_serializer.data}, status=status.HTTP_200_OK)
            return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
