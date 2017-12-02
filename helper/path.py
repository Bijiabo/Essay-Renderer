import re

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
    
    

def setup(target_class):
    target_class.set_instance_method(path_test)
    target_class.set_instance_method(path__parent_path)