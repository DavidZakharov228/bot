import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests

vk_session = vk_api.VkApi(token='vk1.a.gV418o9HEmTOQI2gPvO04uTQ_fzNuRTeH6ruGpoLL6ZtfSrf_QsYWEwGdtGEo2eZLdu7lkkdw8T-bg3gV7Lr8eR4I6H6Qmk9wDbN3vI8dRgR1qLUa3kLXoT3MjLddbZ-CoDmNmLFt1VNFvSscfHtwzPfkkiYyJN-Nq1GUi2abNf_jLTb2dj065ckqDJBxHswivvucSBLXFGLODaT3WaxLA') # введите токен вашей группы VK
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

def get_place_photo(place_name):
    # получаем координаты места
    geocode_url = 'https://geocode-maps.yandex.ru/1.x/?format=json&geocode={}'.format(place_name)
    response = requests.get(geocode_url).json()
    coordinates = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    # получаем фото места
    photo_url = 'https://static-maps.yandex.ru/1.x/?ll={}&size=400,400&z=15&l=map&pt={},pm2dgl'.format(coordinates, coordinates)
    return photo_url

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        place_name = event.text
        photo_url = get_place_photo(place_name)
        vk.messages.send(chat_id=event.chat_id, message=photo_url, random_id=event.random_id)