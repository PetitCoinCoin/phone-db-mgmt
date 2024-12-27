import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.models import Customer

client = TestClient(app)


class TestCustomers:
    BASE_URL = "/customers"

    def test_list_empty_customers(self):
        response = client.get(self.BASE_URL)
        assert response.status_code == 200
        json_response = response.json()
        assert not len(json_response)

    def test_list_customers(self, mock_customer):
        customer = mock_customer
        response = client.get(self.BASE_URL)
        assert response.status_code == 200
        json_response = response.json()
        assert len(json_response) == 1
        assert json_response[0]["name"] == customer.name
        assert json_response[0]["id"] == customer.id

    @pytest.mark.parametrize(
            "customer_id,status_code",
            [(None, 200), (9999, 404)],
        )
    def test_get_customer(self, customer_id, status_code, mock_customer):
        customer = mock_customer
        customer_id = customer_id if customer_id else customer.id
        response = client.get(f"{self.BASE_URL}/{customer_id}")
        assert response.status_code == status_code
        json_response = response.json()
        if status_code == 200:
            assert json_response["name"] == customer.name
            assert json_response["id"] == customer.id

    def test_create_customer(self, session):
        new_name = "New customer"
        response = client.post(self.BASE_URL, json={"name": new_name})
        assert response.status_code == 201
        json_response = response.json()
        assert json_response["name"] == new_name
        new_customer = session.query(Customer).filter(Customer.name==new_name).first()
        assert new_customer
        # Cleaning - shouldn't be needed
        session.delete(new_customer)
        session.commit()

    def test_create_customer_error(self, mock_customer):
        response = client.post(self.BASE_URL, json={"name": mock_customer.name})
        assert response.status_code == 409

    @pytest.mark.parametrize(
            "customer_id,status_code",
            [(None, 204), (9999, 404)],
        )
    def test_delete_customer(self, customer_id, status_code, session, mock_customer):
        customer = mock_customer
        customer_id = customer_id if customer_id else customer.id
        response = client.delete(f"{self.BASE_URL}/{customer_id}")
        assert response.status_code == status_code
        assert not session.query(Customer).filter(Customer.id==customer_id).first()
