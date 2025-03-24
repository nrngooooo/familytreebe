from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Person, Place, Uye, UrgiinOvog, User

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # Hash the password before saving
        password = make_password(validated_data['password'])
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password
        )
        user.save()  # Save to Neo4j
        return user

    def update(self, instance, validated_data):
        # Update the user instance
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance
    
# 🟢 Person Serializer
class PersonSerializer(serializers.Serializer):
    class Meta:
        model = Person
        fields = '__all__'

    def create(self, validated_data):
        return Person(**validated_data).save()

    def update(self, instance, validated_data):
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
    
