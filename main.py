#!/usr/bin/python
# #coding:utf-8
from flask import Flask, request, session, redirect, url_for, render_template
import requests
import re
import base64
import mistune
from os import environ
from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

from helper import Helper
helper = Helper()

app = Flask(__name__, static_url_path='/static')
app.url_map.converters['regex'] = RegexConverter

# 初始化配置
statistics_code = environ.get('statistics_code', '')
blog_name = environ.get('blog_name', 'Blog')
owner = environ.get('owner', 'owner')
repo = environ.get('repo', 'blog.te.dog')
branch = environ.get('branch', 'master')
token = environ.get('token', '')
headers = {'Authorization': 'token {token}'.format(token=token)}

@app.route('/<regex(".*"):path>')
def index(path=''):
    title = blog_name
    if path == '+':
        path = ''
    path = helper.base64_decode_for_string(path)
    request_url = 'https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}'.format(owner=owner, repo=repo, branch=branch, path=path)
    print(request_url)
    request_result = requests.get(request_url, headers=headers)
    print(request_result.json())
    content = request_result.json()
    content_is_list = type(content) == list

    # 判断是否为报错信息
    if not content_is_list:
        if 'message' in content:
            return render_template('debug.html', content=content['message'])

    if not content_is_list:
        title = re.sub(r'\.md$|\.txt$|^.+\/', '', path)
        content_markdown_string = base64.b64decode(content['content']).decode('utf-8')
        content['original_content'] = content_markdown_string
        # 处理 markdown 中的图片
        def test(matched):
            image_markdown_str = str(matched.group('value'))
            image_file_path = re.sub(r'\!\[\]\(|\)|\!\[Image\]\(', '', image_markdown_str)
            image_file_uri = 'https://raw.githubusercontent.com/{user}/{repo}/{branch}/{filename}'.format(user=owner, repo=repo,branch=branch,filename=image_file_path)
            return '![](' + image_file_uri + ')'
        content_markdown_string = re.sub('(?P<value>\!\[\]\(.+\)|\!\[Image\]\(.+\))', test, content_markdown_string)
        # 解析 markdown 为 html
        content['content'] = mistune.markdown(content_markdown_string)
        # get lastest commit information
        request_url = 'https://api.github.com/repos/{owner}/{repo}/commits?path={path}&ref={branch}'.format(owner=owner, repo=repo, branch=branch, path=path)
        print(request_url)
        request_result = requests.get(request_url, headers=headers)
        print(request_result.json())
        content['commit_info'] = request_result.json()[0]

    return render_template('index.html', content=content, re=re, type=type, list=list, base64encode=helper.base64_encode_for_string, blog_name=blog_name, statistics_code=statistics_code, title=title)

@app.route('/demo')
def demo():
    return render_template('index.html', content='hello,world', type=type, list=list, statistics_code=statistics_code)

if __name__ == '__main__':
    app.run(debug=True)