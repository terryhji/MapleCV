# MapleCV
This project aims to bypass Maplestory's anti-botting mechanisms and provide efficient training routes. Through this, a bot that can automate gameplay was created.

The project provides a general overview that emcompasses what the project aims to solve and how it was implemented.

## Introduction
### What is Maplestory?

Maplestory is a massively multiplayer online role-playing game published by Nexon, available in various servers around the world. The objective of the game is to finish quests and level up by killing monsters to train.

### What are runes?

To prevent bot activity, Maplestory implements a unique twist on training. Much like a [CAPTCHA](https://en.wikipedia.org/wiki/CAPTCHA), the game will spawn a rune somewhere on the player's map that will give the player a buff if solved. The player can unlock the rune by pressing the activation button over it, showing a randomly generated combination of 4 arrows.

![image](https://github.com/terryhji/mapleml/assets/139197235/39403113-fc22-451a-b428-e6d5cbd915fe)

To deter bot gameplay, runes, if not activated within a certain period of time, will remove all rewards earned from hunting monsters. 

### What is the challenge with training?

Leveling up in Maplestory is a very tedious and long task that many people do not have enough time to do. Certain quests and events are locked behind a minimum level requirement, gatekeeping newer players from enjoying the bulk of what makes Maplestory fun: late-game boss fights.

### How can this be solved?

By providing an efficient bot that mimics player gameplay, we can effectively eliminate the minimum level barrier. 

First, the program should be able to offer a way to identify map bounds and create optimal training paths. Then, it should be able to detect the solution to the rune for the full automated experience.

## Process

This project can be split into two different sub-projects. One is creating optimal training paths, and one is the rune solver. 

### Optimal Training Path

First, we need to identify how to get a live feed of the map in Maplestory. We can solve this by using DXCam, allowing us to view gameplay at 60 frames/sec. If we set this camera around the bounds of the map, we can isolate the map and find our player, indicated by the yellow circle.

![image](https://github.com/terryhji/mapleml/assets/139197235/904b31cd-cfa1-493d-a9b3-7a16c255ce89)

We can now constantly track where the player is on the map by implementing OpenCV template matching.

So now, how can we create an optimal training path for our character? We can do this by finding an algorithm that will help us imitate human training movements. That's where the Travelling Salesman Problem comes in.

![image](https://github.com/terryhji/mapleml/assets/139197235/36fecb94-6c3c-4942-9b02-4bca3567631f)

The Travelling Salesman Problem is an algorithm that creates a path that connects each node to the closest node around it, visiting each node once. Like a travelling salesman, the nodes will connect with each other until all nodes have been visited once, revealing a path that is effective when wanting to visit everything. The TSP algorithm is used in our case as it closely imitates how a player will usually play: killing monsters closest to them, going around the map in a rotating pattern.

We can implement the TSP algorithm in our program by having our player create nodes on the map, showing a live feed of an optimal training path while nodes are being placed.



To closely imitate player gameplay, each node is surrounded by a larger bound that will provide leeway for the bot's movement. These bounds are pivotal in having more fluid player movements and less bot-like. Once the bot has reached within the bounds, the player will then move to the next node's bounds, and so on. 

The main issue with this approach in automating gameplay is that the bot will seem somewhat robotic due to having to confirm that the character is stopped within the bounds, where it can then perform its next action. If the character is not stopped within each bounds, key strokes can be queued into the program, resulting in movement in the wrong direction. To solve this, another option was created to offer faster training, in the form of rotating around the map.

This approach can be implemented by having the player provide bounds to where the bot will go up or down on the map, rotating clockwise.


It does this by offering two different options, whether to train in a rotation or by setting nodes and finding the most optimal path around the map.
