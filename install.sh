#!/bin/bash

# args: -p provider -t token
# 初始化变量
provider="ollama"
token="ollama"

usage() {
    echo "Usage:  [-p provider] [-t token] -h"
    echo "  -p provider: llm provider name, ollama/chatglm/deepseek"
    echo "  -t token: api_key, you need an api_key to access the provider"
    echo "  -h help"
    exit 0
}

# 解析参数
while getopts "p:t:h" opt; do
    case $opt in
        p) provider="$OPTARG"
           ;;
        t) token="$OPTARG"
           ;;
        h) usage
           ;;
        ?) usage
           ;;
    esac
done

cd ~

echo "Download auto-commit..."
git clone https://github.com/djs66256/auto-commit.git

if pip3 install -q --upgrade pip; then
    echo "Pip3 is installed."
else
    echo "Pip3 is not installed."
    exit 1
fi

if python3 -m pip install --upgrade pip; then
    echo "Python3 is installed."
else
    echo "Python3 is not installed."
    exit 1
fi

echo "Install requirements..."
cd auto-commit
pip3 install --upgrade -r requirements.txt

echo "Setup config..."
echo "settings:\n  provider: ${provider}\n  api_key: ${provider}\n" > ~/.auto-commit/config.yaml

echo "Setup alias..."
# if bashrc exists, install to bashrc, otherwise install to bash_profile
if [ -f ~/.bashrc ]; then
    bashrc_path=~/.bashrc
else
    echo "bashrc does not exist."
    if [ -f ~/.bash_profile ]; then
        echo "bash_profile exists."
        bashrc_path=~/.bash_profile
    else
        echo "bash_profile does not exist."
        exit 1
    fi
fi

echo "alias gca='python3 ~/auto-commit/commit.py -a'" >> $bashrc_path

source $bashrc_path

echo "DONE!"