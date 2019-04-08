import connexion
import six

from swagger_server.models.segmentation import Segmentation  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util


def all_segmentation():  # noqa: E501
    """Get all segmentations

    Get all segmentations. # noqa: E501


    :rtype: List[Segmentation]
    """
    return 'do some magic!'


def create_segmentation(segID, body):  # noqa: E501
    """Create Segmentation

    Create new Segmentation. # noqa: E501

    :param segID: segID that need to be created
    :type segID: str
    :param body: Create Segmentation
    :type body: dict | bytes

    :rtype: Segmentation
    """
    if connexion.request.is_json:
        body = Segmentation.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_segmentation(segID):  # noqa: E501
    """Delete Segmentation

    Delete Segmentation. # noqa: E501

    :param segID: The segID that needs to be deleted
    :type segID: str

    :rtype: None
    """
    return 'do some magic!'


def execute_segmentation(segID):  # noqa: E501
    """Execute a segmentation

    Execute a segmentation. # noqa: E501

    :param segID: segID that need to be execute
    :type segID: str

    :rtype: List[User]
    """
    return 'do some magic!'


def get_segmentation_by_id(segID):  # noqa: E501
    """Get query by segID

     # noqa: E501

    :param segID: The segID that needs to be fetched. Use 1 for testing.
    :type segID: str

    :rtype: Segmentation
    """
    return 'do some magic!'


def update_segmentation(segID, body):  # noqa: E501
    """Updated segmentation

    Update Segmentation # noqa: E501

    :param segID: segID that need to be updated
    :type segID: str
    :param body: Update Segmentation
    :type body: dict | bytes

    :rtype: Segmentation
    """
    if connexion.request.is_json:
        body = Segmentation.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
