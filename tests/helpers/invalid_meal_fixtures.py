invalid_meal_fixtures = {
    "invalid_content_type" :
        "23456",
    "invalid_params_name":
        {
            "Name": "wierd meal",
            "appetizer": 1,
            "main": 2,
            "dessert": 3
        },
    "missing_params":
        {
            "appetizer": 1,
            "main": 2,
            "dessert": 3
        },
    "invalid_params_type":
        {
            "name": "Zuchini meal",
            "appetizer": 1.0,
            "main": 2,
            "dessert": 3
        },
    "invalid_dish_id":
        {
            "name": "Zuchini meal",
            "appetizer": 1,
            "main": 100,
            "dessert": 3
        }
}