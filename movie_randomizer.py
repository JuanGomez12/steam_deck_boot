import logging
import random
import shutil
import sys
from pathlib import Path

logging.basicConfig()

MOVIES_PATH = Path("uioverrides") / "movies"
STARTUP_MOVIE_PATH = MOVIES_PATH / "deck_startup.webm"


class MovieRandomizer:
    def __init__(self, movies_path: Path) -> None:
        if not isinstance(movies_path, Path):
            raise TypeError(f"Expected Path type, received {type(movies_path)}")
        if not movies_path.is_dir():
            logging.error(
                f"Could not find the {movies_path} directory in {movies_path.resolve().parents[2]}"
            )
            raise FileNotFoundError(
                f"{movies_path.resolve()} is not a directory/does not exist"
            )
        self.movies_path = movies_path
        self.startup_movie_path = movies_path / "deck_startup.webm"
        self.startup_movie_exists = self.startup_movie_path.is_file()

    def __repr__(self) -> str:
        return f"Movie Randomizer with path to: {self.movies_path}"

    def rename_boot_movie(self, startup_movie_new: Path, copy_file: bool = False):
        """Copies or creates a hardlink for deck_startup.webm pointing to
        startup_movie_new, depending of the value of copy_file.
        If the Python version is lower than 3.10, defaults to copying the file.

        Args:
            startup_movie_new (Path): Path to the startup movie to copy/hardlink
                to.
            copy_file (bool, optional): If True, copies the file instead of
                creating a hard link. Defaults to False.
        """
        logging.info(f"Using {startup_movie_new} as new startup movie")
        if copy_file or sys.version_info < (3, 10):
            shutil.copyfile(str(startup_movie_new), str(self.startup_movie_path))
        else:
            self.startup_movie_path.hardlink_to(startup_movie_new)

    def randomize_boot_movie(self) -> int:
        """Randomly selects a new boot movie from the available movies in the
        directory that end in deck_startup.webm

        Raises:
            FileNotFoundError: If the movies directory does not exist.
            FileNotFoundError: If no movies are found in the movies directory.

        Returns:
            int: 1 If it succesfully changes the startup movie, -1 if it doesn't.
        """
        succesful_run = -1
        if self.movies_path.is_dir():
            boot_movies = sorted(
                list(self.movies_path.glob("*deck_startup.webm"))
                + list(self.movies_path.glob("*deck_startup.WEBM"))
            )
            if boot_movies:
                startup_movie_new = boot_movies[random.randint(0, len(boot_movies) - 1)]
                # Rename new movie to deck_startup.webm
                self.rename_boot_movie(
                    self.startup_movie_path,
                    startup_movie_new,
                )
                succesful_run = 1
            else:
                logging.warning(f"Could not find movies in {self.movies_path}")
                raise FileNotFoundError(f"No movies were found in {self.movies_path}")

        else:
            logging.warning(
                f"Could not find the {self.movies_path} directory in {self.movies_path.resolve().parents[2]}"
            )
            raise FileNotFoundError(f"No directory exists in {self.movies_path}")
        return succesful_run


if __name__ == "__main__":
    try:
        movie_randomizer = MovieRandomizer(Path("uioverrides") / "movies")
        movie_randomizer.randomize_boot_movie()
    except:
        logging.expection("Error running the movie randomization script")
