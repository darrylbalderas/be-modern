from modern_catalog.programs.models import Activity, Section
from modern_catalog.programs.types import ActivityType
import graphene


class ProgramInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    description = graphene.String()


class SectionInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    name = graphene.String()
    description = graphene.String()
    order_index = graphene.Int()
    overview_image = graphene.String()
    programs = graphene.List(ProgramInput)


class ActivityInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    content = graphene.String()
    sections = graphene.List(SectionInput)


class CreateActivity(graphene.Mutation):
    class Arguments:
        input = ActivityInput(required=True)

    ok = graphene.Boolean()
    activity = graphene.Field(ActivityType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        sections = []
        for section in input.sections:
            try:
                section = Section.objects.get(pk=section.id)
            except Section.DoesNotExist:
                return CreateActivity(ok=False, activity=None)
            sections.append(section)
        activity_instance = Activity(name=input.name, content=input.content)
        activity_instance.save()
        activity_instance.sections.set(sections)
        return CreateActivity(ok=ok, activity=activity_instance)


class UpdateActivity(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ActivityInput(required=True)

    ok = graphene.Boolean()
    activity = graphene.Field(ActivityType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        activity_instance = Activity.objects.get(pk=id)
        if activity_instance:
            ok = True
            activity_instance.content = input.content
            activity_instance.name = input.name
            activity_instance.save()
            return UpdateActivity(ok=ok, Activity=activity_instance)
        return UpdateActivity(ok=ok, Activity=None)


class DeleteActivity(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    activity = graphene.Field(ActivityType)

    @staticmethod
    def mutate(root, info, id):
        try:
            activity_instance = Activity.objects.get(pk=id)
        except Activity.DoesNotExist:
            return DeleteActivity(ok=False, activity=None)
        activity_instance.delete()
        activity_instance.id = id
        return DeleteActivity(ok=True, activity=activity_instance)
