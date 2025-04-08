import uuid
from rest_framework.response import Response
from rest_framework import status
from neomodel.exceptions import DoesNotExist
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Person, Place, User
from .serializers import LoginSerializer, PersonSerializer, PlaceSerializer, RelationshipSerializer, UserSerializer
from .authentication import UUIDTokenAuthentication
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access to registration
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate a new token using UUID
            token = str(uuid.uuid4())
            user.token = token
            user.save()

            return Response({
                "message": "Амжилттай нэвтэрлээ!",
                "uid": user.uid,
                "username": user.username,
                "email": user.email,
                "element_id": user.element_id,
                "token": token,
            }, status=200)
        return Response(serializer.errors, status=400)
    
# 🟢 List & Create Persons
class ProfileView(APIView):
    authentication_classes = [UUIDTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, uid):
        try:
            user = User.nodes.get(uid=uid)
            person = next(iter(user.created_people.all()), None)  # safer version
            data = {
                "username": user.username,
                "email": user.email,
                "person": PersonSerializer(person).data if person else None
            }
            return Response(data)
        except DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def post(self, request, uid):
        try:
            user = User.nodes.get(uid=uid)
            # Get existing person or create new one
            person = next(iter(user.created_people.all()), None)
            
            serializer = PersonSerializer(data=request.data)
            if serializer.is_valid():
                if person:
                    # Update existing person
                    for attr, value in serializer.validated_data.items():
                        setattr(person, attr, value)
                    person.save()
                else:
                    # Create new person
                    person = Person(**serializer.validated_data)
                    person.save()
                    user.created_people.connect(person)
                
                return Response(PersonSerializer(person).data, status=200)
            return Response(serializer.errors, status=400)
        except DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class PersonCreateView(APIView):
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            person = serializer.save()
            return Response(PersonSerializer(person).data, status=201)
        return Response(serializer.errors, status=400)

class PersonEditView(APIView):
    def put(self, request, element_id):
        try:
            person = Person.nodes.get(element_id=element_id)
        except Person.DoesNotExist:
            return Response({"error": "Person not found"}, status=404)

        serializer = PersonSerializer(person, data=request.data, partial=True)
        if serializer.is_valid():
            person = serializer.save()
            return Response(PersonSerializer(person).data)
        return Response(serializer.errors, status=400)

class AddRelationshipView(APIView):
    def post(self, request):
        serializer = RelationshipSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        from_id = serializer.validated_data['from_person_id']
        to_id = serializer.validated_data['to_person_id']
        rel_type = serializer.validated_data['relationship_type']

        try:
            from_person = Person.nodes.get(element_id=from_id)
            to_person = Person.nodes.get(element_id=to_id)
        except Person.DoesNotExist:
            return Response({"error": "Person not found"}, status=404)

        # Define Neo4j relationship logic
        if rel_type == "ЭЦЭГ":
            from_person.father.connect(to_person)
        elif rel_type == "ЭХ":
            from_person.mother.connect(to_person)
        elif rel_type == "ХҮҮХЭД":
            from_person.children.connect(to_person)
        elif rel_type == "АХ":
            from_person.brothers.connect(to_person)
        elif rel_type == "ЭГЧ":
            from_person.sisters.connect(to_person)
        elif rel_type == "ДҮҮ":
            from_person.youngsiblings.connect(to_person)
        elif rel_type == "ӨВӨӨ":
            from_person.grandfather.connect(to_person)
        elif rel_type == "ЭМЭЭ":
            from_person.grandmother.connect(to_person)
        elif rel_type == "ГЭР БҮЛ":
            from_person.spouse.connect(to_person)
        elif rel_type == "ТӨРСӨН":
            from_person.born_in.connect(to_person)
        elif rel_type == "ХАМААРНА":
            from_person.generation.connect(to_person)
        elif rel_type == "ХАРЬЯЛАГДДАГ":
            from_person.urgiinovog.connect(to_person)
        elif rel_type == "БҮРТГЭСЭН":
            from_person.created_by.connect(to_person)
        elif rel_type == "ЗАСВАРЛАСАН":
            from_person.modified_by.connect(to_person)  
            
        return Response({"message": f"{rel_type} холбоо үүсгэгдлээ."}, status=201)
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

class LogoutView(APIView):
    authentication_classes = [UUIDTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user.token = None
            user.save()
            return Response({"message": "Амжилттай гарлаа"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
