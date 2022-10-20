import logging
import random
import shutil
import sys
from pathlib import Path

logging.basicConfig()


class AnimationRandomizer:
    """Animation Randomizer class.

    Attributes:
        animations_path: Path to the deck_startup animations directory.
        startup_animation_path: Path to the deck_startup.webm file.
    """

    def __init__(self, animations_path: Path) -> None:
        """Initializes the animationRandomizer class

        Args:
            animations_path (Path): Path to the animations directory.

        Raises:
            TypeError: If animations_path is not of type pathlib Path.
            FileNotFoundError: If the animations_path directory does not exist.
        """
        if not isinstance(animations_path, Path):
            raise TypeError(f"Expected Path type, received {type(animations_path)}")
        if not animations_path.is_dir():
            logging.error(
                f"Could not find the {animations_path} directory in {animations_path.resolve().parents[2]}"
            )
            raise FileNotFoundError(
                f"{animations_path.resolve()} is not a directory/does not exist"
            )
        self.animations_path = animations_path
        self.startup_animation_path = animations_path / "deck_startup.webm"

    def __repr__(self) -> str:
        return f"Animation Randomizer with path to: {self.animations_path}"

    def rename_boot_animation(
        self, startup_animation_new: Path, copy_file: bool = False
    ):
        """Copies or creates a hardlink for deck_startup.webm pointing to
        startup_animation_new, depending of the value of copy_file.
        If the Python version is lower than 3.10, defaults to copying the file.

        Args:
            startup_animation_new (Path): Path to the startup animation to copy/hardlink
                to.
            copy_file (bool, optional): If True, copies the file instead of
                creating a hard link. Defaults to False.
        """
        logging.info(f"Using {startup_animation_new} as new startup animation")
        if copy_file or sys.version_info < (3, 10):
            shutil.copyfile(
                str(startup_animation_new), str(self.startup_animation_path)
            )
        else:
            self.startup_animation_path.hardlink_to(startup_animation_new)

    def randomize_boot_animation(self) -> int:
        """Randomly selects a new boot animation from the available animations in the
        directory that end in deck_startup.webm

        Raises:
            FileNotFoundError: If the animations directory does not exist.
            FileNotFoundError: If no animations are found in the animations directory.

        Returns:
            int: 1 If it succesfully changes the startup animation, -1 if it doesn't.
        """
        succesful_run = -1
        if self.animations_path.is_dir():
            boot_animations = sorted(
                list(self.animations_path.glob("*deck_startup.webm"))
                + list(self.animations_path.glob("*deck_startup.WEBM"))
            )
            if boot_animations:
                startup_animation_new = boot_animations[
                    random.randint(0, len(boot_animations) - 1)
                ]
                # Rename new animation to deck_startup.webm
                self.rename_boot_animation(
                    self.startup_animation_path,
                    startup_animation_new,
                )
                succesful_run = 1
            else:
                logging.warning(f"Could not find animations in {self.animations_path}")
                raise FileNotFoundError(
                    f"No animations were found in {self.animations_path}"
                )

        else:
            logging.warning(
                f"Could not find the {self.animations_path} directory in {self.animations_path.resolve().parents[2]}"
            )
            raise FileNotFoundError(f"No directory exists in {self.animations_path}")
        return succesful_run


if __name__ == "__main__":
    animation_randomizer = AnimationRandomizer(Path("uioverrides") / "animations")
    animation_randomizer.randomize_boot_animation()
