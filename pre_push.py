#!/usr/bin/env python
import os
import shutil
from distutils.dir_util import copy_tree


def build_all():
    root_dir = os.path.dirname(os.path.realpath(__file__))
    repo_path = '/tmp/protolangs'
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
    
    root = os.getcwd()
    dirs = [os.path.join(root, dir) for dir in os.listdir('.') if os.path.isdir(dir)]
    for dir in dirs:
        os.chdir(dir)
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        if '.protolangs' in files:
            with open('.protolangs', 'r') as file:
                languages = [line.rstrip() for line in file]
                for language in languages:
                    cwd = os.getcwd()
                    repo_name = 'protobuf-%s-%s' % (os.path.basename(dir), language)
                    shutil.rmtree('%s/%s' % (repo_path, repo_name), ignore_errors=True)
                    os.system('git clone git@github.com:kekhuay/%s.git %s/%s' % (repo_name, repo_path, repo_name))
                    os.system('docker container run --rm --mount type=bind,source=`pwd`,target=/defs namely/protoc-all -d ./ -o pb-%s -l %s' % (language, language))
                    os.system('cp -R pb-%s/* %s/%s/' % (language, repo_path, repo_name))
                    os.chdir('%s/%s' % (repo_path, repo_name))
                    os.system('git add .')
                    os.system('git commit -m "Auto Creation of Proto"')
                    os.system('git push -u origin master')
                    os.chdir(dir)


if '__main__' == __name__:
    build_all()
