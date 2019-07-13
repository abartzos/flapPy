import Flappy as flp
import random

# this model makes the bird jump randomly

flp.init()
while not flp.lost:
    flp.frame()
    if random.choice([0,1,0,0,0,0]):
        flp.jump()


print('Score: ', flp.score)
    