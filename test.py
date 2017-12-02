from os import environ
from api import api
from data_types.template_render_data import Template_Render_Data

# setup environment variable
class Assistant:
    def __init__(self):
        print('Test Assistan init.')

    def clearEnvironment(self):
        print('start clear environment...')
        del environ['statistics_code']
        del environ['blog_name']
        del environ['owner']
        del environ['repo']
        del environ['branch']
        del environ['token']
        del environ['headers']
        print('clear environemnt done')

    def setupEnvironmentVarible(self):
        print('start setup environment...')
        environ['statistics_code'] = ''
        environ['blog_name'] = 'Blog.test'
        environ['owner'] = 'owner.test'
        environ['repo'] = 'blog.te.dog.test'
        environ['branch'] = 'master.test'
        environ['token'] = '.test'
        print('setup environemnt done')

assistant = Assistant()

if __name__ == '__main__':
    # assistant.clearEnvironment()
    assistant.setupEnvironmentVarible()
    api.reloadConfig()
    api.get_content_for_path('hello')

    data = Template_Render_Data()
    print(data.data)
    data.path = 'a/b/c'
    print(data.data)
    data.path = 'a/b/c/d'
    print(data.data)
    data.path = 'a'
    print(data.data)
    data.path = ''
    print(data.data)