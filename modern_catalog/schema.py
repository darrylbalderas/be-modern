import graphene

from modern_catalog.programs import schema as programs_schema


class Query(programs_schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query)
