from flask_testing import TestCase
from hello import app

class BaseTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True

        return app

class TestHelloView(BaseTestCase):

    def test_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get('/')
        self.assertTemplateUsed('index.html')

    def test_response(self):
        response = self.client.get('/')
        self.assertIn(b"Hello World!!! I've run my first Flask application.", response.data)

class TestHelloUserView(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.quotes = [
                b"Only two things are infinite, the universe and human stupidity, and I&#39;m not sure about the former.",
                b"Give me six hours to chop down a tree and I will spend the first four sharpening the axe.",
                b"Tell me and I forget. Teach me and I remember. Involve me and I learn.",
                b"Listen to many, speak to a few.",
                b"Only when the tide goes out do you discover who&#39;s been swimming naked."
        ]

    def test_status_code(self):
        response = self.client.get('/hello/user1/')
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get('/hello/user1/')
        self.assertTemplateUsed('hello_user.html')

    def test_response_nquotes(self):
        response = self.client.get('/hello/user1/')
        nquotes = sum([ 1 for quote in self.quotes if quote in response.data ])
        assert nquotes == 1

    def test_response_valid_quote(self):
        response = self.client.get('/hello/user1/')
        assert any([ quote in response.data for quote in self.quotes ])

    def test_hello_response(self):
        response = self.client.get('/hello/user1/')
        assert b'Hello user1' in response.data


class TestDisplayQuotesView(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.quotes = [
                b"Only two things are infinite, the universe and human stupidity, and I&#39;m not sure about the former.",
                b"Give me six hours to chop down a tree and I will spend the first four sharpening the axe.",
                b"Tell me and I forget. Teach me and I remember. Involve me and I learn.",
                b"Listen to many, speak to a few.",
                b"Only when the tide goes out do you discover who&#39;s been swimming naked."
        ]

    def test_status_code(self):
        response = self.client.get('/quotes/')
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get('/quotes/')
        self.assertTemplateUsed('quotes.html')

    def test_response_nquotes(self):
        response = self.client.get('/quotes/')
        print(response.data)
        nquotes = sum([ 1 for quote in self.quotes if quote in response.data ])
        assert nquotes == 5

    def test_response_valid_quotes(self):
        response = self.client.get('/quotes/')
        assert all([ quote in response.data for quote in self.quotes ])  
