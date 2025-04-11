import graphene


class TokenBaseGraph(graphene.ObjectType):
    access_token = graphene.String()
    refresh_token = graphene.String()