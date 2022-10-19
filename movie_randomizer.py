from pathlib import Path
import random
import logging
import shutil
import json

logging.basicConfig()

MOVIES_PATH = Path("uioverrides") / "movies"
STARTUP_MOVIE_PATH = MOVIES_PATH / "deck_startup.webm"
STARTUP_MOVIE_ORIGINAL_NAME = MOVIES_PATH / "deck_startup_name.json"



def rename_boot_movie(
    startup_movie_path: Path, startup_movie_new: Path, file_save_path: Path
):
    logging.info(f"Using {startup_movie_new} as new startup movie")
    shutil.copyfile(str(startup_movie_new), str(startup_movie_path))
    # Save olf file name
    with open(file_save_path, "w") as file_handle:
        json.dump(file_handle, {"startup_movie_name": str(startup_movie_new)})


def randomize_boot_movie(config: dict) -> int:
    movies_path = config["movies_path"]
    startup_movie_path = config["startup_movie_path"]
    startup_movie_original_name = config["startup_movie_original_name"]

    if movies_path.is_dir():
        boot_movies = sorted(
            list(movies_path.glob("*deck_startup.webm"))
            + list(movies_path.glob("*deck_startup.WEBM"))
        )
        if boot_movies:
            startup_movie_new = boot_movies[random.randint(0, len(boot_movies) - 1)]
            # Rename new movie to deck_startup.webm
            if startup_movie_path.is_file() and startup_movie_original_name.is_file():
                # Old deck_startup video name is known
                with open(startup_movie_original_name, "r") as file_handle:
                    data = json.load(file_handle)
                old_startup_movie_name = Path(
                    data.get("startup_movie_name", find_generic_name())
                )
                startup_movie_path.rename(old_startup_movie_name)
                rename_boot_movie(
                    startup_movie_path, startup_movie_new, startup_movie_original_name
                )

            elif startup_movie_path.is_file():
                # Old deck_startup video is not known (text file could not be found)
                logging.info(
                    f"Could not find {startup_movie_original_name}, renaming old movie with generic name"
                )
                old_startup_movie_new_name = find_generic_name()
                startup_movie_path.rename(old_startup_movie_new_name)
                # Rename new file
                rename_boot_movie(
                    startup_movie_path, startup_movie_new, startup_movie_original_name
                )
            else:
                rename_boot_movie(
                    startup_movie_path, startup_movie_new, startup_movie_original_name
                )

        else:
            logging.warning(f"Could not find movies in {movies_path}")
    else:
        logging.warning(
            f"Could not find the uioverrides/movies directory in {movies_path.resolve().parents[2]}"
        )
        return -1


def find_generic_name(directory_path: Path = MOVIES_PATH) -> Path:
    old_startup_movie_new_name = (directory_path / f"deck_startup_old").with_suffix(
        STARTUP_MOVIE_PATH.suffix
    )
    if old_startup_movie_new_name.is_file():
        counter = 2
        old_startup_movie_new_name = (
            directory_path
            / f"deck_startup_old_{counter}{old_startup_movie_new_name.suffix}"
        )
        while old_startup_movie_new_name.is_file():
            counter += 1
            old_startup_movie_new_name = (
                directory_path
                / f"deck_startup_old_{counter}{old_startup_movie_new_name.suffix}"
            )
    return old_startup_movie_new_name


if __name__ == "__main__":
    config = {
        "movies_path": Path("uioverrides") / "movies",
        "startup_movie_path": MOVIES_PATH / "deck_startup.webm",
        "startup_movie_original_name": MOVIES_PATH / "deck_startup_name.json",
    }
    randomize_boot_movie(config)
