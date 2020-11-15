# from django.test import TestCase

# Create your tests here.
import json
from graphene_django.utils.testing import GraphQLTestCase
from modern_catalog.schema import schema
from mixer.backend.django import mixer
from modern_catalog.programs.models import Program, Section, Activity


class TestPrograms(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['programs.json']

    def test_all_sections(self):
        query = '''
            query {
                allSections {
                    id
                    name
                }
            }
            '''
        response = self.query(query)
        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        expected = {
            'data': {
                'allSections': [{
                    'id': '1',
                    'name': 'Explore your strengths and weaknesses'
                }, {
                    'id': '2',
                    'name': 'Learn to let go'
                }, {
                    'id': '3',
                    'name': 'Walking down memory lane'
                }, {
                    'id': '4',
                    'name': 'Self Awareness'
                }]
            }
        }
        self.assertEquals(content, expected)

    def test_all_activities(self):
        query = '''
            query {
                allActivities {
                    id
                    name
                }
            }
            '''
        response = self.query(query)
        content = json.loads(response.content)
        expected = {
            'data': {
                'allActivities': [{
                    'id': '1',
                    'name': 'Meditate'
                }, {
                    'id': '2',
                    'name': '5 minute journal'
                }]
            }
        }
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_program_by_name(self):
        query = '''
                query programByName($name: String!) {
                    programByName(name: $name) {
                        id
                        name
                    }
                }
                '''
        response = self.query(query, variables={'name': 'Leadership Development'})
        content = json.loads(response.content)

        expected = {
            'data': {
                'programByName': {
                    'id': '1',
                    'name': 'Leadership Development'
                }
            }
        }
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)
