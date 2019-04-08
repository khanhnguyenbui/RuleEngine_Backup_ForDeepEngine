import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util


def all_user():  # noqa: E501
    """Get all users

    Get all users information. # noqa: E501


    :rtype: List[User]
    """
    return 'do some magic!'


def create_user(userID, body):  # noqa: E501
    """Create user

    Create new user. # noqa: E501

    :param userID: userID that need to be created
    :type userID: str
    :param body: Updated user object
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_user(userID):  # noqa: E501
    """Delete user

    Delete user. # noqa: E501

    :param userID: The userID that needs to be deleted
    :type userID: str

    :rtype: None
    """
    return 'do some magic!'


def get_user_by_id(userID):  # noqa: E501
    """Get user by userID

     # noqa: E501

    :param userID: The userID that needs to be fetched. Use 1 for testing.
    :type userID: str

    :rtype: User
    """
    return 'do some magic!'


def update_user(userID, body):  # noqa: E501
    """Updated user

    Update user information. # noqa: E501

    :param userID: userID that need to be updated
    :type userID: str
    :param body: Updated user object
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
