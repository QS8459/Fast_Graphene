import graphene
from uuid import uuid4


mock_data = {
    "characters": [{
        "guid": uuid4(),
        "name": "Mock",
        "surname": "SurMock",
        "type": "user"
    },
    {
        "guid": uuid4(),
        "name": "MockCharacter",
        "surname": "MockCharSurname",
        "type": "other"
    }
    ]
}


class Character(graphene.Interface):
    guid = graphene.UUID(required=True)
    name = graphene.String(required=True)
    surname = graphene.String(required=True)


class User(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)

    @staticmethod
    def is_type_of(value, info):
        return value.get("type") == "user"


class Other(graphene.ObjectType):
    class Meta:
        interfaces =(Character,)
    @staticmethod
    def is_type_of(value, info):
        return value.get('type') == "other"


class Characters(graphene.Union):
    class Meta:
        types = (User, Other)


class SearchResult(graphene.ObjectType):
    characters = graphene.List(Characters)