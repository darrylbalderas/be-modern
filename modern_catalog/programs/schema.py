import graphene
from graphene_django import DjangoObjectType
from modern_catalog.programs.models import Program, Section, Activity


class ProgramType(DjangoObjectType):
    class Meta:
        model = Program
        fields = "__all__"


class SectionType(DjangoObjectType):
    class Meta:
        model = Section
        fields = "__all__"


class ActivityType(DjangoObjectType):
    class Meta:
        model = Activity
        fields = "__all__"


class Query(graphene.ObjectType):
    sections = graphene.List(SectionType)
    activities = graphene.List(ActivityType)
    programs = graphene.List(ProgramType)
    program_by_name = graphene.Field(ProgramType, name=graphene.String(required=True))

    def resolve_sections(root, info):
        # We can easily optimize query count in the resolve method
        return Section.objects.select_related("program").all().order_by('order_index')

    def resolve_activities(root, info):
        # We can easily optimize query count in the resolve method
        return Activity.objects.select_related("section").all()

    def resolve_programs(root, info):
        return Program.objects.all()

    def resolve_program_by_name(root, info, name):
        try:
            return Program.objects.get(name=name)
        except Program.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
