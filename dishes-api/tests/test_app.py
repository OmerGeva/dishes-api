from unittest.mock import MagicMock, patch


def make_dish(client, dish):
    with patch('src.services.GetNutritionalValue.call') as mock_call:
        mock_call.return_value = {
            'name': dish['name'],
            'cal': 100,
            'sodium': 200,
            'sugar': 300
        }
        return client.post("/dishes", json = dish)
