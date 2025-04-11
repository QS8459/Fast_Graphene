import graphene


class BaseInterface(graphene.Interface):
    guid = graphene.UUID(required=True)
    created_at = graphene.DateTime(required=True)
    updated_at = graphene.DateTime(required=True)