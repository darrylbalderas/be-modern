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

    def test_programs(self):
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

    def test_create_activity(self):
        response = self.query('''
            mutation createActivity($input: ActivityInput!) {
                createActivity(input: $input) {
                    ok
                    activity {
                        id
                        name
                        content
                    }
                }
            }
            ''',
                              op_name='createActivity',
                              input_data={
                                  'name': 'Be vulnerable',
                                  'content':
                                  '<p> 3 things you love about yourself </p>',
                                  'sections': [{
                                      'id': 1
                                  }]
                              })
        content = json.loads(response.content)
        expected = {
            'data': {
                'createActivity': {
                    'ok': True,
                    'activity': {
                        'id': '3',
                        'name': 'Be vulnerable',
                        'content': '<p> 3 things you love about yourself </p>'
                    }
                }
            }
        }
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_create_activity_with_unknown_section(self):
        response = self.query('''
                mutation createActivity($input: ActivityInput!) {
                    createActivity(input: $input) {
                        ok
                        activity {
                            id
                            name
                            content
                        }
                    }
                }
                ''',
                              op_name='createActivity',
                              input_data={
                                  'name': 'Unknown',
                                  'content':
                                  '<p> Describe what it means to be alive </p>',
                                  'sections': [{
                                      'id': 100
                                  }]
                              })
        content = json.loads(response.content)
        expected = {'data': {'createActivity': {'ok': False, 'activity': None}}}
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_delete_activity(self):
        response = self.query('''
                mutation deleteActivity($id: Int!) {
                    deleteActivity(id: $id) {
                        ok
                        activity {
                            id
                            name
                            content
                        }
                    }
                }
                ''',
                              op_name='deleteActivity',
                              variables={'id': 2})
        content = json.loads(response.content)
        expected = {
            'data': {
                'deleteActivity': {
                    'ok': True,
                    'activity': {
                        'id': '2',
                        'name': '5 minute journal',
                        'content': ''
                    }
                }
            }
        }
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

        response = self.query('''
                query getActivity($id: Int!) {
                    activity(id: $id) {
                        id
                        name
                    }
                }
                ''',
                              op_name='getActivity',
                              variables={'id': 2})
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEquals(content, {'data': {'activity': None}})

    def test_delete_unknown_activity(self):
        response = self.query('''
                    mutation deleteActivity($id: Int!) {
                        deleteActivity(id: $id) {
                            ok
                            activity {
                                id
                                name
                                content
                            }
                        }
                    }
                    ''',
                              op_name='deleteActivity',
                              variables={'id': 100})
        content = json.loads(response.content)
        expected = {'data': {'deleteActivity': {'ok': False, 'activity': None}}}
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_update_activity(self):
        response = self.query('''
                mutation updateActivity($id: Int!, $input: ActivityInput!) {
                    updateActivity(id: $id, input: $input) {
                        ok
                        activity {
                            id
                            name
                            content
                        }
                    }
                }
                ''',
                              op_name='updateActivity',
                              variables={
                                  'id': 2,
                                  'input': {
                                      'name': '6 minute journal',
                                  }
                              })
        content = json.loads(response.content)
        expected = {
            'data': {
                'updateActivity': {
                    'ok': True,
                    'activity': {
                        'id': '2',
                        'name': '6 minute journal',
                        'content': ''
                    }
                }
            }
        }
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_update_nonexisten_activity(self):
        response = self.query('''
                mutation updateActivity($id: Int!, $input: ActivityInput!) {
                    updateActivity(id: $id, input: $input) {
                        ok
                        activity {
                            id
                            name
                            content
                        }
                    }
                }
                    ''',
                              op_name='updateActivity',
                              variables={
                                  'id': 100,
                                  'input': {
                                      'name': '6 minute journal',
                                  }
                              })
        content = json.loads(response.content)
        expected = {'data': {'updateActivity': {'ok': False, 'activity': None}}}
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_create_section(self):
        response = self.query('''
            mutation createSection($input: SectionInput!) {
                createSection(input: $input) {
                    ok
                    section {
                        id
                        name
                    }
                }
            }
            ''',
                              op_name='createSection',
                              input_data={
                                  'name': 'Conquering your inner self',
                                  'description': '',
                                  'orderIndex': 5,
                                  'overviewImage':
                                  'http://d111111abcdef8.cloudfront.net/image.jpg',
                                  'programs': [{
                                      'id': 1
                                  }]
                              })
        content = json.loads(response.content)
        expected = {
            'data': {
                'createSection': {
                    'ok': True,
                    'section': {
                        'id': '5',
                        'name': 'Conquering your inner self',
                    }
                }
            }
        }
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_delete_section(self):
        response = self.query('''
                mutation deleteSection($id: Int!) {
                    deleteSection(id: $id) {
                        ok
                        section {
                            id
                            name
                        }
                    }
                }
                ''',
                              op_name='deleteSection',
                              variables={'id': 2})
        content = json.loads(response.content)
        expected = {
            'data': {
                'deleteSection': {
                    'ok': True,
                    'section': {
                        'id': '2',
                        'name': 'Learn to let go',
                    }
                }
            }
        }
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

        response = self.query('''
                query getSection($id: Int!) {
                    section(id: $id) {
                        id
                        name
                    }
                }
                ''',
                              op_name='getSection',
                              variables={'id': 2})
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEquals(content, {'data': {'section': None}})

    def test_delete_nonexisten_section(self):
        response = self.query('''
                    mutation deleteSection($id: Int!) {
                        deleteSection(id: $id) {
                            ok
                            section {
                                id
                                name
                            }
                        }
                    }
                    ''',
                              op_name='deleteSection',
                              variables={'id': 100})
        content = json.loads(response.content)
        expected = {'data': {'deleteSection': {'ok': False, 'section': None}}}
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_create_program(self):
        response = self.query('''
            mutation createProgram($input: ProgramInput!) {
                createProgram(input: $input) {
                    ok
                    program {
                        id
                        name
                        description
                    }
                }
            }
            ''',
                              op_name='createProgram',
                              input_data={
                                  'name': 'Imposter syndrome',
                                  'description': '',
                              })
        content = json.loads(response.content)
        expected = {
            'data': {
                'createProgram': {
                    'ok': True,
                    'program': {
                        'id': '3',
                        'name': 'Imposter syndrome',
                        'description': '',
                    }
                }
            }
        }
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_delete_program(self):
        response = self.query('''
                mutation deleteProgram($id: Int!) {
                    deleteProgram(id: $id) {
                        ok
                        program {
                            id
                            name
                        }
                    }
                }
                ''',
                              op_name='deleteProgram',
                              variables={'id': 2})
        content = json.loads(response.content)
        expected = {
            'data': {
                'deleteProgram': {
                    'ok': True,
                    'program': {
                        'id': '2',
                        'name': 'Cognitive Behavioral Therapy',
                    }
                }
            }
        }
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

        response = self.query('''
                query getProgram($id: Int!) {
                    program(id: $id) {
                        id
                        name
                    }
                }
                ''',
                              op_name='getProgram',
                              variables={'id': 2})
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEquals(content, {'data': {'program': None}})

    def test_delete_nonexisten_program(self):
        response = self.query('''
                    mutation deleteProgram($id: Int!) {
                        deleteProgram(id: $id) {
                            ok
                            program {
                                id
                                name
                            }
                        }
                    }
                    ''',
                              op_name='deleteProgram',
                              variables={'id': 100})
        content = json.loads(response.content)
        expected = {'data': {'deleteProgram': {'ok': False, 'program': None}}}
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_update_program(self):
        response = self.query('''
                mutation updateProgram($id: Int!, $input: ProgramInput!) {
                    updateProgram(id: $id, input: $input) {
                        ok
                        program {
                            id
                            name
                        }
                    }
                }
                ''',
                              op_name='updateProgram',
                              variables={
                                  'id': 2,
                                  'input': {
                                      'name': '6 minute journal',
                                  }
                              })
        content = json.loads(response.content)
        expected = {
            'data': {
                'updateProgram': {
                    'ok': True,
                    'program': {
                        'id': '2',
                        'name': '6 minute journal',
                    }
                }
            }
        }
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)

    def test_update_nonexisten_program(self):
        response = self.query('''
                mutation updateProgram($id: Int!, $input: ProgramInput!) {
                    updateProgram(id: $id, input: $input) {
                        ok
                        program {
                            id
                            name
                        }
                    }
                }
                    ''',
                              op_name='updateProgram',
                              variables={
                                  'id': 100,
                                  'input': {
                                      'name': '6 minute journal',
                                  }
                              })
        content = json.loads(response.content)
        expected = {'data': {'updateProgram': {'ok': False, 'program': None}}}
        self.maxDiff = None
        self.assertResponseNoErrors(response)
        self.assertEquals(content, expected)
