import graphene
from graphene_django import DjangoObjectType

from modern_catalog.programs.models import Program, Section, Activity


class ProgramType(DjangoObjectType):
    class Meta:
        model = Program
        fields = ("id", "name", "sections")


class SectionType(DjangoObjectType):
    class Meta:
        model = Section
        fields = ("id", "name", "activities")


class ActivityType(DjangoObjectType):
    class Meta:
        model = Activity
        fields = ("id", "name")


class Query(graphene.ObjectType):
    all_sections = graphene.List(SectionType)
    all_activities = graphene.List(ActivityType)
    program_by_name = graphene.Field(ProgramType, name=graphene.String(required=True))

    def resolve_all_sections(root, info):
        # We can easily optimize query count in the resolve method
        return Section.objects.select_related("program").all()

    def resolve_all_activities(root, info):
        # We can easily optimize query count in the resolve method
        return Activity.objects.select_related("section").all()

    def resolve_program_by_name(root, info, name):
        try:
            return Program.objects.get(name=name)
        except Program.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
