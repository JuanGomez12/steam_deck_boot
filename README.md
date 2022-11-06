# Steam Deck boot movie/animation randomizer
| **Service** |                                                                                                            **Main**                                                                                                            |                                                                                                       **Dev**                                                                                                      |
|:-----------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|      CI     | [![Python test (pytest)](https://github.com/JuanGomez12/steam_deck_boot/actions/workflows/python-test.yml/badge.svg?branch=main&event=push)](https://github.com/JuanGomez12/steam_deck_boot/actions/workflows/python-test.yml) |[![Python test (pytest)](https://github.com/JuanGomez12/steam_deck_boot/actions/workflows/python-test.yml/badge.svg?branch=dev&event=push)](https://github.com/JuanGomez12/steam_deck_boot/actions/workflows/python-test.yml) |
<!-- |             |                                                                                                                                                                                                                                |                                                                                                                                                                                                                    |
|             |                                                                                                                                                                                                                                |                                                                                                                                                                                                                    | -->

As the name implies, the idea is to create a randomizer for the boot animations.
# Instructions
- Back up anything important in the ~/.steam/root/config/uioverrides/movies/ path if you have already set up movies there, just in case something doesn't work correctly!
- The scripts assume that you are running the default user for the steam deck, as it comes in the box.
- When I tried copying the timer and service files, I needed to have elevated permissions. This means that I needed the root password, which wasn't setup and thus I couldn't continue until I had one set up.
    - *TLDR:* make sure that you have set up a password for your steam deck.
    - This can be done by opening a terminal and running passwd, or in Desktop mode going to settings > users and setting your password there.

## Manual Install
### Create folder for steam deck movies
Open a terminal and run:
```
mkdir -p ~/.steam/root/config/uioverrides/movies/
```
This will create the necessary directories that need to exist for us to move the scripts plus the directory on which to store the movies/animations.

### Copy the script to the directory
You can either copy the animation_randomizer.py script to the ~/.steam/root/config/uioverrides directory, or run:
```
curl https://raw.githubusercontent.com/JuanGomez12/steam_deck_boot/main/animation_randomizer.py -o ~/.steam/root/config/uioverrides/animation_randomizer.py
```

### Copy the timers
The timer and its service need to be copied into the /etc/systemd/system folder, so we need to do:
```
sudo cp /tmp/steam_deck_boot/timer/movie_randomizer.* /etc/systemd/system/
```

## Automatic installation
You should never run bash scripts from the internet blindly! However, I'll still offer an auto install that can be used by opening a terminal and typing:
```
curl https://raw.githubusercontent.com/JuanGomez12/steam_deck_boot/main/install_script | bash
```
This install script, found [here](install_script), runs the following commands which you can copy and paste in case you don't want to run a random file from the internet:
```
# Create Steam movies/animations folder
mkdir -p ~/.steam/root/config/uioverrides/movies/

# Delete steam_deck_boot folder if it exists in the tmp directory
rm -rf /tmp/steam_deck_boot

# Clone the repo
git clone https://github.com/JuanGomez12/steam_deck_boot /tmp/steam_deck_boot

# Copy the randomizer to the uioverrides directory
cp /tmp/steam_deck_boot/animation_randomizer.py ~/.steam/root/config/uioverrides/

# Test to see if the script runs correctly
python3 ~/.steam/root/config/uioverrides/animation_randomizer.py

# Copy the timer and service
sudo cp /tmp/steam_deck_boot/timer/movie_randomizer.* /etc/systemd/system/

# Enable the timer
systemctl enable movie_randomizer.timer
```
This will then setup everything so that the movie randomizer runs every time you turn on/reboot your steam deck.

## Add movies/animations
Add the animations to the ~/.steam/root/config/uioverrides/movies/ folder. Make sure that the animations' name ends with "startup" so that they can be recognized by the script!
## ...?

## Profit!
If you get any errors with any of the scripts, please let me know and I'll try to solve them as soon as I can. Hope it's useful for you!