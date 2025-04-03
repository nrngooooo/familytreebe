from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Person, Place, Uye, UrgiinOvog, User
from django.core.files.storage import default_storage

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repassword = serializers.CharField(write_only=True)  # Added confirm password
    element_id = serializers.CharField(read_only=True)

    def validate(self, data):
        """Ensure password and repassword match."""
        if data['password'] != data['repassword']:
            raise serializers.ValidationError({"repassword": "Нууц үг таарахгүй байна!"})
        return data

    def create(self, validated_data):
        """Remove repassword field before saving."""
        validated_data.pop('repassword')  
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        user = User(**validated_data)
        user.save()  
        return user
    def update(self, instance, validated_data):
        # Update the user instance
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

# 🟢 Person Serializer
class PersonSerializer(serializers.Serializer):  # ✅ Correct for Neo4j nodes
    lastname = serializers.CharField(max_length=255, required=False, default="Нэргүй")
    name = serializers.CharField(max_length=255, required=True)
    birthdate = serializers.DateField()
    deathdate = serializers.DateField(allow_null=True, required=False)
    gender = serializers.CharField(max_length=50)
    namtar = serializers.CharField(allow_blank=True)
    image = serializers.ImageField(required=False)  # Accept image upload

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        image_url = None

        if image:
            image_path = f"uploads/{image.name}"
            default_storage.save(image_path, image)  # ✅ Save image to media/uploads/
            image_url = default_storage.url(image_path)  # ✅ Get URL

        # ✅ Create a new person node
        person = Person(**validated_data)
        if image_url:
            person.image_url = image_url
        person.save()  # ✅ Save Neo4j node

        return person

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)
        if image:
            image_path = f"uploads/{image.name}"
            default_storage.save(image_path, image)
            instance.image_url = default_storage.url(image_path)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

# 🟢 Place Serializer
class PlaceSerializer(serializers.Serializer):
    class Meta:
        model = Place
        fields = '__all__'

    def create(self, validated_data):
        return Place(**validated_data).save()

# 🟢 UrgiinOvog Serializer
class UrgiinOvogSerializer(serializers.Serializer):
    class Meta:
        model = UrgiinOvog
        fields = '__all__'

    def create(self, validated_data):
        return UrgiinOvog(**validated_data).save()
    
# 🟢 User Serializer

class UyeSerializer(serializers.Serializer):    
    class Meta:
        model = Uye
        fields = '__all__'

    def create(self, validated_data):
        return Uye(**validated_data).save()
    
