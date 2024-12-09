cd ~

git clone https://github.com/djs66256/auto-commit.git

cd auto-commit
pip3 install --upgrade -r requirements.txt

echo "alias gca='python3 ~/auto-commit/commit.sh -a'" >> ~/.bashrc
echo "alias gca='python3 ~/auto-commit/commit.sh -a'" >> ~/.bash_profile

echo "DONE!"