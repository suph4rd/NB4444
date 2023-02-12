import io
import operator
from typing import Optional

import requests
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from django.utils.datastructures import MultiValueDict

from B4 import models as b4_models, forms as b4_forms
from NB4444 import settings
from tele_bot.exceptions import PhotoError, NoneVariablesException


def get_now():
    return timezone.now()


def get_today():
    return timezone.now().date()


class Variables:
    method = "getUpdates"
    token = settings.TELEGRAM_BOT_TOKEN
    file_path = './tele_bot/logs/'
    update_url = "https://api.telegram.org/"

    @classmethod
    def record_error_log(cls, error):
        log_error_directory = cls.file_path + "error/"
        log_error_file_name = log_error_directory + f"error_{get_today()}.log"
        with open(log_error_file_name, "a") as file:
            file.write(f"{get_now()} __ {error}\n")


class ResultKeeper:
    _text_results: Optional[dict] = None
    _photo_results: Optional[dict] = None
    _current_bot_user = None
    _bot_username = "telegram_bot_user"

    def __init__(self, text_results, photo_results):
        self._text_results = text_results
        self._photo_results = photo_results
        self._check_bot_user()

    def save(self):
        self._save_text_results()
        self._save_photo_results()

    def _check_bot_user(self):
        user = b4_models.User.objects.filter(username=self._bot_username).first()
        if not user:
            user = b4_models.User(
                username=self._bot_username,
                password="Telegrambotuser2023"
            )
            user.save()
        self._current_bot_user = user

    def _save_text_results(self):
        messages = list(map(lambda x: x["text"], self._text_results.values()))
        if messages:
            message_list = [b4_models.Note(text=message, user_id=self._current_bot_user.id) for message in messages]
            b4_models.Note.objects.bulk_create(message_list)

    def _save_photo_results(self):
        for id_, obj in self._photo_results.items():
            file = io.BytesIO(obj["response_dict"]["response"].content)
            size = file.getbuffer().nbytes

            in_memory_uploaded_file = InMemoryUploadedFile(
                file=file,
                field_name="image",
                name=f"{obj['response_dict']['file_id']}.png",
                content_type="image/png",
                size=size,
                charset=None
            )
            form = b4_forms.NoteModelForm(
                data=MultiValueDict({"text": [""], "user": [self._current_bot_user]}),
                files=MultiValueDict({'image': [in_memory_uploaded_file]})
            )

            if not form.is_valid():
                raise ValidationError(form.errors)

            form.save()


class BotLoader:
    __update_id_list: list = None

    _token: str = None
    _method: str = None
    _file_path: str = None
    _update_url: str = None

    def __init__(self):
        if not Variables.token:
            raise NoneVariablesException("Токен отсутствует!")

        self._token = Variables.token
        self._method = Variables.method
        self._file_path = Variables.file_path
        self._telegram_api_url = Variables.update_url

    @property
    def log_file_name(self):
        return f"{self._file_path}{get_today()}_update_id_list.log"

    def get_response_telegram(self):
        response = self._to_request()
        response_json = response.json()

        if not response_json.get('ok'):
            return None, None

        self._init_log_file()
        text_results, photo_results, log_list = self._handle_response(response_json)
        self._finish_log_file(log_list)

        return text_results, photo_results

    def _handle_response(self, response_json):
        log_list = set()
        text_results, photo_results = {}, {}
        for message_obj in response_json['result']:
            try:
                if message_obj.get('update_id') or message_obj.get('edited_message'):
                    message_key = 'message' if message_obj.get('message') else 'edited_message'
                    if str(message_obj[message_key]['message_id']) not in self.__update_id_list:
                        if "text" in message_obj[message_key]:
                            text_results.update({message_obj[message_key]['message_id']: {
                                    "text": message_obj[message_key]["text"],
                                    "type": "text"
                                }
                            })
                        if 'photo' in message_obj[message_key]:
                            photo_response_dict = self._get_photo_response(message_obj, message_key)
                            photo_results.update({message_obj[message_key]['message_id']: {
                                "response_dict": photo_response_dict,
                                "type": "photo"
                            }})
                        log_list.add(message_obj[message_key]['message_id'])
            except Exception as e:
                print(f"Error in loop! {str(e)}")
                Variables.record_error_log(e)

        return text_results, photo_results, log_list

    def _is_update_not_exist(self, message_obj, message_key):
        return str(message_obj[message_key]['message_id']) not in self.__update_id_list

    def _get_photo_response(self, message_obj, message_key):
        file_options = max(message_obj[message_key]["photo"], key= lambda x: operator.getitem(x, "file_size"))
        if not file_options:
            raise PhotoError("file_options is absent for message ", message_obj["update_id"])

        params = {
            "file_id": file_options["file_id"]
        }
        file_info_response = requests.get(f"{self._telegram_api_url}bot{self._token}/getFile", params=params)
        if not file_info_response.ok:
            raise PhotoError("File info hasn't gotten for message ", message_obj["update_id"])

        file_info_response_json = file_info_response.json()
        if not file_info_response_json["ok"]:
            raise PhotoError("File info hasn't gotten for message ", message_obj["update_id"])

        file_path = file_info_response_json["result"]["file_path"]
        file_response = requests.get(
            f"{self._telegram_api_url}file/bot{self._token}/{file_path}"
        )

        if not file_response.ok:
            raise PhotoError("File hasn't gotten for message ", message_obj["update_id"])

        result = {
            "response": file_response,
            "file_id": file_options["file_id"]
        }
        return result

    def _init_log_file(self):
        with open(self.log_file_name, "a") as file:
            pass
        with open(self.log_file_name, "r") as file:
            self.__update_id_list = [line.strip() for line in file]

    def _finish_log_file(self, log_list: set):
        with open(self.log_file_name, "a") as file:
            for item in log_list:
                file.write(f"{item}\n")

    def _to_request(self):
        try:
            request_url = f"{self._telegram_api_url}bot{self._token}/{self._method}"
            print(request_url)
            return requests.request("get", request_url)
        except Exception as e:
            print(e)
            Variables.record_error_log(e)
            raise e


def receive_records_from_telegram_bot():
    try:
        print("Start")
        bot_loader = BotLoader()
        text_results, photo_results = bot_loader.get_response_telegram()
        if any([text_results, photo_results]):
            # todo: save username info (id, username, first_name)
            result_keeper = ResultKeeper(text_results, photo_results)
            result_keeper.save()
            print("Success")
    except Exception as e:
        print(f"Error! {str(e)}")
        Variables.record_error_log(e)
        raise e
    finally:
        print("End")


if __name__ == "__main__":
    raise RuntimeError("This file is the part of django project")
