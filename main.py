import requests
import json
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

    def get_group_info_by_id(self, group_id=None):
        if group_id is not None:
            self.params['group_id'] = group_id
        self.params['fields'] = 'name,members_count'
        response = requests.get('https://api.vk.com/method/groups.getById', self.params)
        return response.json()['response']

    def save_to_json(self, data_to_save):
        with open('data.json', 'w') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)


def main():
    vk_id = '5030613'
    vk_data = MyVkClient(TOKEN)
    my_friends = vk_data.get_friends_by_id(vk_id)
    #  user_vk_groups = vk_data.get_groups_by_id(vk_id)
    count = len(my_friends)
    unique_vk_groups = set(vk_data.get_groups_by_id(vk_id))
    for friend in my_friends:
        print(count)
        friend_vk_groups = vk_data.get_groups_by_id(friend)
        if friend_vk_groups is not None:
            friend_vk_groups = set(friend_vk_groups)
            unique_vk_groups -= friend_vk_groups
            sleep(0.35)
        count = count - 1

    unique_vk_groups = list(unique_vk_groups)
    print(unique_vk_groups)

    new_list = []
    for ug in unique_vk_groups:
        new_dict = {}
        temp_dict = vk_data.get_group_info_by_id(ug)[0]
        new_dict['id'] = temp_dict['id']
        new_dict['name'] = temp_dict['name']
        new_dict['members_count'] = temp_dict['members_count']
        new_list.append(new_dict)

    vk_data.save_to_json(new_list)


if __name__ == '__main__':
    main()
