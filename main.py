#!/usr/bin/python
# #coding:utf-8
from flask import Flask, request, session, redirect, url_for, render_template
import requests
import re
import base64
import mistune
import urllib.parse
from os import environ
from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

from helper import Helper
helper = Helper()
from data_types.template_render_data import Template_Render_Data
from api import api

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

@app.route('/favicon.ico')
def facicon():
    return ''

@app.route('/<regex(".*"):path>')
def index(path=''):
    template_render_data = Template_Render_Data()
    if path == '+':
        path = ''
    
    # print('parent path:' + helper.path__parent_path(path))
    path = urllib.parse.unquote(path)
    template_render_data.path = path
    template_render_data.title = blog_name

    # 获取主要内容
    content = api.get_content_for_path(path).json()
    template_render_data.is_list = type(content) == list

    # 判断是否为报错信息
    if not template_render_data.is_list:
        if 'message' in content:
            return render_template('debug.html', content=content['message'], template_render_data=template_render_data)

    if template_render_data.is_list:
        content = helper.path__filter_hidden_path(content)
    else:
        template_render_data.title = re.sub(r'\.md$|\.txt$|^.+\/', '', path)
        content_markdown_string = base64.b64decode(content['content']).decode('utf-8')
        content['original_content'] = content_markdown_string
        # 处理 markdown 中的图片
        def process_image_url(matched):
            image_markdown_str = str(matched.group('value'))
            image_file_path = re.sub(r'\!\[\]\(|\)|\!\[Image\]\(', '', image_markdown_str)
            image_file_uri = helper.path__raw_path(template_render_data.parent_path, image_file_path)
            return '![](' + image_file_uri + ')'
        content_markdown_string = re.sub('(?P<value>\!\[\]\(.+\)|\!\[Image\]\(.+\))', process_image_url, content_markdown_string)
        # 解析 markdown 为 html
        content['content'] = mistune.markdown(content_markdown_string)
        # get lastest commit information
        content['commit_info'] = api.get_commit_info_for_path(path).json()[0]
    
    return render_template('index.html', content=content, template_render_data=template_render_data)

@app.route('/demo')
def demo():
    return render_template('index.html', content='hello,world', type=type, list=list, statistics_code=statistics_code)

if __name__ == '__main__':
    app.run(debug=True)