from torch.nn.common_types import T
from DQN import * 
from WebInteract import *
from math import cos, sin, pi, ceil

# PARAMETERS
output_size = 16 + 2 # 30 = number of different directions the slither could go, 2 = whether slither should speed or not
lr = 0.001
mem_capacity = 1000000
frameReachProb = 1000
batches = 32
targetFreqUpdate = 96 
width_of_win = 650
height_of_win = 650
left_of_win = 100
top_of_win = 100

agent = Agent(output_size, lr, mem_capacity, frameReachProb, targetFreqUpdate, batches)
interaction = WebInteract(width_of_win, height_of_win, left_of_win, top_of_win)
current_frame = interaction.capture()
# agent.open_model()

while (True):
    # get action from Agent
    prediction = agent.get_action(current_frame, testing=True)
    
    # direction
    action_dir = torch.argmax(prediction[:len(prediction)-2])
    dir_radians = (360 / (output_size - 2)) * action_dir * (pi / 180)
    mouse_x = (0.5 * width_of_win) + ((width_of_win / 5) * cos(dir_radians))
    mouse_y = (0.5 * height_of_win) + ((height_of_win / 5) * sin(dir_radians)) 
    interaction.mouseMove(mouse_x, mouse_y)

    # speed
    action_speed = torch.argmax(prediction[len(prediction)-2:])
    if action_speed.item[0] == 0: 
        interaction.mouseLeftUp()
    else:
        interaction.mouseLeftDown()

    # get another frame
    current_frame = interaction.capture()