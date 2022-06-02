import json

from django.test import TestCase
from django.urls import reverse

from http import HTTPStatus

from utils.helper import set_value

from pathlib import Path

from decouple import config

# Do tests with sample data, 

class API_App_Test(TestCase):

    def setUp(self):

        BASE_DIR = Path(__file__).resolve().parent.parent
        env_file = BASE_DIR / '.env'

        self.env_file_exists = Path.exists(env_file)
        self.orchard_id = '216269'
    
    def test_invalid_url_api_token(self):

        set_value('API_TOKEN', 'XXXXXXXXXXXX')

        response = self.client.get(reverse('missing-trees', args=[self.orchard_id]))

        self.assertIn('Incorrect', json.loads(response.content)['detail'])
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    
    def test_valid_url_api_token(self):

        if self.env_file_exists:

            set_value('API_TOKEN', config('API_TOKEN'))

            response = self.client.get(reverse('missing-trees', args=[self.orchard_id]))

            self.assertTrue(json.loads(response.content).get('missing_trees'))
            self.assertEqual(response.status_code, HTTPStatus.OK)
            
    def test_invalid_orchard_id(self):

        if self.env_file_exists:

            set_value('API_TOKEN', config('API_TOKEN'))

            response = self.client.get(reverse('missing-trees', args=[0]))

            self.assertIn('Access to orchard not permitted', json.loads(response.content)['detail'])
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)