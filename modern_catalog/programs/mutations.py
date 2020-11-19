from modern_catalog.programs.models import Activity, Program, Section
from modern_catalog.programs.types import ActivityType, ProgramType, SectionType
import graphene


class ProgramInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    description = graphene.String()


class SectionInput(graphene.InputObjectType):
    id = graphene.ID()
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
        try:
            activity_instance = Activity.objects.get(pk=id)
        except Activity.DoesNotExist:
            return UpdateActivity(ok=False, activity=None)

        if input.content:
            activity_instance.content = input.content

        if input.name:
            activity_instance.name = input.name

        activity_instance.save()

        return UpdateActivity(ok=True, activity=activity_instance)


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


class CreateSection(graphene.Mutation):
    class Arguments:
        input = SectionInput(required=True)

    ok = graphene.Boolean()
    section = graphene.Field(SectionType)

    @staticmethod
    def mutate(root, info, input=None):
        programs = []
        for program in input.programs:
            try:
                program = Program.objects.get(pk=program.id)
            except Program.DoesNotExist:
                return CreateSection(ok=False, activity=None)
            programs.append(program)
        section_instance = Section(name=input.name,
                                   description=input.description,
                                   overview_image=input.overview_image,
                                   order_index=input.order_index)
        section_instance.save()
        section_instance.programs.set(programs)
        return CreateSection(ok=True, section=section_instance)


class DeleteSection(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    section = graphene.Field(SectionType)

    @staticmethod
    def mutate(root, info, id):
        try:
            section_instance = Section.objects.get(pk=id)
        except Section.DoesNotExist:
            return DeleteSection(ok=False, section=None)
        section_instance.delete()
        section_instance.id = id
        return DeleteSection(ok=True, section=section_instance)


class CreateProgram(graphene.Mutation):
    class Arguments:
        input = ProgramInput(required=True)

    ok = graphene.Boolean()
    program = graphene.Field(ProgramType)

    @staticmethod
    def mutate(root, info, input=None):
        program_instance = Program(name=input.name, description=input.description)
        program_instance.save()
        return CreateProgram(ok=True, program=program_instance)


class DeleteProgram(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    program = graphene.Field(ProgramType)

    @staticmethod
    def mutate(root, info, id):
        try:
            program_instance = Program.objects.get(pk=id)
        except Program.DoesNotExist:
            return DeleteProgram(ok=False, program=None)
        program_instance.delete()
        program_instance.id = id
        return DeleteProgram(ok=True, program=program_instance)


class UpdateProgram(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ProgramInput(required=True)

    ok = graphene.Boolean()
    program = graphene.Field(ProgramType)

    @staticmethod
    def mutate(root, info, id, input=None):
        try:
            program_instance = Program.objects.get(pk=id)
        except Program.DoesNotExist:
            return UpdateProgram(ok=False, program=None)

        if input.description:
            program_instance.content = input.content

        if input.name:
            program_instance.name = input.name

        program_instance.save()

        return UpdateProgram(ok=True, program=program_instance)
