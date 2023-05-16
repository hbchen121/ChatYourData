# Install

下载本项目
```shell
git clone git@github.com:hbchen121/ChatYourData.git
```

## 前端安装（Frontend Install）

```shell
cd client
```

安装nodejs
```shell
# Linux
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - 
sudo apt-get install -y nodejs

# MacOS
brew install nodejs
```

安装相关包，需要再client目录下
```shell
sudo npm install -g pnpm
sudo npm install vuex
sudo npm install vue-router
sudo npm install axios
```

```shell
sudo bash start
```

## 后端安装（Backend Install）

建议先安装conda/miniconda进行python包管理（参考[miniconda_install](miniconda_install.md))，同时创建Python3.9环境
```shell
conda create -n chatdata python==3.9

# activate
conda activate chatdata
```

```shell
cd serve

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

在`start`中修改自己的代理端口，比如我的端口是 8889，否则无法访问 OPENAI_API
```shell
export HTTP_PROXY=http://127.0.0.1:8889
export HTTP_PROXY=http://127.0.0.1:8889
```

启动脚本
```shell
bash sudo start
```

访问端口 `http://0.0.0.0:5173` 或 `http://127.0.0.1:5173` 即可进入

