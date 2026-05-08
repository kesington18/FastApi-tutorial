from fastapi import FastAPI
from sentry_sdk.envelope import Item

app = FastAPI()

items = [
    {'id': 1, 'name': 'Item One'},
    {'id': 2, 'name': 'Item Two'},
    {'id': 3, 'name': 'Item Three'},
]

@app.get('/health')
def health_check():
    return {'status': 'ok'}


@app.get("/items")
def get_items():
    return {
        "success": True,
        "response": "success",
        'data': items
    }

@app.get('/items/{item_id}')
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return {
                "success": True,
                "response": "success",
                'data': items
            }
    return {'message': 'Item not found'}

@app.post('/items')
def create_item(item: dict):
    items.append(item)
    return {
        "success": True,
        "response": "success",
        'data': items
    }