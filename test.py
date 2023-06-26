import requests


def test_book_room_successfully():
    room_id = 1
    url = f"https://ikromjonxusanov.jprq.live/api/rooms/{room_id}/book/"
    payload = {
        "resident": {"name": "Anvar Sanayev"},
        "start": "30-06-2023 09:00:00",
        "end": "30-06-2023 10:00:00",
    }
    response = requests.post(url, json=payload)
    print(response.text)
    assert response.status_code == 201
    return 1

print(test_book_room_successfully())