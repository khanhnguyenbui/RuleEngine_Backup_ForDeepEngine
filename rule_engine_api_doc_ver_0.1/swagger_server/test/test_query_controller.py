# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.query import Query  # noqa: E501
from swagger_server.test import BaseTestCase


class TestQueryController(BaseTestCase):
    """QueryController integration test stubs"""

    def test_all_query(self):
        """Test case for all_query

        Get all queries
        """
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/query/all',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_query(self):
        """Test case for create_query

        Create query
        """
        body = Query()
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/query/{queryID}'.format(queryID='queryID_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_query(self):
        """Test case for delete_query

        Delete query
        """
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/query/{queryID}'.format(queryID='queryID_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_query_by_id(self):
        """Test case for get_query_by_id

        Get query by queryID
        """
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/query/{queryID}'.format(queryID='queryID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_query(self):
        """Test case for update_query

        Updated query
        """
        body = Query()
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/query/{queryID}'.format(queryID='queryID_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
