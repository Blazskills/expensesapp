import pdb
from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker

fake = Faker()


class TestSetup(APITestCase):
   def setUp(self):
        
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.faker = Faker()
        # email = fake.email()
        # updatedemail =fake.email().split('@')[0]
        # if 'example' in email:
        #         email = updatedemail+'@gmail.com'
        # else:
        #     email = fake.email()
        self.user_data = {
            'email': 'ilesanmiospe@gmail.com',
            'username': fake.email().split('@')[0],
            'password': fake.name().split(' ')[0],
            'first_name': fake.name(),
            'last_name': fake.name(),
        }
        
        # import pdb; pdb.set_trace()
        return super().setUp()
    
   def tearDown(self):
        return super().tearDown()
    
    
    