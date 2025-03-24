from neomodel import StructuredNode, StructuredRel, StringProperty, DateProperty, IntegerProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty
from django.db import models

class MarriageRel(StructuredRel):
    date = DateProperty()  # Marriage date

class UrgiinOvog(StructuredNode):
    urgiinovog = StringProperty(required=True)  # Clan name (e.g., Боржигон, Чонос)
    def get_element_id(self):
        return self.element_id

class Person(StructuredNode):
    lastname = StringProperty()
    name = StringProperty(required=True)
    gender = StringProperty(choices={"Эр", "Эм"}, required=True)
    birthdate = DateProperty(required=True)  # Must have a birthdate
    diedate = DateProperty(default=None, required=False)  # Can be null
    zurag = models.ImageField(upload_to='zurag/', blank=True, null=True)
    намтар = StringProperty()
    createdate = DateProperty()
    modifydate = DateProperty()

    # Relationships
    spouse = RelationshipTo('Person', 'НӨХӨР')  # Husband/Wife relationship
    child = RelationshipTo('Person', 'ЭХ')  # Parent-Child relationship
    born_in = RelationshipTo('Place', 'ТӨРСӨН')  # Birthplace relationship
    married = RelationshipTo('Person', 'ГЭРЛЭСЭН', model=MarriageRel)  # Marriage relationship with date
    generation = RelationshipTo('Uye', 'БАЙДАГ')  # Relationship to generation
    created_by = RelationshipFrom('User', 'БҮРТГЭСЭН')  # Created by User
    modified_by = RelationshipFrom('User', 'ЗАСВАРЛАСАН')  # Modified by User
    urgiinovog = RelationshipTo('UrgiinOvog', 'ХАРЬЯЛАГДДАГ')  # Clan relationship
    def get_element_id(self):
        return self.element_id
class Place(StructuredNode):
    name = StringProperty()
    country = StringProperty()
    def get_element_id(self):
        return self.element_id

class Uye(StructuredNode):
    uyname = StringProperty(required=True)
    level = IntegerProperty(required=True)
    # Relationships
    persons = RelationshipFrom('Person', 'ХАРЪЯАЛАГДАНА')
    def get_element_id(self):
        return self.element_id

class User(StructuredNode):
    uid = UniqueIdProperty()  # Changed 'id' to 'uid'
    username = StringProperty(required=True)
    email = StringProperty(required=True)
    password = StringProperty(required=True)

    # Relationships
    created_people = RelationshipTo('Person', 'БҮРТГЭСЭН')  # Users can create multiple people
    family_trees = RelationshipTo('UserFamilyTree', 'HAS_FAMILY_TREE')  # User can have one or more family trees
    def get_element_id(self):
        return self.element_id 

class UserFamilyTree(StructuredNode):
    root_person = RelationshipTo('Person', 'MANAGES', cardinality=1)
    user = RelationshipFrom('User', 'HAS_FAMILY_TREE', cardinality=1)
    name = StringProperty()
    description = StringProperty()
    def get_element_id(self):
        return self.element_id
