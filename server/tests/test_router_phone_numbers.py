import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.models import PhoneNumber

client = TestClient(app)


class TestPhoneNumbers:
    BASE_URL = "/phone_numbers"

    def test_list_empty_phone_numbers(self):
        response = client.get(self.BASE_URL)
        assert response.status_code == 200
        json_response = response.json()
        assert not len(json_response)

    def test_list_phone_numbers(self, mock_phonenumber):
        phone_number = mock_phonenumber
        response = client.get(self.BASE_URL)
        assert response.status_code == 200
        json_response = response.json()
        assert len(json_response) == 1
        assert json_response[0]["id"] == phone_number.id
        assert json_response[0]["phone"] == phone_number.phone

    @pytest.mark.parametrize(
            "phone_id,status_code",
            [(None, 200), (9999, 404)],
        )
    def test_get_phone_number(self, phone_id, status_code, mock_phonenumber):
        phone_number = mock_phonenumber
        phone_id = phone_id if phone_id else phone_number.id
        response = client.get(f"{self.BASE_URL}/{phone_id}")
        assert response.status_code == status_code
        json_response = response.json()
        if status_code == 200:
            assert json_response["id"] == phone_number.id
            assert json_response["phone"] == phone_number.phone

    @pytest.mark.parametrize(
            "phone,customer_id,status_code",
            [
                ("0152098001", None, 201),
                ("0152098792", None, 409),
                ("0152098000", 9999, 400),
                ("0990008000", 9999, 400),
            ]
    )
    def test_create_phone_number(self, phone, customer_id, status_code, session, mock_customer, mock_phonerange, mock_phonenumber):
        customer_id = customer_id if customer_id else mock_customer.id
        new_phone = {
            "phone": phone,
            "customer_id": customer_id,
        }
        response = client.post(self.BASE_URL, json=new_phone)
        assert response.status_code == status_code
        if status_code == 201:
            json_response = response.json()
            assert json_response["phone"] == new_phone["phone"]
            assert json_response["phone_range_id"] == mock_phonerange.id
            new_phone_number = session.query(PhoneNumber).filter(
                PhoneNumber.id==json_response["id"],
            ).first()
            assert new_phone_number
        # Cleaning - shouldn't be needed
        session.delete(mock_customer)
        session.delete(mock_phonerange)
        session.commit()

    
    @pytest.mark.parametrize(
            "phone_id,status_code",
            [(None, 204), (9999, 404)],
        )
    def test_delete_phone_number(self, phone_id, status_code, session, mock_phonenumber):
        phone_number = mock_phonenumber
        phone_id = phone_id if phone_id else phone_number.id
        response = client.delete(f"{self.BASE_URL}/{phone_id}")
        assert response.status_code == status_code
        assert not session.query(PhoneNumber).filter(PhoneNumber.id==phone_id).first()
