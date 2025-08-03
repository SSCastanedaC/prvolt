import requests
from prvolt.settings import HUNTER_API_KEY
from typing import Tuple

class CountriesHandler:
    ws_url = "https://api.first.org/data/v1/countries?scope=full&limit=300"

    @classmethod
    def get_countries(cls):
        URL_BASE = cls.ws_url
        response = requests.get(URL_BASE)
        response.raise_for_status()
        response = response.json()
        countries = response["data"]
        countries = [
            {
                "name": countries[cnt]["country"],
                "code": countries[cnt]["id2"],
            }
            for cnt in countries.keys()
        ]
        return countries


class HunterHandler():
    ws_url = "https://api.hunter.io/v2/leads"
    status_codes = {
        "info": 100,
        "success": 200,
        "no_content": 204,
        "redirection": 300,
        "client_error": 400,
        "server_error": 500,
    }

    @classmethod
    def consume_ws(
        cls,
        body: dict,
        lead_id: int = 0,
        method: str = "GET",
        
    ):
        endpoint = cls.ws_url
        
        if lead_id:
            endpoint = f"{endpoint}/{lead_id}"
        endpoint = f"{endpoint}?api_key={HUNTER_API_KEY}"
        if method == "GET":
            response = requests.get(endpoint)
        elif method == "POST":
            response = requests.post(endpoint, json=body)
        elif method == "DELETE":
            response = requests.delete(endpoint)
        else:
            raise ValueError()
        response.raise_for_status()
        return cls._build_response(response)

    @classmethod
    def _build_response(cls, response) -> Tuple[bool, str | dict]:
        status_codes = cls.status_codes
        if status_codes["success"] <= response.status_code < status_codes["redirection"]:
            return True, "" if response.status_code == status_codes["no_content"] else response.json()
        elif status_codes["client_error"] <= response.status_code < status_codes["server_error"]:
            return False, "Client error"
        elif status_codes["server_error"] <= response.status_code:
            return False, "Server error"
        return False, "Status not provided"
        


class LeadsHandler():

    request_handler = HunterHandler()

    @classmethod
    def get_all(cls):
        return cls.request_handler.consume_ws(body={})

    @classmethod
    def get_by_id(cls, lead_id: int):
        return cls.request_handler.consume_ws(body={}, lead_id=lead_id)

    @classmethod
    def create(cls, body: dict):
        return cls.request_handler.consume_ws(method="POST", body=body)

    @classmethod
    def delete(cls, lead_id: int):
        return cls.request_handler.consume_ws(body={}, lead_id=lead_id, method="DELETE")
