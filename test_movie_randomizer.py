from pathlib import Path

import pytest

from movie_randomizer import MovieRandomizer


def test_new_movie_renaming(tmp_path: Path):
    movie_randomizer = MovieRandomizer(tmp_path)
    new_startup_movie_path = tmp_path / "new_startup_movie.webm"
    new_startup_movie_path.touch()
    movie_randomizer.rename_boot_movie(new_startup_movie_path)
    assert movie_randomizer.startup_movie_path.is_file()
    assert new_startup_movie_path.is_file()


def test_error_wrong_movies_path_type():
    with pytest.raises(TypeError, match=r"Expected Path type, received .*"):
        MovieRandomizer("test")


def test_error_missing_movies_path(tmp_path):
    with pytest.raises(
        FileNotFoundError, match=r".* is not a directory/does not exist"
    ):
        MovieRandomizer(tmp_path / "test")


def test_error_no_movies_in_directory(tmp_path: Path):
    with pytest.raises(FileNotFoundError, match=r"No movies were found in .*"):
        movie_randomizer = MovieRandomizer(tmp_path)
        movie_randomizer.randomize_boot_movie()


# def test_correct_randomization_of_movies():
#     pass
