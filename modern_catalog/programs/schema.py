from modern_catalog.programs.types import ActivityType, ProgramType, SectionType
from modern_catalog.programs.mutations import CreateActivity, CreateProgram
from modern_catalog.programs.mutations import DeleteProgram, UpdateProgram
from modern_catalog.programs.mutations import DeleteActivity, DeleteSection
from modern_catalog.programs.mutations import UpdateActivity, CreateSection
import graphene
from modern_catalog.programs.models import Program, Section, Activity


class Query(graphene.ObjectType):
    section = graphene.Field(SectionType, id=graphene.Int())
    activity = graphene.Field(ActivityType, id=graphene.Int())
    program = graphene.Field(ProgramType, id=graphene.Int())
    sections = graphene.List(SectionType)
    activities = graphene.List(ActivityType)
    programs = graphene.List(ProgramType)

    def resolve_sections(root, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Section.objects.all().order_by('order_index')

    def resolve_activities(root, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Activity.objects.all()

    def resolve_programs(root, info, **kwargs):
        return Program.objects.all()

    def resolve_activity(root, info, **kwargs):
        id = kwargs.get('id')
        try:
            return Activity.objects.get(pk=id)
        except Activity.DoesNotExist:
            return None

    def resolve_section(root, info, **kwargs):
        id = kwargs.get('id')

        try:
            return Section.objects.get(pk=id)
        except Section.DoesNotExist:
            return None

    def resolve_program(root, info, **kwargs):
        id = kwargs.get('id')

        try:
            return Program.objects.get(pk=id)
        except Program.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    create_activity = CreateActivity.Field()
    update_activity = UpdateActivity.Field()
    delete_activity = DeleteActivity.Field()
    create_section = CreateSection.Field()
    delete_section = DeleteSection.Field()
    create_program = CreateProgram.Field()
    delete_program = DeleteProgram.Field()
    update_program = UpdateProgram.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
