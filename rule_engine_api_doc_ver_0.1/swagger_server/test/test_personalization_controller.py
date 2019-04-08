# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.personalization import Personalization  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPersonalizationController(BaseTestCase):
    """PersonalizationController integration test stubs"""

    def test_all_personalization(self):
        """Test case for all_personalization

        Get all Personalizations
        """
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/personalization/all',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_personalization(self):
        """Test case for create_personalization

        Create Personalization
        """
        body = Personalization()
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/personalization/{perID}'.format(perID='perID_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_personalization(self):
        """Test case for delete_personalization

        Delete Personalization
        """
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/personalization/{perID}'.format(perID='perID_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_execute_personalization(self):
        """Test case for execute_personalization

        Execute a Personalization
        """
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/personalization/execute/{userID}/{perID}'.format(userID='userID_example', perID='perID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_personalization_by_id(self):
        """Test case for get_personalization_by_id

        Get Personalization by perID
        """
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/personalization/{perID}'.format(perID='perID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_personalization(self):
        """Test case for update_personalization

        Updated Personalization
        """
        body = Personalization()
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/personalization/{perID}'.format(perID='perID_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
