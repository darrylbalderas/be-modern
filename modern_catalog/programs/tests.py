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

    def test_program(self):
        query = '''
                query getProgram($id: Int!) {
                    program(id: $id) {
                        id
                        name
                    }
                }
                '''
        response = self.query(query, variables={'id': 1})
        content = json.loads(response.content)

        expected = {'data': {'program': {'id': '1', 'name': 'Leadership Development'}}}
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_section(self):
        query = '''
                query getSection($id: Int!) {
                    section(id: $id) {
                        id
                        name
                    }
                }
                '''
        response = self.query(query, variables={'id': 1})
        content = json.loads(response.content)

        expected = {
            'data': {
                'section': {
                    'id': '1',
                    'name': 'Explore your strengths and weaknesses'
                }
            }
        }
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_activity(self):
        query = '''
                query getActivity($id: Int!) {
                    activity(id: $id) {
                        id
                        name
                    }
                }
                '''
        response = self.query(query, variables={'id': 1})
        content = json.loads(response.content)

        expected = {'data': {'activity': {'id': '1', 'name': 'Meditate'}}}
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)
