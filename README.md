# DisasterBot

ExampleBot documentation here: https://github.com/RLBot/RLBotPythonExample/blob/master/README.md

RLBot discord here: https://discord.gg/2prRFJ7

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
* Use the issues feature in github as a todo list (and for issues).
* Discuss decisions on discord via dm, or when everybody should be involved in the RLBot server (please use the correct channel, #strategy-discussion for strategy discussion etc.).
* Use a pull-request to ask others for feedback on your work (feedback can be given on github).


### Programming guidelines

* The bot should be completely modular e.g. every state, controller, planner should have it's own file and use inheritance.
* Python code should be according to PEP 8.



## Working plan

* Build different actions that do a specific thing.
* Build a testing environment (using state setting) to test these actions.
* When we are happy with an action it can be used by the policy.
* Build a policy (this part of the plan needs work).


### Project structure

* One configuration file to run the bot.
* One "actions" folder that contains the actions. (a single action should not require more than one file)
* One "policy" folder that contains the algorithm that choses between the states
* One "utils" folder that contains tools used by the bot in action.
* One "test" folder that contains:
  * One configuration file to test the bot (this will have a selector for the action and environment).
  * One "environements" folder that contains testing environments
  * One "utils" folder that contains tools used by the bot while testing.



## Defenition of concepts

### Actions
Actions are what the policy can chose from.
Examples are:
* Drive to own goal
* Shoot ball toward opponent goal
* Dribble ball away from the opponent
* Pass ball to teammate
These actions should have no parameters.
Actions should not contain too much strategy (when in doubt ask).

### Controller
This is a class that takes some arguments and creates a controller_state.
Controllers should have no strategy at all.
RLBotUtils are in this category.

### Policy
This is the part of the bot that contains most of the strategy.
The exact algorithm used is to be discussed.
