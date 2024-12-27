import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.models import PhoneRange

client = TestClient(app)


class TestPhoneRanges:
    BASE_URL = "/phone_ranges"

    def test_list_phone_ranges(self, mock_phonerange):
        phone_range = mock_phonerange
        response = client.get(self.BASE_URL)
        assert response.status_code == 200
        json_response = response.json()
        assert len(json_response) == 3
        assert json_response[-1]["lower"] == phone_range.lower
        assert json_response[-1]["upper"] == phone_range.upper

    @pytest.mark.parametrize(
            "range_id,status_code",
            [(None, 200), (9999, 404)],
        )
    def test_get_phone_range(self, range_id, status_code, mock_phonerange):
        phone_range = mock_phonerange
        range_id = range_id if range_id else phone_range.id
        response = client.get(f"{self.BASE_URL}/{range_id}")
        assert response.status_code == status_code
        json_response = response.json()
        if status_code == 200:
            assert json_response["lower"] == phone_range.lower
            assert json_response["upper"] == phone_range.upper

    def test_create_phone_range(self, session):
        new_range = {
            "lower": "0200000000",
            "upper": "0230000000",
        }
        response = client.post(self.BASE_URL, json=new_range)
        assert response.status_code == 201
        json_response = response.json()
        assert json_response["lower"] == new_range["lower"]
        assert json_response["upper"] == new_range["upper"]
        new_phone_range = session.query(PhoneRange).filter(
            PhoneRange.id==json_response["id"],
        ).first()
        assert new_phone_range
        # Cleaning - shouldn't be needed
        session.delete(new_phone_range)
        session.commit()

    
    @pytest.mark.parametrize(
            "range_id,status_code",
            [(None, 204), (9999, 404)],
        )
    def test_delete_phone_range(self, range_id, status_code, session, mock_phonerange):
        phone_range = mock_phonerange
        range_id = range_id if range_id else phone_range.id
        response = client.delete(f"{self.BASE_URL}/{range_id}")
        assert response.status_code == status_code
        assert not session.query(PhoneRange).filter(PhoneRange.id==range_id).first()
