import time
import requests
from django.utils import timezone

from B4 import models
from NB4444 import settings


def get_now():
    return timezone.now()


def get_today():
    return timezone.now().date()


class Variables:
    # telegram api settings
    method = "getUpdates"
    token = settings.TELEGRAM_BOT_TOKEN

    # message_id log file
    file_path = './botV4/logs/'

    @classmethod
    def record_error_log(cls, error):
        log_error_directory = cls.file_path + "error/"
        log_error_file_name = log_error_directory + f"error_{get_today()}.log"
        with open(log_error_file_name, "a") as file:
            file.write(f"{get_now()} __ {error}\n")


class Connect:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    @staticmethod
    def insert_to_db(response_list, **kwargs):
        for message in response_list:
            models.Note.objects.create(
                text=message
            )


def get_response_telegram():
    def to_request():
        try:
            request_url = f"https://api.telegram.org/bot{token}/{method}"
            print(request_url)
            return requests.request("get", request_url)
        except Exception as e:
            print(e)
            Variables.record_error_log(e)
            return None

    token = Variables.token
    method = Variables.method
    file_path = Variables.file_path
    log_file_name = f"{file_path}{get_today()}_update_id_list.log"
    while not to_request():
        print("sleep")
        time.sleep(30)

    response = to_request()
    response_json = response.json()
    if not response_json.get('ok'):
        return None
    open(log_file_name, "a")
    with open(log_file_name, "r") as file:
        update_id_list = [line.strip() for line in file]
    response_list, log_list = dict(), set()
    for message in response_json['result']:
        try:
            if message.get('update_id') or message.get('edited_message'):
                message_key = 'message' if message.get('message') else 'edited_message'
                if str(message[message_key]['message_id']) not in update_id_list:
                    response_list.update({message[message_key]['message_id']: message[message_key]['text']})
                    log_list.add(message[message_key]['message_id'])
        except Exception as e:
            print(f"Error in loop! {str(e)}")
            Variables.record_error_log(e)
    with open(log_file_name, "a") as file:
        for item in log_list:
            file.write(f"{item}\n")
    return response_list.values()


def receive_records_from_telegramm_bot():
    try:
        print("Start")
        response_list = get_response_telegram()
        if response_list:
            Connect.insert_to_db(response_list)
            print("Success")
    except Exception as e:
        print(f"Error! {str(e)}")
        Variables.record_error_log(e)
    finally:
        print("End")


if __name__ == "__main__":
    receive_records_from_telegramm_bot()
