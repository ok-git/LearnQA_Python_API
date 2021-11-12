# с помощью библиотеки “json”, распарсить переменную json_text и вывести текст второго сообщения с помощью функции print

import json


def key_error(key):
    print(f'Ключа {key} в JSON нет')


json_as_string = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":' \
                 '"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
root_key = 'messages'
sub_key = 'message'
msg_number = 2

json_obj = json.loads(json_as_string)

if root_key in json_obj:
    if len(json_obj[root_key]) <= msg_number:
        if sub_key in json_obj[root_key][msg_number - 1]:
            print(json_obj[root_key][msg_number - 1][sub_key])
        else:
            key_error(sub_key)
    else:
        print(f'Сообщения №{msg_number} в списке сообщений нет')
else:
    key_error(root_key)

