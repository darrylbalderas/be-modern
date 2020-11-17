# from django.test import TestCase

# Create your tests here.
import json
from graphene_django.utils.testing import GraphQLTestCase
from modern_catalog.schema import schema


class TestPrograms(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['programs.json']

    def test_sections(self):
        query = '''
            query {
                sections {
                    id
                    name
                }
            }
            '''
        response = self.query(query)
        content = json.loads(response.content)

        # This validates the status code and if you get errors
        expected = {
            'data': {
                'sections': [{
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
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_activities(self):
        query = '''
            query {
                activities {
                    id
                    name
                }
            }
            '''
        response = self.query(query)
        content = json.loads(response.content)
        expected = {
            'data': {
                'activities': [{
                    'id': '2',
                    'name': '5 minute journal'
                }, {
                    'id': '1',
                    'name': 'Meditate'
                }]
            }
        }
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_all_programs(self):
        query = '''
            query {
                programs {
                    id
                    name
                }
            }
            '''
        response = self.query(query)
        content = json.loads(response.content)
        expected = {
            'data': {
                'programs': [{
                    'id': '2',
                    'name': 'Cognitive Behavioral Therapy'
                }, {
                    'id': '1',
                    'name': 'Leadership Development'
                }]
            }
        }
        self.maxDiff = None
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
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)
