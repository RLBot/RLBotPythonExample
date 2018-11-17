# DisasterBot

ExampleBot documentation here: https://github.com/RLBot/RLBotPythonExample/blob/master/README.md

## Guidelines
_The guidelines are WIP._

### Contribution guidelines

* Everyone who is not a collaborator should make a pull request for their changes.
* Documentation can be changed on the master branch.
* All other files should never be modified on the master branch in order to keep the bot stable.
* After testing changes and approval from the other collaborators a branch can be merged into master.


### Teamwork guidelines

* Don't work on someone else's code without permission, or it might not be merged.
* Issues can be worked on by everyone, but don't doublecommit.


### Programming guidelines

* The bot should be completely modular e.g. every state, controller, planner should have it's own file and use inheritance.
* Python code should be according to PEP 8.



## Working plan

* Build different states that do a specific thing.
* Build a testing environment (using state setting) to test these states.
* When we are happy with a state it can be used by the state machine.
* Build a state machine or planning algorithm (this part of the plan needs work).


### Project structure

* One configuration file to run the bot.
* One "states" folder that contains the states. (a single state should not require more than one file)
* One "planner" folder that contains the algorithm that choses between the states
* One "utils" folder that contains tools used by the bot in action.
* One "test" folder that contains:
  * One configuration file to test the bot (this will have a selector for the state).
  * One "utils" folder that contains tools used by the bot while testing.



## Defenition of concepts

### States
States are the lowest level of actions that the planning algorithm can chose from.
Examples are:
* Drive to own goal
* Shoot ball toward opponent goal
* Dribble ball away from the opponent
* Pass ball to teammate
These states should have no parameters.
States should not contain too much strategy (when in doubt ask).

### Controller
This is a class that takes some arguments and creates a controller_state.
Controllers should have no strategy at all.
RLBotUtils are in this category.

### State machine/ planning algorithm
This is the part of the bot that contains most of the strategy.
The exact algorithm used is to be discussed.
