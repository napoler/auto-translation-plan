#! /usr/bin/bash

# 自动清理生成内容
#sudo apt-get install hugo -y
rm -rf ../docs/*
rm -rf content/post/*
# mkdir content/post/
python autoCreate.py

#进行编译
hugo server

#hugo server --bind=0.0.0.0 --baseURL=192.168.192.173 -w
#建立软链接
#ln -s ./public/ ../docs

cp ./.nojekyll ../docs
hugo server && xdg-open http://localhost:1313/ #运行本地
# 推送命令
# cd ../
# git add .
# git commit -m "auto更新文档"
# git pull
# git push
