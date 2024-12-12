cd ~
if [ -d ~/auto-commit ]; then
    cd auto-commit
    echo "Update auto-commit..."
    git pull
    pip3 install --upgrade -r requirements.txt
    echo "DONE!"
    exit 0
else
    echo "auto-commit is not installed."
    exit 1
fi