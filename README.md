# AI Slither

Using the DQN (Deep Q Network) to play slither.io 
Original DQN Paper: https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf
The libraries I used is in the requirements.txt

# How it works

- Then it will capture a screenshot of the window. You may need to adjust the screen capture dimensions so it fits the whole screen. I tried to make this automatic, but pywin32 won't work with me: https://stackoverflow.com/questions/67550294/dimensions-of-screenshot-doesnt-match-dimensions-of-resized-window-in-pywin32. If you don't want to adjust the screen dimensions, then set Scale & Layout under Display to 100%. This will set the DPI to 96, which is the default value of DPI awareness for pywin32.  

- Then DQN will find out the reward and if the game has finished using OCR (pytesseract). 

- DQN will train the network everytime the bot dies.

- Will start a new episode automatically.


# Notes

- 


# TODO List

- Finish requirements
- Setup all the libraries (including torch for CUDA, and also install CUDA)
- Create WebsiteInteraction class
- Implement DQN
- Create the main!
- Create a makefile for running the algorithm 


# How to run
