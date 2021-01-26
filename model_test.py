from flask_testing import TestCase
from flask import escape
from helloapp import app, db
from .config import TestingConfig
from .models import Quotes


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object(TestingConfig)

        return app

    @classmethod
    def setUpClass(cls):
        db.session.commit()
        db.drop_all()
        db.create_all()

        quote1 = Quotes(quoteauthor='Albert Einstein', quotestring="Only two things are infinite, the universe and human stupidity, and I'm not sure about the former.")

        quote2 = Quotes(quoteauthor='Abraham Lincoln', quotestring="Give me six hours to chop down a tree and I will spend the first four sharpening the axe.")

        quote3 = Quotes(quoteauthor='Benjamin Franklin', quotestring="Tell me and I forget. Teach me and I remember. Involve me and I learn.")

        quote4 = Quotes(quoteauthor='Willian Shakespeare', quotestring="Listen to many, speak to a few.")

        quote5 = Quotes(quoteauthor='Warren Buffett', quotestring="Only when the tide goes out do you discover who's been swimming naked.")

        db.session.add(quote1)
        db.session.add(quote2)
        db.session.add(quote3)
        db.session.add(quote4)
        db.session.add(quote5)

        db.session.commit()

    
class TestQuotesModel(BaseTestCase):

    def test_quotes_count(self):
        self.assertEqual(Quotes.query.count(), 5)

    def test_filter_franklin_quote_no(self):
        bquotes = Quotes.query.filter(Quotes.quoteauthor == 'Benjamin Franklin').all()
        self.assertEqual(len(bquotes), 1)

    def test_filter_franklin_quote(self):
        bquote = Quotes.query.filter(Quotes.quoteauthor == 'Benjamin Franklin').first()
        self.assertEqual(bquote.quotestring, 'Tell me and I forget. Teach me and I remember. Involve me and I learn.')


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

        cls.quotes = Quotes.query.all()
        cls.quotes = [escape(quote.quotestring).encode() for quote in cls.quotes ]


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
        cls.quotes = Quotes.query.all()
        cls.quotes = [escape(quote.quotestring).encode() for quote in cls.quotes ]

    def test_status_code(self):
        response = self.client.get('/quotes/')
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get('/quotes/')
        self.assertTemplateUsed('quotes.html')

    def test_response_nquotes(self):
        response = self.client.get('/quotes/')
        print(response.data)
        print(self.quotes)
        nquotes = sum([ 1 for quote in self.quotes if quote in response.data ])
        assert nquotes == 5

    def test_response_valid_quotes(self):
        response = self.client.get('/quotes/')
        assert all([ quote in response.data for quote in self.quotes ])  
