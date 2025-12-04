import requests


class ItemClient:
    def __init__(self, base_url: str):
        """
        Initialize the service with the base URL of the Items REST API.
        :param base_url: Base URL of the REST API (e.g., "http://localhost:8000/items")
        """
        self.base_url = base_url.rstrip('/')

    def get_all_items(self):
        """
        Read all goods in shop from the API.
        :return: List of goods.
        """
        url = f"{self.base_url}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()

    def get_item_by_id(self, item_id: int):
        """
        Fetch a specific item by its ID.
        :param item_id: ID of the item to fetch.
        :return: Item details.
        """
        url = f"{self.base_url}/{item_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()
