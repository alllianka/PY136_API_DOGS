import requests
import sys
import json
from tokens import token
from tqdm import tqdm
import time

log_list = []
count = 0
breed = input("Введите название породы на английском языке:").strip().lower()  # gпользователь вводит название породы
dogs_url = f'https://dog.ceo/api/breed/{breed}'                                # формируется URL запрос
breed_response = requests.get(dogs_url+'/images/random')
if breed_response.status_code!=200 and breed_response.json()['status']=='error': # проверка, что введена порода? существующая на сайте
    print('Такая порода не найдена')
    sys.exit(1)
breed_link = breed_response.json()['message']  # получить ссылку на фото собаки
log_list.append(breed_response.json())
breed_photo_name = breed_link.split('/')[-1]   # получить название фото собаки
count+=1

yd_url = 'https://cloud-api.yandex.net/v1/disk/resources'
headers = {'Authorization': f'OAuth {token}'}
params = {'path': f'pd-136/{breed}'}
create_folder_response = requests.put(yd_url, params=params, headers=headers) # создать папку с названием породы собаки

upload_yd_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
params = {
    'url' : breed_link,
    'path': f'pd-136/{breed}/{breed}_{breed_photo_name}'}
upload_folder_response = requests.post(upload_yd_url, params=params, headers=headers) # загрузить фото собаки в папку

# проверка на сущесвтование под-пород
sub_breed_response = requests.get(dogs_url+'/list')
if sub_breed_response.json()['message'] == []:
    print('Такая порода не имеет под-пород')
else:
    for sub_breed in sub_breed_response.json()['message']:
        sub_breed_image = requests.get(f'{dogs_url}/{sub_breed}/images/random')
        count +=1
        sub_breed_image_link = sub_breed_image.json()['message']
        sub_breed_photo_name = sub_breed_image_link.split('/')[-1]   # получить название фото под-породы
        # загрузить фото под-породы на диск в папку /порода/под-порода+название_фото
        upload_yd_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'url': sub_breed_image_link,
            'path': f'pd-136/{breed}/{sub_breed}_{sub_breed_photo_name}'}
        upload_folder_response = requests.post(upload_yd_url,
                                               params=params,
                                               headers=headers)  # загрузить фото собаки в папку
        log_list.append(sub_breed_image.json())

# сериализуем список в текстовую структуру JSON
json_string = json.dumps(log_list)
# записываем log в JSON файл
with open(f"{breed}.json", "w", encoding="utf-8") as log_file:
    json.dump(json_string, log_file)

my_list = list(range(1, count + 1))
for i in tqdm(my_list):
    time.sleep(1)



