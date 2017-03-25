# Chomp AI

Author: Lei Mao

Date: 3/25/2017

## Project Description

[Chomp](https://en.wikipedia.org/wiki/Chomp) is a two-player strategy game played on a rectangular chocolate bar made up of smaller square blocks (cells). 
The players take it in turns to choose one block and "eat it" (remove from the board), together with those that are below it and to its right. 
The top left block is "poisoned" and the player who eats this loses.

Chomp is actually a classic discrete mathematics problem. The player goes first was proved that it always have winning strategy, although the winning strategy might not be easily explicitly specified.

The purpose of the project is to develop a potent AI that can give explicit winning strategy during the game.


## Run the Game

The Chomp was developed using Python and PyGame. The player needs to install Python 2.7, Numpy and PyGame in order to run the game.

To run the Chomp, run the command "python chomp_gui.py x m n" in termimal. 

'x' designates who goes first in the game. It can be either 'Human' or 'AI'. 

'm' and 'n' are the width and height of the rectangle. 'm' and 'n' are the positive integers no larger than AI_limit.

In this version, the AI_limit is 8.

## About AI

The data for winning strategy was actually pre-calculated and saved in file. The AI will use the data to design winning strategy during the game.

The AI is extremely potent that it is guaranteed to win if it goes first.

It also has extremely high winning rate (nearly 100%) against human players (mostly my friends) if human players goes first, because human players will likely make mistake during the game.

Once the human player makes a mistake even if the human player goes first, the AI guarantees to win.

The AI has its limit. Because it relies on the pre-calculated data, and the data was calculated for the board size no larger than AI_limit x AI_limit.

