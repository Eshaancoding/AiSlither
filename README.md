# AI Slither (WORK IN PROGRESS!)

Using the DQN (Deep Q Network) to play slither.io.
Original DQN Paper: https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf.
The libraries I used is in the requirements.txt. You can simply type `pip3 install -r requirements.txt`. If you would like the training process to be run on your GPU (usually faster on the GPU than the CPU), then you need to install CUDA. Then the program will automatically switch from CPU to GPU. 


## How it works

- Open up a slither.io window. For accurate results, use Microsoft Edge and set the game to low quality (in the upper right of the menu). Click start afterwards. 

- Start the program using `make` in the folder's directory. Then it will capture a screenshot of the window. Be careful about choosing your custom window dimensions, because your browser can set a predefined dimension if the desired dimensions are too small.   

- The algorithm will then move the mouse in different directions, and it could also click the mouse to speed-up the player. 

- Then DQN will find out the reward and if the game has finished using OCR (pytesseract). 

- DQN will train the network everytime the bot dies.

- Will start a new episode automatically.


## Concerns
- Will DQN be able to train on multiple actions AT the same time. 
[x,x,x_target,x,x,x,x,x,x,y_target,y] 

## TODO List

- Implement DQN
- Create the main!
- Create a makefile for running the algorithm 

## How to run
