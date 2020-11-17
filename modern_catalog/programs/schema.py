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
    section = graphene.Field(SectionType, id=graphene.Int())
    activity = graphene.Field(ActivityType, id=graphene.Int())
    program = graphene.Field(ProgramType, id=graphene.Int())
    sections = graphene.List(SectionType)
    activities = graphene.List(ActivityType)
    programs = graphene.List(ProgramType)

    def resolve_sections(root, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Section.objects.select_related("program").all().order_by('order_index')

    def resolve_activities(root, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Activity.objects.select_related("section").all()

    def resolve_programs(root, info, **kwargs):
        return Program.objects.all()

    def resolve_activity(root, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Activity.objects.get(pk=id)
        return None

    def resolve_section(root, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Section.objects.get(pk=id)
        return None

    def resolve_program(root, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Program.objects.get(pk=id)
        return None
        # try:
        #     return Program.objects.get(name=name)
        # except Program.DoesNotExist:
        #     return Program.objects.none()


schema = graphene.Schema(query=Query)
