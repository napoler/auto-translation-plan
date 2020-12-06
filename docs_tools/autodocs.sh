#! /usr/bin/bash

# 自动构建脚本
#sudo apt-get install hugo -y


#进行编译
hugo
# hugo server #运行本地
#hugo server --bind=0.0.0.0 --baseURL=192.168.192.173 -w
#建立软链接
#ln -s ./public/ ../docs

cp ./.nojekyll ../docs

# 推送命令
cd ../
git add .
git commit -m "auto更新文档"
git pull
git push
