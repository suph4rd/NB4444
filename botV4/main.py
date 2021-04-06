import datetime
import psycopg2
import requests


class Variables:
    # telegram api settings
    method = "getUpdates"
    token = "1232067764:AAH9Y6sts9-rcoLAnAI5CH--jzsUBwRjkGc"

    # db settings
    db_name = "nb4444"
    db_host = "localhost"
    db_user = "nb4444"
    db_password = "1234"
    db_port = 5432


class Connect:
    instance = None
    db_name = Variables.db_name
    db_host = Variables.db_host
    db_user = Variables.db_user
    db_password = Variables.db_password
    db_port = Variables.db_port

    def __new__(cls, *args, **kwargs):
        if not Connect.instance:
            Connect.instance = super().__new__(cls, *args, **kwargs)
        return Connect.instance

    def __init__(self, **kwargs):
        self.db_host = kwargs.get('db_host', Connect.db_host)
        self.db_port = kwargs.get('db_host', Connect.db_port)
        self.db_name = kwargs.get('db_name', Connect.db_name)
        self.db_user = kwargs.get('db_user', Connect.db_user)
        self.db_password = kwargs.get('db_passresponse_listword', Connect.db_password)

    @staticmethod
    def insert_to_db(response_list, **kwargs):
        connect = Connect(**kwargs)
        with psycopg2.connect(
                host=connect.db_host,
                port=connect.db_port,
                dbname=connect.db_name,
                user=connect.db_user,
                password=connect.db_password
        ) as psycopg2_connect:
            with psycopg2_connect.cursor() as cursor:
                for message in response_list:
                    cursor.execute(f'INSERT INTO public."B4_nlg"(date_nlg, text_nlg, image_nlg) VALUES '
                                   f'(\'{datetime.datetime.today()}\', \'{message}\', \'\' );')
                    psycopg2_connect.commit()


def get_response_telegram():
    def to_request():
        try:
            return requests.request("get", f"https://api.telegram.org/bot{token}/{method}")
        except:
            return None

    token = Variables.token
    method = Variables.method
    lig_file_name = f"{datetime.date.today()}_update_id_list.log"
    while not to_request():
        print("sleep")

    response = to_request()
    response_json = response.json()
    if not response_json.get('ok'):
        return None
    open(lig_file_name, "a")
    with open(lig_file_name, "r") as file:
        update_id_list = [line.strip() for line in file]
    response_list, log_list = [], []
    for message in response_json['result']:
        if str(message['update_id']) not in update_id_list:
            response_list.append(message['message']['text'])
            log_list.append(message['update_id'])
    with open(lig_file_name, "a") as file:
        for item in log_list:
            file.write(f"{item}\n")
    return response_list


def main():
    response_list = get_response_telegram()
    if response_list:
        Connect.insert_to_db(response_list)
        print("Success")


if __name__ == "__main__":
    main()
