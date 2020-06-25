from Spy_games import UserVK, TOKEN

if __name__ == '__main__':
    eshmargunov = UserVK(TOKEN)
    print(eshmargunov.user('eshmargunov', '171691064'))
    print(eshmargunov.write_dict_to_file())
