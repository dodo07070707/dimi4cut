import requests
url = requests.get("localhost:8000/register/")
IMG_DIR = ''


def post(user_id: int, pw: str):
    image_path = f'{IMG_DIR}/{user_id}'

    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}
        data = {'user_id': user_id, 'pw': pw}
        response = requests.post(url, files=files, data=data)

    print(response.json())
