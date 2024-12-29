#!/bin/bash

# args: -p provider -t token
# 初始化变量
provider="ollama"
token="ollama"
add_alias=false

usage() {
    echo "Usage:  [-p provider] [-t token] -s -h"
    echo "  -p provider: llm provider name, ollama/chatglm/deepseek"
    echo "  -t token: api_key, you need an api_key to access the provider"
    echo "  -s add alias gca to bashrc"
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
        s) add_alias=true
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
echo "settings:\n  provider: ${provider}\n\n${provider}:\n  api_key: ${token}\n" > ~/.auto-commit/config.yaml

if [ $add_alias == true ]; then
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
else
    echo 'You can add alias to bashrc:\n  echo "alias gca='python3 ~/auto-commit/commit.py -a'" >> ~.bashrc\n  source ~/.bashrc'
fi

echo "DONE!"