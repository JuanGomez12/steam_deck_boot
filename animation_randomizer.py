import logging
import random
import shutil
import sys
from pathlib import Path
from typing import Optional

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
            startup_animation_new (Path): Path to the startup animation to
                copy/hardlink to.
            copy_file (bool, optional): If True, copies the file instead of
                creating a hard link. Defaults to False.

        Raises:
            FileNotFoundError: If the new startup animation does not exist.
        """
        if not startup_animation_new.is_file():
            raise FileNotFoundError(f"Could not find animation {startup_animation_new}")
        logging.info(f"Using {startup_animation_new} as new startup animation")
        if copy_file or sys.version_info < (3, 10):
            shutil.copyfile(
                str(startup_animation_new), str(self.startup_animation_path)
            )
        else:
            if self.startup_animation_path.is_file():
                self.startup_animation_path.unlink()
            self.startup_animation_path.hardlink_to(startup_animation_new)

    def randomize_boot_animation(
        self, random_seed: Optional[int] = None
    ) -> Optional[Path]:
        """Pseudo randomly selects a new boot animation from the available
        animations in the directory that end in deck_startup.webm

        Args:
            random_seed (int, optional): Random seed to use for the random
            selection. Useful for reproducibility. Defaults to None.

        Raises:
            FileNotFoundError: If the animations directory does not exist.
            FileNotFoundError: If no animations are found in the animations directory.
        Returns:
            Path|None: Path to the animation selected, or None if the function
                couldn't run.
        """
        animation_used_path = None
        if self.animations_path.is_dir():
            boot_animations = sorted(
                list(self.animations_path.glob("*startup.webm"))
                + list(self.animations_path.glob("*startup.WEBM"))
            )
            logging.debug(f'Found {len(boot_animations)} animations')
            if self.startup_animation_path in boot_animations:
                boot_animations.remove(self.startup_animation_path)
            if boot_animations:
                if random_seed is not None:
                    random.seed(random_seed)
                startup_animation_new = boot_animations[
                    random.randint(0, len(boot_animations) - 1)
                ]
                logging.info(
                    f"{startup_animation_new} selected as the new boot animation"
                )
                # Rename new animation to deck_startup.webm
                self.rename_boot_animation(startup_animation_new)
                animation_used_path = startup_animation_new
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
        return animation_used_path


if __name__ == "__main__":
    animation_randomizer = AnimationRandomizer(Path(__file__).parent / "movies")
    animation_used_path = animation_randomizer.randomize_boot_animation()
    print(f"New animation set: {animation_used_path}")
