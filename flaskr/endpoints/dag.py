"""
Internal endpoint for getting and posting execution data
This are the endpoints used by airflow in its communication with cornflow
"""

from flask import request
from flask_restful import Resource

from ..models import ExecutionModel
from ..schemas import ExecutionSchema
from ..shared import Auth

execution_schema = ExecutionSchema()


class DAGEndpoint(Resource):
    """
    Endpoint used for the DAG endpoint
    """
    # TODO: this endpoint should be a PUT actually, as the execution is also created
    #  and airflow is only writing the results to the needed fields
    @Auth.super_admin_required
    def post(self, reference_id):
        """
        API method to write the results of the execution
        It requires authentication to be passed in the form of a token that has to be linked to
        an existing session (login) made by the superuser created for the airflow webserver

        :param str reference_id: ID of the execution
        :return: A dictionary with a message (body) and a HTTP status code
        :rtype: Tuple(dict, integer)
        """
        # TODO: control errors and give back error message and error status,
        #  for example if there is a problem with the data validation
        req_data = request.get_json()
        execution = ExecutionModel.get_execution_with_reference(reference_id)
        execution.update(req_data)
        execution.finished = True
        execution.save()
        return {'message': 'saved results'}, 201
    
    @Auth.super_admin_required
    def get(self, reference_id):
        """
        API method to get the data of the instance that is going to be executed
        It requires authentication to be passed in the form of a token that has to be linked to
        an existing session (login) made by the superuser created for the airflow webserver

        :param str reference_id: ID of the execution
        :return: the execution data (body) in a dictionary with structure of :class:`ConfigSchema`
        and :class:`DataSchema` and an integer for HTTP status code
        :rtype: Tuple(dict, integer)
        """
        # TODO: control errors and give back error message and error status,
        #  for example if there is no data.
        execution_data = ExecutionModel.get_execution_data(reference_id)
        return execution_data, 200
