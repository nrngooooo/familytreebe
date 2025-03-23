from neomodel import StructuredNode, StringProperty, DateProperty, IntegerProperty, RelationshipTo, RelationshipFrom
from django.db import models

class Person(StructuredNode):
    lastname = StringProperty()
    name = StringProperty(required=True)
    gender = StringProperty(choices={"Эр", "Эм"}, required=True)
    birthdate = DateProperty()
    diedate = DateProperty()
    zurag = models.ImageField(upload_to='zurag/', blank=True, null=True)
    намтар = StringProperty()
    createdate = DateProperty()
    modifydate = DateProperty()

    # Relationships
    spouse = RelationshipTo('Person', 'НӨХӨР')  # Husband/Wife relationship
    child = RelationshipTo('Person', 'ЭХ')       # Parent-Child relationship
    born_in = RelationshipTo('Place', 'ТӨРСӨН')  # Birthplace relationship
    married = RelationshipTo('Person', 'ГЭРЛЭСЭН')  # Marriage relationship
    generation = RelationshipTo('Uye', 'БАЙДАГ')  # Relationship to generation


class UrgiinOvog(StructuredNode):
    urgiinovog = StringProperty()


class Place(StructuredNode):
    name = StringProperty()
    country = StringProperty()

class User(StructuredNode):
    username = StringProperty()
    email = StringProperty()
    password = StringProperty()

class Uye(StructuredNode):
    uyname = StringProperty(required=True)  # Name of the generation
    level = IntegerProperty(required=True)  # Level: 0=Self, 1=Father, 1=Mother, 2=Grandfather, 2=Grandmother, etc.

    # Relationships
    persons = RelationshipFrom('Person', 'ХАРЪЯАЛАГДАНА')  # Relationship to persons in this generation