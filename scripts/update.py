#!/usr/local/bin/python

from src.ingestions import update_games, update_teams

if __name__ == "__main__":
    update_teams()
    update_games()