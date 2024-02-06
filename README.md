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

This project can be split into two different sub-projects. One is creating optimal training paths, and one is the rune detector. 

### Optimal Training Path

First, we need to identify how to get a live feed of the map in Maplestory. We can solve this by using DXCam, allowing us to view gameplay at 60 frames/sec. If we set this camera around the bounds of the map, we can isolate the map and find our player, indicated by the yellow circle.

![image](https://github.com/terryhji/mapleml/assets/139197235/904b31cd-cfa1-493d-a9b3-7a16c255ce89)

We can now constantly track where the player is on the map by implementing OpenCV template matching.

So now, how can we create an optimal training path for our character? We can do this by finding an algorithm that will help us imitate human training movements. That's where the Travelling Salesman Problem comes in.

![image](https://github.com/terryhji/mapleml/assets/139197235/36fecb94-6c3c-4942-9b02-4bca3567631f)

The Travelling Salesman Problem is an algorithm that creates a path that connects each node to the closest node around it, visiting each node once. Like a travelling salesman, the nodes will connect with each other until all nodes have been visited once, revealing a path that is effective when wanting to visit everything. The TSP algorithm is used in our case as it closely imitates how a player will usually play: killing monsters closest to them, going around the map in a rotating pattern.

We can implement the TSP algorithm in our program by having our player create nodes on the map, showing a live feed of an optimal training path while nodes are being placed.

![maplecv tsp](https://github.com/terryhji/mapleml/assets/139197235/962f8785-05ec-4a75-a335-c4fdc5cb1ae0)

To closely imitate player gameplay, each white node is surrounded by a larger white bound that will provide leeway for the bot's movement. These bounds are pivotal in having more fluid player movements and less bot-like. Once the bot has reached within the bounds, the player will then move to the next node's bounds, and so on. 

The main issue with this approach in automating gameplay is that the bot will seem somewhat robotic due to having to confirm that the character is stopped within the bounds, where it can then perform its next action. If the character is not stopped within each bounds, key strokes can be queued into the program, resulting in movement in the wrong direction. To solve this, another option was created to offer faster training, in the form of rotating around the map. Rotating around the map would mean that the margin of error can be large as long as the bot is going in the specific rotation direction.

This approach can be implemented by having the player provide bounds through a trackbar to where the bot will go up or down on the map, rotating clockwise.

![maplecv rotation](https://github.com/terryhji/mapleml/assets/139197235/460c805b-f852-412e-b55a-9ad37c0a775c)

The following left bounds (blue) will be the point where the bot will go upwards and the right (orange) is when the bot will go down. The top two lines in light blue are the points where the bot will proceed to go from left to right to the other once reaching this bound. As for the bottom, the bot will proceed to go to from right to left after performing downward movement key strokes. 

For both training paths, movement is performed using ctypes virtual keys and hex key codes.

### Rune Detector

To visually represent the changes made to the rune feed, an example image will be used:

![image](https://github.com/terryhji/mapleml/assets/139197235/93a9b6ef-6cf8-44f1-8a12-6697f55abe1a)

First, we need to remove as much noise and obstructions possible. We can first apply HSV colour range thresholding. The optimal range was discovered using a trackbar and testing. The upper and lower boundaries are as followed: (95, 0, 0) and (130, 255, 220).

![image](https://github.com/terryhji/mapleml/assets/139197235/072a1d98-e2a0-4d39-bfde-7d17cebd3abe)

Next, we can apply gaussian blur to help remove small artifacts and smooth out our edges.

![image](https://github.com/terryhji/mapleml/assets/139197235/0e27c0ed-b714-4c4a-a515-a190798d0c1d)

After gaussian blur has been applied, we can use canny edge detection.

![image](https://github.com/terryhji/mapleml/assets/139197235/71db2ee2-7937-43a2-87fe-88a45d7b116b)

As shown, the elipse that contains the runes have a distinct shape to them that is consistent regardless of resolution or map.

To isolate the runes, we can use contour approximation method to find boundary points that encompass an area similar to the area of the runes. By filtering these boundary points and cropping the image, we will be presented with the below image.

![image](https://github.com/terryhji/mapleml/assets/139197235/2fa01f61-5424-4dcb-9b15-8d926e52eca1)

Now, to detect each arrow, we can use the same process as before by finding the contour area to isolate each arrow.

![image](https://github.com/terryhji/mapleml/assets/139197235/a3fe9ff2-42f8-4842-b282-c9aed3095bde)

![image](https://github.com/terryhji/mapleml/assets/139197235/1b817755-5a22-4c0a-ad1c-27652172c579)

![image](https://github.com/terryhji/mapleml/assets/139197235/b2cd9f70-f48f-4f18-b64a-30f274c1b791)

Each arrow is isolated then simplified using polygonal curve approximation using the Douglas-Peucker algorithm. A representation of the coordinates each edge is shown below.

![image](https://github.com/terryhji/mapleml/assets/139197235/71fba417-5ae9-48b5-82d7-d74c54e8b8b4)

The direction of each arrow is determined by the two largest lines of the arrow.

## Improvements

### Machine Learning

A more flexible approach that can solve runes with obstructions behind the runes such as [Rune Breaker](https://github.com/gbrlfaria/rune-breaker?tab=readme-ov-file#what-are-runes) by gbrlfaria would be more effective than MapleCV's static approach. Below is an example of such obstructions.

![image](https://github.com/terryhji/mapleml/assets/139197235/cec3f0ad-7f42-4531-85f2-a9f73640d8db)

### Character Skills

With the goal of true autonomy, being able to detect when a skill is off cooldown and using it would be fundamental for effective training. This can be done by having users input each skill and the relative cooldown for each and using it whenever ready.

### Monster Detection

To train more efficiently, characters with multi targeting abilities tend to go towards packs of monsters to save both time and energy (known in the game as mana points). Either a model can be trained to detect these monsters or OpenCV template matching. It would more likely be better to use template matching due to the sheer amount of different monsters in the game.

## Built With

- [OpenCV](https://opencv.org/)
- [DXCam](https://github.com/ra1nty/DXcam)

## License

Usage is provided under the [MIT License](https://opensource.org/license/mit/). See LICENSE for the full details.
