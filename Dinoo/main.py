import pygame
import sys
import random
from interfaces.gameplay import *
from interfaces.introscreen import *

def main():
        isGameQuit = introscreen()
        if not isGameQuit:
            from interfaces.gameplay import start_game_with_skin
            from config import skins, selected_skin
            start_game_with_skin(
                skins[selected_skin]["ingame"], skins[selected_skin]["ingame_ducking"])


if __name__ == "__main__":
    main()
