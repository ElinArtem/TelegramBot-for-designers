import telebot
from telebot import types

from openai_connection import *

from cfg import CONFIG
import json
import base64


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  

class TelegramBot(telebot.TeleBot):
    def __init__(self, api: str) -> None:
        super().__init__(api)


bot = TelegramBot(api=CONFIG.get("Telegram_API"))
users_file = CONFIG.get('USER_FILE')


def save_to_json(data):
    try:
        with open(users_file, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {users_file} successfully.")
    except Exception as e:
        print(f"Error saving data to {users_file}: {str(e)}")


def conect_json():    
    try:
        with open(users_file) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}  # Return empty dictionary if JSON is invalid


@bot.message_handler(commands=["start"])
def start(message: types.Message) -> None:
    logged_in_users = conect_json()

    # Check if user is already logged in
    if str(message.from_user.id) in logged_in_users:
        bot.send_message(
            message.chat.id, 
            f"С возвращением, <b>{message.from_user.first_name}</b>!\n"
            "Рады вас видеть!", 
            parse_mode="html",
            reply_markup=menu_markup()
        )
    else:
        # Ask for password
        bot.send_message(
            message.chat.id,
            "Приветствуем вас!\n"
            "Для входа в систему бота требуется ввести пароль:"
        )
        bot.register_next_step_handler(message, login)


# Login function that handles the password check
def login(message: types.Message) -> None:
    logged_in_users = conect_json()

    # Check if password is correct
    if message.text == CONFIG.get("Password"):
        logged_in_users[str(message.from_user.id)] = {
            "first_name": message.from_user.first_name,
            "username": message.from_user.username
        }
        save_to_json(logged_in_users)

        bot.send_message(
            message.chat.id, 
            f"Добро пожаловать, <b>{message.from_user.first_name}</b>!\nВы успешно вошли в систему.", 
            parse_mode="html",
            reply_markup=menu_markup()
        )
    else:
        bot.send_message(
            message.chat.id, 
            "Неверный пароль. Попробуйте еще раз."
        )
        bot.register_next_step_handler(message, login)


@bot.message_handler(content_types=['text'])
def main(message: types.Message):
    logged_in_users = conect_json()
    text = message.text.lower()
    if str(message.from_user.id) in logged_in_users:
        if text in ["описание", "создать описание", "описание по картинке"]:
            create_discription(message)

        elif text in ["помощь", "help", "помогите", "нужна помощь"]:
            help_message = (
                "Если у вас возникли проблемы вы можете оправить запрос в нашу тех. поддержку для решения вашей проблемы\n"
                "Введите ваш вопрос:"
            )
            bot.send_message(message.chat.id, help_message, parse_mode="html", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, help)
        elif text in ["перезагрузить систему"]:
            start(message)
        
        else: 
            bot.send_message(message.chat.id, "Я не знаю, что ответить на это.", parse_mode="html", reply_markup=menu_markup())
    else:
        bot.send_message(message.chat.id, "Вы не авторизованы. Введите пароль для подтверждения:", parse_mode="html", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, login)


def create_discription(message: types.Message) -> None:
    message_to_send = 'Отправьте изображение с жатием (форматы: .jpg, .png), для которого нужно подготовить описание'

    bot.send_message(
        message.chat.id, 
        message_to_send,
        parse_mode="html",
        reply_markup=types.ReplyKeyboardRemove()
    )
    
    bot.register_next_step_handler(message, handle_photo)


def handle_photo(message: types.Message) -> None:
    if message.content_type != 'photo':
        bot.reply_to(message, "Пожалуйста, повторите попытку, отправьте фото.")
        return  # Exit if no photo is sent
    
    # Handle the first photo (in case multiple photos are sent)
    photo = message.photo[1].file_id

    message_type = "Пожалуйста, выбирите из списка тип написания описания"
    bot.send_message(
        message.chat.id,
        message_type,
        parse_mode="html",
        reply_markup=choose_markup()
    )
    
    bot.register_next_step_handler(message, handle_type, photo)
    

def handle_type(message: types.Message, photo: str) -> None:
    try:
        file_info = bot.get_file(photo)
        file_path = file_info.file_path

        # Download the file
        downloaded_file = bot.download_file(file_path)

        # Save the file locally
        with open(f'{message.chat.id}.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)

        type_of_discription = message.text

        send_discription(message, type_of_discription)

    except Exception as e:
        bot.send_message(1102084410, (
            f'У пользователя @{message.from_user.username}\n'
            f"Произошла ошибка при обработке фото: {e}"
            ))


def send_discription(message: types.Message, type_of_discription):

    bot.send_message(message.chat.id, "Мы обрабатываем изображение, это займет несколько секунд", reply_markup= types.ReplyKeyboardRemove())

    def to_link(message):
        base64_image = encode_image(f"{message.chat.id}.jpg")
        link = f"data:image/jpeg;base64,{base64_image}"

        return link
    
    link = to_link(message)

    discription = description_by_image(link, type_of_discription)

    bot.send_message(message.chat.id, discription, parse_mode="html", reply_markup=menu_markup())


def help(message: types.Message):
    bot.send_message(
        1102084410,
        (
            f"Пришел запрос о помощи от @{message.from_user.username}\n\n"
            "Текст сообщения:\n"
            f"{message.text}"
        )
    )
    bot.send_message(message.chat.id, "Помощь будет предоставлена в ближайшее время, с вами свяжутся", reply_markup=menu_markup())


def menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = 'создать описание'
    item2 = 'нужна помощь'
    item3 = "перезагрузить систему"

    markup.row(item1)
    markup.row(item2)
    markup.row(item3)

    return markup


def choose_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = 'От лица дизайнера'
    item2 = 'От лица клиента'
    item3 = 'От лица бренда'
    item4 = "От лица эксперта"

    markup.row(item1)
    markup.row(item2)
    markup.row(item3)
    markup.row(item4)

    return markup


bot.polling(non_stop=True)

if __name__ == "__main__":
    flag = True
    while flag:
        try:
            bot.polling(non_stop=True, timeout=10)
        except:
            flag = True
