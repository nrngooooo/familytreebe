from django.contrib.auth.hashers import make_password, check_password
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
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        
        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])  # Always hash updated password
        instance.save()
        return instance
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.nodes.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Хэрэглэгч олдсонгүй!")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Нууц үг буруу байна!")

        data['user'] = user
        return data

# 🟢 Person Serializer

class PersonSerializer(serializers.Serializer):
    name = serializers.CharField()
    lastname = serializers.CharField(required=False)
    gender = serializers.ChoiceField(choices=["Эр", "Эм"])
    birthdate = serializers.DateField()
    diedate = serializers.DateField(required=False, allow_null=True)
    image_url = serializers.CharField(required=False)
    biography = serializers.CharField(required=False)
    element_id = serializers.CharField(read_only=True)

    def create(self, validated_data):
        person = Person(**validated_data)
        person.save()
        return person

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
class RelationshipSerializer(serializers.Serializer):
    from_person_id = serializers.CharField()
    to_person_id = serializers.CharField()
    relationship_type = serializers.ChoiceField(choices=[
        "ЭЦЭГ", "ЭХ", "ХҮҮХЭД", "АХ","ЭГЧ","ДҮҮ", "ГЭР БҮЛ", "ӨВӨӨ", "ЭМЭЭ", "ТӨРСӨН", "ХАМААРНА", "ХАРЬЯЛАГДДАГ", "БҮРТГЭСЭН", "ЗАСВАРЛАСАН"
    ])
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
    
