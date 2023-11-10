sudo apt update
sudo apt upgrade
pip install --upgrade pip
git config --global --add safe.directory /workspaces/math-100-code
git config --global init.defaultBranch main
git config --global core.autocrlf false

sudo apt install libsnappy-dev
pip install nfl_data_py psycopg2 sqlalchemy
pip install -e .
