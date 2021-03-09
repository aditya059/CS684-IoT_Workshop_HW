from datetime import datetime
from typing import Any

import requests
from requests.models import Response


class ServerApi:
    """
    Implements IoT Server API

    Methods in this class resemble resources of the IoT Server API. Complete the methods
    to query the resource. To get required data use the requests library and supplied
    API documentation.

    The default baseUrl to use is https://apihptu.e-yantra.org/api

    The messages in requests and responses are JSON. This means that you should use json
    parameter while making a request and call json() on response (response.json()).

    NOTE:
    Use self.session and not self.http_client or requests.
    For instance,
    self.session.get() is VALID.
    self.http_client.get() is INVALID.
    requests.get() is INVALID.

    Some methods in this class raise exceptions by calling `raise_exceptions` method on 4xx or
    5xx errors i.e. if the request is unsuccessful.
    """

    def __init__(self, base_url='https://apihptu.e-yantra.org/api', http_client=requests):
        """
        Sets base_url and http_client to use.

        DO NOT MODIFY
        """
        if base_url is None:
            base_url = 'http://localhost:8080'
        self.base_url = base_url
        if http_client is None:
            http_client = requests
        self.http_client = http_client
        self.session = http_client.session()
        self.session.headers.update({'Accept': 'application/json'})

    @staticmethod
    def raise_exceptions(response) -> None:
        """
        Throw requests.HTTPError() with message 'Error <status_code>' and response `response`.
        E.g. If response.status_code is 404 throw requests.HTTPError('Error 404', response=response)

        The method should raise exception if there's a 4xx or 5xx error. This method is needed
        since requests library won't raise 4XX or 5XX errors by itself. `status_code` to use can
        be found in `response.status_code`
        """
        if response.status_code // 100 != 2:
            raise requests.HTTPError(f'Error {response.status_code}', response=response)

    def login(self, username: str, password: str) -> None:
        """
        User login.

        Requests login endpoint with username and password of the user to fetch
        the authToken. The authToken should be sent in the Authorization header
        with other requests as given in API documentation.

        Raises exception if unsuccessful by calling raise_exceptions.
        """
        response = self.session.post(f'{self.base_url}/login', json={'username': username, 'password': password})
        self.raise_exceptions(response)
        self.authToken = response.json()['authToken']

    def create_thing(self, name: str, thing_type: str = '', description: str = '') -> dict:
        """
        Create a thing with given name, thing_type and description.

        Returns the created thing's details obtained in response as dictionary.
        Note: Requires authToken for authentication.

        Raises exception if unsuccessful by calling raise_exceptions.
        """
        response = self.session.post(f'{self.base_url}/thing', json={'name': name, 'thingType': thing_type, 'description': description}, headers = {'Authorization': f'Bearer {self.authToken}'})
        self.raise_exceptions(response)
        return response.json()

    def get_thing(self, thing_id: int) -> dict:
        """
        Get thing with id `thing_id`.

        Returns the thing's details obtained in response as dictionary.

        Raises exception if unsuccessful by calling raise_exceptions.
        Note: Requires authToken for authentication.
        """
        response = self.session.get(f'{self.base_url}/thing/{thing_id}', headers = {'Authorization': f'Bearer {self.authToken}'})
        self.raise_exceptions(response)
        return response.json()

    def update_thing(self, thing_id: int, name: str, thing_type: str = '', description: str = '') -> dict:
        """
        Update thing with id `thing_id` and details name, thing_type and description.

        Returns the data obtained in response as dictionary.

        Raises exception if unsuccessful by calling raise_exceptions.
        Note: Requires authToken for authentication.
        """
        response = self.session.put(f'{self.base_url}/thing/{thing_id}', json={'name': name, 'thingType': thing_type, 'description': description} ,headers = {'Authorization': f'Bearer {self.authToken}'})
        self.raise_exceptions(response)
        return response.json()
        
    def delete_thing(self, thing_id: int) -> None:
        """
        Delete thing with id `thing_id`.

        Raises exception if unsuccessful by calling raise_exceptions.
        Note: Requires authToken for authentication.
        """
        response = self.session.delete(f'{self.base_url}/thing/{thing_id}', headers = {'Authorization': f'Bearer {self.authToken}'})
        self.raise_exceptions(response)

    def client_token(self, thing_id: int) -> str:
        """
        Get access token for thing with id `thing_id`.

        This access token is used for authenticating the thing connected to internet.
        It should be sent in Authorization header with every thing/device request.
        Returns the token obtained in response as string.

        Raises exception if unsuccessful by calling raise_exceptions.
        Note: Requires authToken for authentication.
        """
        response = self.session.get(f'{self.base_url}/thing/{thing_id}/token' ,headers = {'Authorization': f'Bearer {self.authToken}'})
        self.raise_exceptions(response)
        return response.json()['accessToken']

    def add_telemetry(self, access_token: str, data: dict) -> dict:
        """
        Send telemetry data for thing with given access_token.

        Returns the details of the telemetry data obtained in response as dictionary.

        Raises exception if unsuccessful by calling raise_exceptions.
        Note: Requires accessToken for authentication.
        """
        response = self.session.post(f'{self.base_url}/telemetry', json= data, headers = {'Authorization': f'Bearer {access_token}'})
        self.raise_exceptions(response)
        return response.json()

    def update_telemetry(self, access_token: str, data_id: int, data: dict) -> dict:
        """
        Update telemetry data with id `data_id` for thing with given access_token.

        Returns the details of the updated telemetry data obtained in response as dictionary.

        Raises exception if unsuccessful by calling raise_exceptions.
        Note: Requires accessToken for authentication.
        """
        response = self.session.put(f'{self.base_url}/telemetry/{data_id}', json= data, headers = {'Authorization': f'Bearer {access_token}'})
        self.raise_exceptions(response)
        return response.json()

    def get_telemetry(self, access_token: str, start_time: str, end_time: str) -> list:
        """
        Get telemetry data sent between `start_time` and `end_time` for thing with `access_token`.

        start_time and end_time follow 'YYYY:MM:DD HH:mm:ss' format
        E.g. '2020-12-06 20:01:02'

        Returns the telemetry data points obtained in response as list.
        Return empty list if there's no data between specified range (404 Not Found).

        Raises exception if unsuccessful by calling raise_exceptions.
        Note: Requires accessToken for authentication.
        """
        response = self.session.get(f'{self.base_url}/telemetry?startTs={start_time}&endTs={end_time}', headers = {'Authorization': f'Bearer {access_token}'})
        if response.status_code != 404:
            self.raise_exceptions(response)
        return response.json()

    def get_thing_telemetry(self, thing_id: int, start_time: str, end_time: str) -> list:
        """
        Get telemetry data sent between `start_time` and `end_time` for thing with `thing_id`.

        Returns the telemetry data points obtained in response as list.
        Return empty list if there's no data between specified range (404 Not Found).

        Raises exception if unsuccessful by calling raise_exceptions.
        Note: Requires authToken for authentication.
        """
        response = self.session.get(f'{self.base_url}/thing/{thing_id}/telemetry?startTs={start_time}&endTs={end_time}', headers = {'Authorization': f'Bearer {self.authToken}'})
        if response.status_code != 404:
            self.raise_exceptions(response)
        return response.json()

    def send_rpc(self, thing_id: str, method: str, params: Any) -> dict:
        """
        Send RPC with `method` and `params` to thing `thing_id`.

        Returns the details of the command obtained in response as dictionary.

        Raises exception if unsuccessful by calling raise_exceptions.
        Note: Requires authToken for authentication.
        """
        response = self.session.post(f'{self.base_url}/rpc/{thing_id}', json={'method': method, 'params': params}, headers = {'Authorization': f'Bearer {self.authToken}'})
        print("Response on sending RPC: ", response.json())
        self.raise_exceptions(response)
        return response.json()

    def receive_rpc(self, access_token: str) -> dict:
        """
        Get RPC for thing with given `access_token`.

        Returns the details of the command obtained in response as dictionary.
        Return empty dictionary if this resource returns 404.

        Raises exception if unsuccessful by calling raise_exceptions.
        Note: Requires accessToken for authentication.
        """
        response = self.session.get(f'{self.base_url}/rpc', headers = {'Authorization': f'Bearer {access_token}'})
        print("Recieved RPC: ", response.json())
        if response.status_code != 404:
            self.raise_exceptions(response)
        return response.json()


