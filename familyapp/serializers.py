from rest_framework import serializers
from .models import Person, Place, Uye, UrgiinOvog, User

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
class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        return User(**validated_data).save()
    
class UyeSerializer(serializers.Serializer):    
    class Meta:
        model = Uye
        fields = '__all__'

    def create(self, validated_data):
        return Uye(**validated_data).save()
    
