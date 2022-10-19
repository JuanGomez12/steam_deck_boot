import logging
import random
import shutil
from pathlib import Path

logging.basicConfig()

MOVIES_PATH = Path("uioverrides") / "movies"
STARTUP_MOVIE_PATH = MOVIES_PATH / "deck_startup.webm"


class MovieRandomizer:
    def __init__(self, movies_path: Path) -> None:
        self.movies_path = movies_path
        self.startup_movie_path = movies_path / "deck_startup.webm"
        self.startup_movie_exists = self.startup_movie_path.is_file()

    def rename_boot_movie(self, startup_movie_new: Path, copy_file: bool = False):
        logging.info(f"Using {startup_movie_new} as new startup movie")
        if copy_file:
            shutil.copyfile(str(startup_movie_new), str(self.startup_movie_path))
        else:
            self.startup_movie_path.hardlink_to(startup_movie_new)

    def randomize_boot_movie(self) -> int:
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
                    self.startup_movie_original_name,
                )
            else:
                logging.warning(f"Could not find movies in {self.movies_path}")
        else:
            logging.warning(
                f"Could not find the uioverrides/movies directory in {self.movies_path.resolve().parents[2]}"
            )
            return -1


if __name__ == "__main__":
    movie_randomizer = MovieRandomizer(Path("uioverrides") / "movies")
    movie_randomizer.randomize_boot_movie()
