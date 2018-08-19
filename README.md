# Roguelike Python Game
# Descent Into Jotunheim

**Descent Into Joutnheim**, made by David Kohler, is designed for Python 3.6. Uses the libtcodpy library for ease of
making and running a roguelike game in Python. When game is run, it will create a GUI window and display the title screen
for the game. The game uses the keyboard and mouse to play. To see the rules and keybindings, the user can press 'c' while
on the title screen, or 'r' while in-game. From the title screen, if you have a savefile, you can press 'b' to load it,
otherwise press 'a' to start a new game. The game consists of 50 randomly generated dungeons with random enemies and random
loot. The game contains 62 unique items and 26 unique enemies. Specific items and monsters have certain spawn chances
depending on the current dungeon level, with better items and harder enemies appearing as the game progresses. For more
information, see the rules screen in-game. The game takes inspiration from Norse mythology with the names of items, monsters,
and even the theme.

## Installation

1. Copy the repository 
2. Make sure you have Python version 3.6 or later and Homebrew installed
3. Run:
`brew install mercurial`

`pip install tdl`

## Usage

`engine.py` actually runs the game

1. In terminal, usage: `engine.py`
2. Could also run `engine.py` from IDE

For rules of game, when game is run, press 'c' to go to the rules page

## Authors

David Kohler

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

### Acknowledgement

This project takes inspiration from the RogueBasin Roguelike tutorial

Visit [RogueBasin](http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python3%2Blibtcod,_setup_Mac) if
you need help setting up the environment for a Mac
