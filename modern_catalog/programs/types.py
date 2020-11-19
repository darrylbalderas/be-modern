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
