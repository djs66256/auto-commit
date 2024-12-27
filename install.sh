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