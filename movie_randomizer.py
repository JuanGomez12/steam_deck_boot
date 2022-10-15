from pathlib import Path
import random
import logging
import shutil

logging.basicConfig()

def randomize_boot_movie():
    movies_path = Path('uioverrides') / 'movies'
    startup_movie_old = movies_path / 'deck_startup.webm'
    if movies_path.is_dir():
        boot_movies = sorted(list(movies_path.glob('*deck_startup.webm')) + list(movies_path.glob('*deck_startup.WEBM')))
        if boot_movies:
            new_boot_movie = boot_movies[random.randint(0, len(boot_movies) - 1)]
            if startup_movie_old.exists():
                # Rename current movie
                counter=1
                while startup_movie_old.exists():
                    startup_movie = movies_path / f'old_{counter}_{startup_movie_old.name}'
                    counter+=1
                if not startup_movie_old.exists():
                    logging.info(f'Renaming {startup_movie_old} to {startup_movie}')
                    startup_movie.rename(startup_movie_old)
            else:
                # Rename new movie to deck_startup.webm
                logging.info(f'Using {new_boot_movie} as new startup movie')
                shutil.copyfile(str(new_boot_movie), str(startup_movie_old))
        else:
            logging.warning(f'Could not find movies in {movies_path}')
    else:
        logging.warning(f'Could not find the uioverrides/movies directory in {movies_path.resolve().parents[2]}')

if __name__ == "__main__":
    randomize_boot_movie()