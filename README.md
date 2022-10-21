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
This will create the necessary directories that are needed to store the animations/movies.
## Copy the script to the directory
You can either copy the animation_randomizer.py script to the ~/.steam/root/config/uioverrides directory, or open the directory and run:
```
cd ~/.steam/root/config/uioverrides && git clone --no-checkout https://github.com/JuanGomez12/steam_deck_boot tmp && mv tmp/.git . && rmdir tmp && git checkout main
```
What this one liner does is clone this repository to a temporary directory, move it to the current directory and then remove the temporary directory (workaround as git clone can't be run in a non-empty directory).

If you get an error saying that the directory is not empty, just delete the folder and start again from the first step.

## Create cron job
From a terminal open crontab using:
```
crontab -e
```
Select the text editor you want to use to update the file, in this Readme we'll assume we're using nano. If you need to isntall nano, just run in the terminal:
```
pacman -S nano
```
And add the following line:
```
@reboot  python ~/.steam/root/config/uioverrides/animation_randomizer.py
```
To close the editor, press ctrl + x, press y to save the changes and then press enter to save the crontab file.

## Add movies/animations
Add the animations to the ~/.steam/root/config/uioverrides/movies/ folder. Note: The script will only use the animations which have a name that ends with "startup", so make sure to name your files accordingly for the script to recognize them!
## ...?

## Profit!
