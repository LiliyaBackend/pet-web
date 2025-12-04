from app.client.item_client import ItemClient

# Base URL of the REST API
api_url = "http://localhost:8000/api/v1/items"
item_service = ItemClient(api_url)

items = item_service.get_all_items()
print("All items:", items)

item_id = 1
item = item_service.get_item_by_id(item_id)
print(f"Item {item_id}:", item)
