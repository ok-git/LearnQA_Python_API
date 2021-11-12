# Необходимо написать скрипт, который создает GET-запрос на метод: https://playground.learnqa.ru/api/long_redirect
# С помощью конструкции response.history необходимо узнать, сколько редиректов происходит от изначальной точки
# назначения до итоговой. И какой URL итоговый.

import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect')

for i, el in enumerate(response.history, start=1):
    print(f'{i} запрос, url - {el.url}')

print(f'Итоговый запрос, url - {response.url}')
print(f'Всего редиректов {len(response.history)}')
