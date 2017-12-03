#!/usr/bin/python
# #coding:utf-8
import re
import os
import urllib.parse
import base64
from furl import furl
from config import config

def path_test():
    print('test func from path.py')
    return 'test'

def path__parent_path(current_path):
    parent_path = ''
    if re.search(r'\/', current_path):
        parent_path = re.sub(r'\/[^\/]+$', '', current_path)
    else:
        parent_path = ''
    return parent_path

def path__raw_path(current_path, file_relative_path):
    raw_branch_path = 'https://raw.githubusercontent.com'
    raw_path = furl(raw_branch_path)
    raw_path.path.segments = [config.owner, config.repo, config.branch, current_path, file_relative_path]
    return raw_path.url
    
def path__filter_hidden_path(path_array):
    result = []
    for item in path_array:
        if not re.match('^\_|^\.', item['name']):
            result.append(item)
    return result

def setup(target_class):
    target_class.set_instance_method(path_test)
    target_class.set_instance_method(path__parent_path)
    target_class.set_instance_method(path__raw_path)
    target_class.set_instance_method(path__filter_hidden_path)