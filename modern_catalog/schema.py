import graphene

from modern_catalog.programs import schema as programs_schema


class Query(programs_schema.Query, graphene.ObjectType):
    pass


class Mutation(programs_schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
