import requests
from config import config

class API:
    def __init__(self):
        print('API init.')
        config.load()

    def reloadConfig(self):
        config.load()

    def get_content_for_path(self, path):
        all_config = config.dict_of_all()
        request_url = 'https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}' .format(path=path, **all_config)
        request_result = requests.get(request_url, headers=config.headers)
        return request_result

    def get_commit_info_for_path(self, path):
        all_config = config.dict_of_all()
        request_url = 'https://api.github.com/repos/{owner}/{repo}/commits?path={path}&ref={branch}' .format(path=path, **all_config)
        request_result = requests.get(request_url, headers=config.headers)
        return request_result


api = API()

if __name__ == '__main__':
    api.get_content_for_path('hello')