# steam_deck_boot
| **Service** |                                                                                                            **Main**                                                                                                            |                                                                                                       **Dev**                                                                                                      |
|:-----------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|      CI     | [![pytest](https://github.com/JuanGomez12/steam_deck_boot/actions/workflows/pytest.yml/badge.svg)](https://github.com/JuanGomez12/steam_deck_boot/actions/workflows/pytest.yml) |[![pytest](https://github.com/JuanGomez12/steam_deck_boot/actions/workflows/pytest.yml/badge.svg?branch=dev)](https://github.com/JuanGomez12/steam_deck_boot/actions/workflows/pytest.yml) |
<!-- |             |                                                                                                                                                                                                                                |                                                                                                                                                                                                                    |
|             |                                                                                                                                                                                                                                |                                                                                                                                                                                                                    | -->

# Instructions

## Create folder for steam deck movies
Open a terminal and run:
```
mkdir -p ~/.steam/root/config/uioverrides/movies/
```
This will create the necessary directories that need to exist
## Copy the script to the directory
You can either copy the animation_randomizer.py script to the ~/.steam/root/config/uioverrides directory, or open the directory and run:
```
cd ~/.steam/root/config/uioverrides && git clone --no-checkout https://github.com/JuanGomez12/steam_deck_boot tmp && mv tmp/.git . && rmdir tmp && git checkout main
```
What this one liner does is clone this repository to a temporary directory, move it to the current directory and then remove the temporary directory (workaround as git clone can't be run in a non-empty directory)
## Create cron job
From a terminal open crontab:
```
crontab -e
```
And add the following line:
```
@reboot  python ~/.steam/root/config/uioverrides/animation_randomizer.py
```

## Add movies/animations
Add the animations to the ~/.steam/root/config/uioverrides/movies/ folder. Make sure that the animations' name ends with "startup" so that they can be recognized by the script!
## ...?

## Profit!
