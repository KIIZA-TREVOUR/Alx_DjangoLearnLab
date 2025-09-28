from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book


class BookAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="George Orwell")
        self.book = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author
        )
        self.client = APIClient()

    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_book_detail(self):
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '1984')

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'Animal Farm',
            'publication_year': 1945,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        data = {'title': 'New Book', 'publication_year': 2020, 'author': self.author.id}
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        data = {'title': 'Nineteen Eighty-Four', 'publication_year': 1949, 'author': self.author.id}
        response = self.client.post(f'/api/books/{self.book.id}/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Nineteen Eighty-Four')

    def test_update_book_unauthenticated(self):
        data = {'title': 'Hacked', 'publication_year': 2025, 'author': self.author.id}
        response = self.client.post(f'/api/books/{self.book.id}/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(f'/api/books/{self.book.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_unauthenticated(self):
        response = self.client.post(f'/api/books/{self.book.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_year(self):
        Book.objects.create(title="New Book", publication_year=2020, author=self.author)
        response = self.client.get('/api/books/?publication_year=1949')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_search_by_title(self):
        response = self.client.get('/api/books/?search=1984')
        self.assertEqual(len(response.data), 1)

    def test_search_by_author(self):
        response = self.client.get('/api/books/?search=Orwell')
        self.assertEqual(len(response.data), 1)

    def test_ordering_by_year(self):
        Book.objects.create(title="New Book", publication_year=2020, author=self.author)
        response = self.client.get('/api/books/?ordering=publication_year')
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [1949, 2020])

    def test_ordering_by_title_desc(self):
        Book.objects.create(title="Animal Farm", publication_year=1945, author=self.author)
        response = self.client.get('/api/books/?ordering=-title')
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, ['Animal Farm', '1984'])  # Fixed!