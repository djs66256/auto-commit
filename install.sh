cd ~

git clone https://github.com/djs66256/auto-commit.git

cd auto-commit
pip install -r requirements.txt

echo "alias gca='python3 ~/auto-commit/commit.sh -a'" >> ~/.bashrc

echo "DONE!"