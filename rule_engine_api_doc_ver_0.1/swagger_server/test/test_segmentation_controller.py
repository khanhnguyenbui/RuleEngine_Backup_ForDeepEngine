# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.segmentation import Segmentation  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSegmentationController(BaseTestCase):
    """SegmentationController integration test stubs"""

    def test_all_segmentation(self):
        """Test case for all_segmentation

        Get all segmentations
        """
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/segmentation/all',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_segmentation(self):
        """Test case for create_segmentation

        Create Segmentation
        """
        body = Segmentation()
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/segmentation/{segID}'.format(segID='segID_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_segmentation(self):
        """Test case for delete_segmentation

        Delete Segmentation
        """
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/segmentation/{segID}'.format(segID='segID_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_execute_segmentation(self):
        """Test case for execute_segmentation

        Execute a segmentation
        """
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/segmentation/execute/{segID}'.format(segID='segID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_segmentation_by_id(self):
        """Test case for get_segmentation_by_id

        Get query by segID
        """
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/segmentation/{segID}'.format(segID='segID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_segmentation(self):
        """Test case for update_segmentation

        Updated segmentation
        """
        body = Segmentation()
        response = self.client.open(
            '/deepengine/Shopper/1.0.0/method/segmentation/{segID}'.format(segID='segID_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
