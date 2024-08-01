
class AppClient:
    def __init__(self, client):
        self.app_client = client
        self.base_url = "/api/v1/order/"

    def create_order(self, payload):
        response = self.app_client.post(self.base_url, json=payload)
        return response

    def retrieve_order(self, order_id):
        response = self.app_client.get(f"{self.base_url}{order_id}")
        return response

    def update_order(self, order_id, payload):
        response = self.app_client.put(f"{self.base_url}{order_id}", json=payload)
        return response

    def delete_order(self, order_id):
        response = self.app_client.delete(f"{self.base_url}{order_id}")
        return response
