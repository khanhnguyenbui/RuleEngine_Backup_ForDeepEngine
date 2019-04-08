# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.segmentation_point import SegmentationPoint  # noqa: F401,E501
from swagger_server import util


class Personalization(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, per_id: str=None, per_name: str=None, content: List[SegmentationPoint]=None):  # noqa: E501
        """Personalization - a model defined in Swagger

        :param per_id: The per_id of this Personalization.  # noqa: E501
        :type per_id: str
        :param per_name: The per_name of this Personalization.  # noqa: E501
        :type per_name: str
        :param content: The content of this Personalization.  # noqa: E501
        :type content: List[SegmentationPoint]
        """
        self.swagger_types = {
            'per_id': str,
            'per_name': str,
            'content': List[SegmentationPoint]
        }

        self.attribute_map = {
            'per_id': 'perID',
            'per_name': 'perName',
            'content': 'content'
        }

        self._per_id = per_id
        self._per_name = per_name
        self._content = content

    @classmethod
    def from_dict(cls, dikt) -> 'Personalization':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Personalization of this Personalization.  # noqa: E501
        :rtype: Personalization
        """
        return util.deserialize_model(dikt, cls)

    @property
    def per_id(self) -> str:
        """Gets the per_id of this Personalization.


        :return: The per_id of this Personalization.
        :rtype: str
        """
        return self._per_id

    @per_id.setter
    def per_id(self, per_id: str):
        """Sets the per_id of this Personalization.


        :param per_id: The per_id of this Personalization.
        :type per_id: str
        """

        self._per_id = per_id

    @property
    def per_name(self) -> str:
        """Gets the per_name of this Personalization.


        :return: The per_name of this Personalization.
        :rtype: str
        """
        return self._per_name

    @per_name.setter
    def per_name(self, per_name: str):
        """Sets the per_name of this Personalization.


        :param per_name: The per_name of this Personalization.
        :type per_name: str
        """

        self._per_name = per_name

    @property
    def content(self) -> List[SegmentationPoint]:
        """Gets the content of this Personalization.


        :return: The content of this Personalization.
        :rtype: List[SegmentationPoint]
        """
        return self._content

    @content.setter
    def content(self, content: List[SegmentationPoint]):
        """Sets the content of this Personalization.


        :param content: The content of this Personalization.
        :type content: List[SegmentationPoint]
        """

        self._content = content
