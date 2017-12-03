from os import environ

class _Config:
    statistics_code = environ.get('statistics_code', '')
    blog_name = environ.get('blog_name', 'Blog')
    owner = environ.get('owner', 'owner')
    repo = environ.get('repo', 'blog.te.dog')
    branch = environ.get('branch', 'master')
    token = environ.get('token', '')

    def __init__(self):
        print('Config init.')
        self.load()

    def load(self):
        self.statistics_code = environ.get('statistics_code', '')
        self.blog_name = environ.get('blog_name', 'Blog')
        self.owner = environ.get('owner', 'owner')
        self.repo = environ.get('repo', 'blog.te.dog')
        self.branch = environ.get('branch', 'master')
        self.token = environ.get('token', '')

    def dict_of_all(self):
        return {
            "statistics_code": self.statistics_code,
            "blog_name": self.blog_name,
            "owner": self.owner,
            "repo": self.repo,
            "branch": self.branch,
            "token": self.token
        }

    @property
    def headers(self):
        return {'Authorization': 'token {token}'.format(token=self.token)}

    
config = _Config()