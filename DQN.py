import torch
import random
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F

# Run NN on GPU, send any input vector TO THE GPU before RUNNING NN
# Look Concerns on README
# Heavily, Heavily inspired by another repo I made: https://github.com/Eshaancoding/DQN


def put_to_gpu_or_cpu (x):
    # set it to GPU if avaliable
    if torch.cuda.is_available():
        x = x.cuda()
    else:
        x = x.cpu()   
    return x

class ReplayMemory:
    mem = [[]]
    capacity = 0

    def __init__(self, capacity) -> None:
        self.capacity = capacity

    def store (self, current_state, action_speed, action_dir, reward, next_state, is_done):
        if len(self.mem) == self.capacity:
            self.mem.pop(0)
        
        append_mem = []
        append_mem.append(current_state)
        append_mem.append(action_speed)
        append_mem.append(action_dir)
        append_mem.append(reward)
        append_mem.append(next_state)
        append_mem.append(is_done)
        self.mem.append(append_mem)

class Agent:
    net = None
    optim = None
    target_net = None 
    reply_mem = None
    frameReachProb = 0
    batches = 0
    targetFreqUpdate = 0 
    output_size = 0
    loss_history = []
    frames = 0

    def __init__(self, output_size, lr, mem_capacity, frameReachProb, targetFreqUpdate, batches):
        # init var
        self.output_size = output_size # should include direction AND speed
        self.reply_mem = ReplayMemory(mem_capacity)
        self.frameReachProb = frameReachProb
        self.batches = batches
        self.targetFreqUpdate = targetFreqUpdate

        # init Neural network (experimental)
        self.net = nn.Sequential( 
            nn.Conv2d(3, 18, 3),
            nn.ReLU(),
            nn.Conv2d(18, 30, 2),
            nn.MaxPool2d(2, 1),
            nn.ReLU(),
            nn.Dropout(),
            nn.Flatten(),
            nn.Linear(300, 150), # IDK THIS INPUT VAL. CHECK IT OUT
            nn.Sigmoid(), 
            nn.Linear(150, self.output_size)
        )

        self.net = put_to_gpu_or_cpu(self.net)
    
        self.optim = optim.SGD(self.net.parameters(), lr=lr)

        # set target_net 
        self.target_net = self.net

    def get_action (self, input): 
        self.net.eval()
        input = put_to_gpu_or_cpu(input)
        self.frames+=1
        prob = 0.0
        if self.frames < self.frameReachProb: 
            prob = (-0.9 / self.frameReachProb) * self.frames + 1
        else:
            prob = 0.1
        is_random = (random.randint(0,100) < (prob * 100))
        if is_random:
            return torch.rand(self.output_size)
        else:
            return self.net(input)

    def train (self):

        self.net.train()

        for i in range(self.batches):
            rand_num = random.randint(0, len(self.mem) - 1)
            mem_read = self.mem[rand_num]
            current_state = put_to_gpu_or_cpu(mem_read[0])
            action_speed = mem_read[1] # must be 0 or 1
            action_dir = mem_read[2] # must 0 to num_of_direction - 1
            reward = mem_read[3]
            next_state = put_to_gpu_or_cpu(mem_read[4])
            is_done = mem_read[5] 

            # train
            y_dir = 0
            y_speed = 0
            target_net_predict = self.target_net(next_state)
            if is_done: 
                y_dir = reward
                y_speed = reward
            else: 
                y_dir = reward + (0.99 * torch.max(target_net_predict[:len(target_net_predict)-2]))
                y_speed = reward + (0.99 * torch.max(target_net_predict[len(target_net_predict)-2:]))
            
            preds = self.net(current_state)
            target = preds
            target[len(target)-2+action_speed] = y_speed
            target[action_dir] = y_dir

            self.optim.zero_grad()
            loss = F.mse_loss(preds, target)
            loss.backward()
            self.optim.step()
            self.loss_history.append(loss.data[0])

        if self.frames % self.targetFreqUpdate == 0:
            self.target_net = self.net