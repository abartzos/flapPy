import Flappy as flp
import random

# this model makes the bird jump randomly

game = flp.Game()
while not game.hit():
    game.frame()
    if random.choice([0,0,0,0,1]):
        game.jump()

print(game.score())
