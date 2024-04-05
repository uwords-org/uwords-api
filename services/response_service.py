from http import HTTPStatus
from rest_framework.response import Response


class ResponseService:

    @staticmethod
    def return_success(msg):
        return Response(msg, HTTPStatus.OK)

    @staticmethod
    def return_not_found(msg):
        return Response(msg, HTTPStatus.NOT_FOUND)

    @staticmethod
    def return_bad_request(msg):
        return Response(msg, HTTPStatus.BAD_REQUEST)
