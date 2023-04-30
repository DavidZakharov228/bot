import vk_api
import datetime
import wikipedia
import re
from vk_api.longpoll import VkLongPoll, VkEventType

# Функция для отправки сообщения пользователю
def send_message(chat_id, message):
    vk.messages.send(
        chat_id=chat_id,
        message=message,
        random_id=vk_api.utils.get_random_id()
    )

# Функция для обработки сообщений
def handle_message(chat_id, message):
    # Проверяем, есть ли в сообщении слово "сейчас"
    if "сейчас" in message:
        now = datetime.datetime.now()
        send_message(chat_id, now.strftime("Сегодня %d.%m.%Y, время %H:%M:%S"))
    # Проверяем, есть ли в сообщении слово "википедия"
    elif "википедия" in message.lower():
        query = re.search(r'википедия (.+)', message.lower()).group(1)
        try:
            page = wikipedia.page(query)
            summary = wikipedia.summary(query, sentences=3)
            send_message(chat_id, f"{page.title}\n\n{summary}\n\n{page.url}")
        except wikipedia.exceptions.PageError:
            send_message(chat_id, f"Страница по запросу '{query}' не найдена в Википедии.")
        except wikipedia.exceptions.DisambiguationError as e:
            options = "\n".join(e.options)
            send_message(chat_id, f"Уточните запрос '{query}', возможно вы имели в виду:\n\n{options}")
    # Проверяем, является ли сообщение примером
    elif re.match(r'\d+\s*[+*\/-]\s*\d+', message):
        result = eval(message)
        send_message(chat_id, f"{message} = {result}")
    # Если ничего не подошло, просто приветствуем пользователя
    else:
        send_message(chat_id, f"Привет, {vk.users.get(user_id=chat_id)[0]['first_name']}! Я могу помочь тебе найти информацию на Википедии или решить математический пример. Просто напиши мне, что тебе нужно.")

# Авторизуемся в ВКонтакте
vk_session = vk_api.VkApi(token='vk1.a.gV418o9HEmTOQI2gPvO04uTQ_fzNuRTeH6ruGpoLL6ZtfSrf_QsYWEwGdtGEo2eZLdu7lkkdw8T-bg3gV7Lr8eR4I6H6Qmk9wDbN3vI8dRgR1qLUa3kLXoT3MjLddbZ-CoDmNmLFt1VNFvSscfHtwzPfkkiYyJN-Nq1GUi2abNf_jLTb2dj065ckqDJBxHswivvucSBLXFGLODaT3WaxLA')
vk = vk_session.get_api()

# Получаем Long Poll сервер
long_poll = vk_api.longpoll.VkLongPoll(vk_session)

# Обрабатываем новые сообщения
for event in long_poll.listen():
    if event.type == vk_api.longpoll.VkEventType.MESSAGE_NEW:
        chat_id = event.chat_id
        message = event.text
        handle_message(chat_id, message)