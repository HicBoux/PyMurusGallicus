# PyMurusGallicus

A python/pygame application to play the board game Murus Gallicus between 2 players or against a minimax AI.
Murus Gallicus is a mancala board game invented in 2009 by the American Phil Leduc.


<h2>How to play Murus Gallicus ? What are the rules of the game ?</h2>

The rules are explained simply in a few words here : [Mancala World Fandom Wiki](https://mancala.fandom.com/wiki/Murus_Gallicus).<br/>
PyMurusGallicus is based on the original rules without variants.

<h2>What can do you with PyMurusGallicus ?</h2>

You can :
<ul>
  <li>Play against another player</li>
  <li>Play against a Minimax based AI</li>
  <li>Try to improve the heuristic of the Minimax based AI in the "evaluate()" function of board.py</li>
  <li>Try to add new features or new AI algorithms</li>
</ul>

<h2>How to launch PyMurusGallicus ?</h2>

<h3>Requirements :</h3>
-Python 3.6 or possibly more <br/>
-The following Python library : Pygame 2.0.1 <br/>

<h3>Install and play :</h3>
Open a shell terminal in the root directory of the app where the Makefile is built.
Then feel free to execute one of the following commands :

<h4>Install</h4>
To install the game before to be able to run it : <code> make install </code>

<h4>Run</h4>
To launch the game and play against another player or an AI in the graphical window : <code> make run </code>

<h4>Test</h4>
To test the code through the unit tests : <code> make test </code>

<h4>Clean</h4>
To clean the files and virtual environment created by the PyMurusGallicus app when installed or runned : <code> make clean </code>

<h4>All : Install + Test + Run</h4>
To install the app, execute the unit tests and then run the game : <code> make all</code> or simply <code> make </code>

<h2>References</h2>

-[The Noun Project (Trevor Dsouza's icon)](https://thenounproject.com/term/checkers/1684698/) : source of the PyMurusGallicus app icon <br/>
-[Board Game Geek : Murus Gallicus](https://boardgamegeek.com/boardgame/55131/murus-gallicus)<br/>
-[Mancala World Fandom Wiki](https://mancala.fandom.com/wiki/Murus_Gallicus)<br/>
-[Tech With Tim's Youtube Channel](https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg)

<h2>Credits</h2>

Copyright (c) 2021, HicBoux. Work released under MIT License.

(Please contact me if you wish to use my work in specific conditions not allowed automatically by the MIT License.)
