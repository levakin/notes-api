import requests


def test_reqs():
    url = 'http://127.0.0.1:8080/'

    requests.post(url=url, json={'title': 'Текст заголовка', 'text': 'Текст заметки'})

    r = requests.post(url=url, json={'title': 'Текст заголовка 2',
                                     'text': 'Текст заметки 2'})
    note_id = r.json()['id']
    requests.request(method="UPDATE", url=url, json={'id': note_id,
                                                     'title': 'Текст заголовка 2',
                                                     'text': 'Текст заметки 2 обновленный'})

    r = requests.post(url=url, json={'title': 'Test title',
                                     'text': "Lorem ipsum"})
    note_id = r.json()['id']
    requests.request(method="UPDATE", url=url, json={'id': note_id,
                                                     'title': 'Updated title',
                                                     'text': 'Updated Lorem ipsum'})

    r = requests.post(url=url, json={'title': 'To be deleted',
                                     'text': "To be deleted"})
    note_id = r.json()['id']
    r = requests.delete(url=url, json={'id': note_id})
