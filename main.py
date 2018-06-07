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

    def find_unique_groups(self, user_vk_groups, user_vk_friends):
        count = len(user_vk_friends)
        user_vk_groups = set(user_vk_groups)
        for friend in user_vk_friends:
            print(count)
            friend_vk_groups = self.get_groups_by_id(friend)
            if friend_vk_groups is not None:
                friend_vk_groups = set(friend_vk_groups)
                user_vk_groups -= friend_vk_groups
                sleep(0.35)
            count = count - 1
        return list(user_vk_groups)

    def formatting_list_groups(self, list_groups):
        tmp_list = []
        for ug in list_groups:
            new_dict = {}
            temp_dict = self.get_group_info_by_id(ug)[0]
            new_dict['id'] = temp_dict['id']
            new_dict['name'] = temp_dict['name']
            new_dict['members_count'] = temp_dict['members_count']
            tmp_list.append(new_dict)
        return tmp_list

    def save_to_json(self, data_to_save, vk_id=None):
        if vk_id is None:
            vk_id = 'data'
        with open(vk_id+'.json', 'w') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        return None


def main():
    vk_id = '5030613'
    vk_data = MyVkClient(TOKEN)
    user_friends = vk_data.get_friends_by_id(vk_id)
    user_vk_groups = vk_data.get_groups_by_id(vk_id)
    unique_vk_groups = vk_data.find_unique_groups(user_vk_groups, user_friends)
    formatted_list = vk_data.formatting_list_groups(unique_vk_groups)
    vk_data.save_to_json(formatted_list, vk_id)


if __name__ == '__main__':
    main()
