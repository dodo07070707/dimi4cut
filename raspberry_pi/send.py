import requests
from path import IMG_DIR, SERVER


def post(user_id: int, pw: str) -> None:
    image_path = f'{IMG_DIR}/{user_id}.jpg'

    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}
        data = {'user_id': user_id, 'pw': pw}
        response = requests.post(SERVER, files=files, data=data)

    print("="*30, "="*30, "="*30, sep='\n')
    print(" "*30, " "*30, " "*30, sep='\n')
    print(response.json())
    print(" "*30, " "*30, " "*30, sep='\n')
    print("="*30, "="*30, "="*30, sep='\n')
