# RLBotPythonExample
Example of a python bot using the RLBot framework, and customized for use
in a classroom setting.

## Getting Started

These instructions assume that you're attending some kind of session where
somebody is explaining RLBot and hosting the game on one main computer.

1. Make sure you have python 3.6 or higher installed.
1. Download this specific branch of the repository: https://github.com/RLBot/RLBotPythonExample/zipball/puppy. Make sure you unzip if necessary.
1. Look in the rlbot.cfg file and make sure the `network_address`
matches what the person hosting has provided.
1. Look in the src/bot.cfg file and change the name "AnonymousBot" to something
you can recognize, so you'll know which car on the screen is yours.
1. Run the program. This should cause a car to appear in the game on the host computer!
   - Windows: Double click on run.bat
   - Mac / Linux: Open a terminal at this folder location and run `python3 run.py`
1. It didn't work yet, but now you've got all the stuff downloaded via the fast wifi connection. Now kill the script and switch to the slower connection:
1. Connect to the wireless network called RLBot. The person hosting can tell you the password.
1. Open the src/bot.py file in your favorite code editor and start tinkering.
The behavior of the car should change immediately every time you save.

## Advanced 

- Read about the data available at https://github.com/RLBot/RLBotPythonExample/wiki/Input-and-Output-Data
- Find useful constants at https://github.com/RLBot/RLBot/wiki/Useful-Game-Values
- Make your car beautiful with `src/appearance.cfg` and https://github.com/RLBot/RLBot/wiki/Bot-Customization
