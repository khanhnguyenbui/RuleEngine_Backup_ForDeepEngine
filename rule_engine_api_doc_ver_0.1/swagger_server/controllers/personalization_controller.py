import connexion
import six

from swagger_server.models.personalization import Personalization  # noqa: E501
from swagger_server import util


def all_personalization():  # noqa: E501
    """Get all Personalizations

    Get all Personalizations. # noqa: E501


    :rtype: List[Personalization]
    """
    return 'do some magic!'


def create_personalization(perID, body):  # noqa: E501
    """Create Personalization

    Create new Personalization. # noqa: E501

    :param perID: perID that need to be created
    :type perID: str
    :param body: Create Personalization
    :type body: dict | bytes

    :rtype: Personalization
    """
    if connexion.request.is_json:
        body = Personalization.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_personalization(perID):  # noqa: E501
    """Delete Personalization

    Delete Personalization. # noqa: E501

    :param perID: The perID that needs to be deleted
    :type perID: str

    :rtype: None
    """
    return 'do some magic!'


def execute_personalization(userID, perID):  # noqa: E501
    """Execute a Personalization

    Execute a Personalization. # noqa: E501

    :param userID: The userID that needs to be calculator
    :type userID: str
    :param perID: perID that need to be execute
    :type perID: str

    :rtype: int
    """
    return 'do some magic!'


def get_personalization_by_id(perID):  # noqa: E501
    """Get Personalization by perID

     # noqa: E501

    :param perID: The perID that needs to be fetched. Use 1 for testing.
    :type perID: str

    :rtype: Personalization
    """
    return 'do some magic!'


def update_personalization(perID, body):  # noqa: E501
    """Updated Personalization

    Update Personalization # noqa: E501

    :param perID: perID that need to be updated
    :type perID: str
    :param body: Update Personalization
    :type body: dict | bytes

    :rtype: Personalization
    """
    if connexion.request.is_json:
        body = Personalization.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
