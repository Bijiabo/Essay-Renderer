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
        print(request_url)


api = API()

if __name__ == '__main__':
    api.get_content_for_path('hello')