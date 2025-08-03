from django.test import TestCase

# Create your tests here.

class Test(TestCase):

    success_code = 200

    def test_home_view(self):
        response = self.client.get("/leads/list")
        self.assertEqual(response.status_code, self.success_code)

    def test_create_view(self):
        response = self.client.get("/leads/create")
        self.assertEqual(response.status_code, self.success_code)
        self.assertContains(response, "Germany")
        csrf_token = response.context["csrf_token"]
        response = self.client.post('/leads/create', {
            'email': 'test.user@mail.com',
            'first_name': 'Test',
            'last_name': "User",
            'country_code': "CO",
            "csrfmiddlewaretoken": csrf_token
        }, follow=True)
        response = self.client.get("/leads/list")
        self.assertContains(response, "test.user@mail.com")
