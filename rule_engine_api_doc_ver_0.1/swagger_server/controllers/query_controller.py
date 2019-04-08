import connexion
import six

from swagger_server.models.query import Query  # noqa: E501
from swagger_server import util


def all_query():  # noqa: E501
    """Get all queries

    Get all queries. # noqa: E501


    :rtype: List[Query]
    """
    return 'do some magic!'


def create_query(queryID, body):  # noqa: E501
    """Create query

    Create new query. # noqa: E501

    :param queryID: queryID that need to be created
    :type queryID: str
    :param body: Updated query object
    :type body: dict | bytes

    :rtype: Query
    """
    if connexion.request.is_json:
        body = Query.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_query(queryID):  # noqa: E501
    """Delete query

    Delete query. # noqa: E501

    :param queryID: The queryID that needs to be deleted
    :type queryID: str

    :rtype: None
    """
    return 'do some magic!'


def get_query_by_id(queryID):  # noqa: E501
    """Get query by queryID

     # noqa: E501

    :param queryID: The queryID that needs to be fetched. Use 1 for testing.
    :type queryID: str

    :rtype: Query
    """
    return 'do some magic!'


def update_query(queryID, body):  # noqa: E501
    """Updated query

    Update query information. # noqa: E501

    :param queryID: queryID that need to be updated
    :type queryID: str
    :param body: Updated query object
    :type body: dict | bytes

    :rtype: Query
    """
    if connexion.request.is_json:
        body = Query.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
