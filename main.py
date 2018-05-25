import requests
from Data.config import TOKEN
from time import sleep


class MyVkClient:
    def __init__(self, token):
        self.version = '5.78'
        self.token = token
        self.params = {
            'v': self.version,
            'access_token': self.token
        }

    def get_friends_by_id(self, user_id=None):
        if user_id is not None:
            self.params['user_id'] = user_id
        response = requests.get('https://api.vk.com/method/friends.get', self.params)
        return response.json()['response']['items']

    def get_groups_by_id(self, user_id=None):
        if user_id is not None:
            self.params['user_id'] = user_id
        response = requests.get('https://api.vk.com/method/groups.get', self.params)
        if 'error_code' in response.text:
            return None
        else:
            return response.json()['response']['items']


def main():
    vk_data = MyVkClient(TOKEN)
    my_friends = vk_data.get_friends_by_id('5030613')
    a = vk_data.get_groups_by_id('5030613')
    count = len(my_friends)

    a = set(a)
    print(a)
    for friend in my_friends:
        print(count)
        b = vk_data.get_groups_by_id(friend)
        if b is not None:
            b = set(b)
            a -= b
            sleep(0.35)
        count = count - 1
    print(a)


if __name__ == '__main__':
    main()