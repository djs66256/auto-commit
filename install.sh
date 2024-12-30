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
    echo "  -s add alias 'gca=python commit.py -a' to bashrc"
    echo "  -h help"
    exit 0
}

# 解析参数
while getopts "p:t:sh" opt; do
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

if [ -d ~/auto-commit ]; then
    cd auto-commit
    git pull --rebase
    cd ..
else
    git clone https://github.com/djs66256/auto-commit.git
fi

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
if [ ! -d ~/.auto-commit ]; then
    mkdir ~/.auto-commit
fi

echo "settings:" > ~/.auto-commit/config.yml
echo "  provider: ${provider}" >> ~/.auto-commit/config.yml
echo "${provider}:" >> ~/.auto-commit/config.yml
echo "  api_key: ${token}" >> ~/.auto-commit/config.yml

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
    echo 'You can add alias to bashrc:'
    echo '  echo "alias gca='python3 ~/auto-commit/commit.py -a'" >> ~.bashrc'
    echo '  source ~/.bashrc'
fi

echo "DONE!"