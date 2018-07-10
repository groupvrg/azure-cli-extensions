#!/bin/sh

curr=`pwd`
cd $(dirname $0)
pwd
az extension remove -n image-copy-extension
az extension list
python3 setup.py sdist bdist_wheel
az extension add -y --source dist/image_copy_extension-0.0.1-py2.py3-none-any.whl
az extension list
cd $curr