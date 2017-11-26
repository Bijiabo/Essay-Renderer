from flask import Flask, request, session, redirect, url_for, render_template
import requests
import re
import base64
import mistune
from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

owner = 'bijiabo'
repo = 'blog.te.dog'
branch = 'master'

# @app.route('/')
# @app.route('/<path>')
@app.route('/<regex(".*"):path>')
def index(path=''):
    request_url = 'https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}'.format(owner=owner, repo=repo, branch=branch, path=path)
    print(request_url)
    request_result = requests.get(request_url)
    print(request_result.json())
    content = request_result.json()
    content_is_list = type(content) == list
    if not content_is_list:
        content_markdown_string = base64.b64decode(content['content']).decode('utf-8')
        content['content'] = mistune.markdown(content_markdown_string)
    return render_template('index.html', content=content, re=re, type=type, list=list)

@app.route('/demo')
def demo():
    return render_template('index.html', content='hello,world', type=type, list=list)

if __name__ == '__main__':
    app.run(debug=True)