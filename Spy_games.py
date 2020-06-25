import requests
import time
import json


TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


class UserVK():

    def __init__(self, token: str) -> None:
        self.token = token


    def get_params(self):
        return {
        'access_token': TOKEN,
        'v': 5.89,
    }


    def user(self, username, id):
        self.username = username
        self.id = id
        return f'Исследование проводится для пользователя {username} - id {id}'

    def get_groups_user(self) -> dict:
        params = self.get_params()
        params['extended'] = 1
        params['fields']: {}
        respons = requests.get(
        'https://api.vk.com/method/groups.get',
        params
        )
        time.sleep(1)
        for index, call in enumerate(respons, 1):
            print(index)
        return respons.json()

    def get_dict_groups_user(self) -> dict:
        dict_groups_user = {}
        user_groups = self.get_groups_user()
        user_groups_temp = [user_groups['response']['items']]
        for groups in user_groups_temp:
            for group in groups:
                dict_groups_user[(group['id'])] = [group['name']]
        return dict_groups_user

    def get_members_groups_user(self) -> list:
        list_groups = []
        dict_groups_user = self.get_dict_groups_user()
        for keys, value in dict_groups_user.items():
            params = self.get_params()
            params['group_id'] = keys
            respons_mem = requests.get(
                'https://api.vk.com/method/groups.getMembers',
                params
            )
            time.sleep(2)
            rj = respons_mem.json()
            for index, call in enumerate(rj, 1):
                print(index)
                dict_groups = {'name': [], 'gid': [], 'members_count': []}
                dict_groups['name'].append(value),
                dict_groups['gid'].append(keys),
                dict_groups['members_count'].append(rj['response']['count'])
            list_groups.append(dict_groups)
        return list_groups

    def get_groups_user_with_friends(self) -> list:
        list_groups_fr = []
        dict_groups_user = self.get_dict_groups_user()
        for keys, value in dict_groups_user.items():
            params = self.get_params()
            params['group_id'] = keys
            params['filter'] = 'friends'
            respons_mem = requests.get(
                'https://api.vk.com/method/groups.getMembers',
                params
            )
            time.sleep(2)
            rj = respons_mem.json()
            for index, call in enumerate(rj, 1):
                print(index)
                new_dict = {'name': [], 'gid': [], 'members_count': []}
                new_dict['name'].append(value),
                new_dict['gid'].append(keys),
                new_dict['members_count'].append(rj['response']['count'])
            list_groups_fr.append(new_dict)
        return list_groups_fr

    def get_groups_user_without_friends(self) -> list:
        final_groups = []
        gids = []
        list_groups = self.get_members_groups_user()
        list_groups_fr = self.get_groups_user_with_friends()
        for group in list_groups_fr:
            if group['members_count'] == [0]:
               gids.append(group['gid'])
        for groups in list_groups:
            if groups['gid'] in gids:
                final_groups.append(groups)
        print(f'Группы пользователя, в которых не состоят его друзья: {final_groups}')
        return final_groups

    def write_dict_to_file(self) -> json:
        list_groups = self.get_groups_user_without_friends()
        total_len = len(list_groups)
        for index, call in enumerate(list_groups, 1):
            print(f"Processing {index} / {total_len}")
        with open('groups.json', 'w', encoding='utf-8') as f:
            json.dump(list_groups, f, ensure_ascii=False, indent=2)
        return 'groups.json'
