# 1A2B Game

A Line bot based on a finite state machine
Let you play 1A2B

## Deploy
deploy on AWS EC2

## Finite State Machine Diagram
![show-fsm](./img/show-fsm.png)

## How to play (Usage)
* Type in **"play 1A2B"** to start the game.
* Type in **"$a_1a_2a_3a_4$"** to guess the number. Ex. "5267"
* Type in **"replay"** to start a new game.
* Type in **"quit"** to rage quit.
* Click **yes** or **no** after winning the game to continue or exit.

### Rule
The number range is [0~3], number may appear more than once.
We'll give you hint in the form of XAYB, "B" means the number is matched but not in the right position, while "A" means it's in the right position.
For example, answer is 8123 and player guess 1052, then the hint will be 0A2B. Note that if answer is 5543, and player guess 5255, the hint will be 1A1B.

## States
- **user**
	Initial state
- **play_1A2B**
	Ready to play 1A2B.
	In this state, we'll randomly select next node.
- **state_1A2B_winning**
	Winning the game.
	In this state, player can choose to play again or not.
- **state_1A2B_$a_1a_2a_3a_4$**
	Dynamically generated states. $a_1a_2a_3a_4$ represents answer.
	This state is randomly selected by **play_1A2B**.
- **state_1A2B_$a_1a_2a_3a_4$correct**
	Dynamicall generated states.
	Entered after player guessed the answer.
- **state_1A2B_$a_1a_2a_3a_4$wrong**
	Dynamicall generated states.
	Entered after player *didn't* guessed the answer.

## About Program

### Dynamic generate states
In Gen1A2B.py file, these's a variable called ***Game1A2B_N*** which controlls the number range of our 1A2B game. In deploy version, it's set to 4, but it have no problem going up to 10.
The state count in this program can be calculated by $Game1A2B\_N^4*3+3$. A number of 4 yields 771 states, a number of 10 yields 30003 states.

### Multiple users
Different user has independent datas, states.