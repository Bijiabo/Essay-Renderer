from helper import Helper
helper = Helper()

class Template_Render_Data:
    _path = ''
    parent_path = ''
    title = ''
    content = ''

    def __init__(self):
        print('init Template_Render_Data')

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        print('path: ' + value)
        self._path = value
        self.parent_path = helper.path__parent_path(value)
    
    @property
    def data(self):
        print(self._path)
        _data = {
            'path': self.path,
            'parent_path': self.parent_path,
            'title': self.title,
            'content': self.content
        }
        return _data