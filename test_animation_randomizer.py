from pathlib import Path

import pytest

from animation_randomizer import AnimationRandomizer


def test_new_animation_renaming(tmp_path: Path):
    animation_randomizer = AnimationRandomizer(tmp_path)
    new_startup_animation_path = tmp_path / "new_startup_animation.webm"
    new_startup_animation_path.touch()
    animation_randomizer.rename_boot_animation(new_startup_animation_path)
    assert animation_randomizer.startup_animation_path.is_file()
    assert new_startup_animation_path.is_file()


def test_error_renaming_missing_new_animation(tmp_path: Path):
    animation_randomizer = AnimationRandomizer(tmp_path)
    new_startup_animation_path = tmp_path / "new_startup_animation.webm"
    # new_startup_animation_path.touch()
    with pytest.raises(FileNotFoundError, match=r"Could not find animation .*"):
        animation_randomizer.rename_boot_animation(new_startup_animation_path)


def test_error_wrong_animations_path_type():
    with pytest.raises(TypeError, match=r"Expected Path type, received .*"):
        AnimationRandomizer("test")


def test_error_missing_animations_path(tmp_path):
    with pytest.raises(
        FileNotFoundError, match=r".* is not a directory/does not exist"
    ):
        AnimationRandomizer(tmp_path / "test")


def test_error_no_animations_in_directory(tmp_path: Path):
    with pytest.raises(FileNotFoundError, match=r"No animations were found in .*"):
        animation_randomizer = AnimationRandomizer(tmp_path)
        animation_randomizer.randomize_boot_animation()


def test_correct_randomization_of_animations(tmp_path: Path):
    [
        (tmp_path / f"new_startup_animation_{i}_deck_startup.webm").touch()
        for i in range(10)
    ]
    animation_randomizer = AnimationRandomizer(tmp_path)
    animation = animation_randomizer.randomize_boot_animation(random_seed=42)
    assert animation.is_file()
    assert animation_randomizer.startup_animation_path.is_file()


def test_only_one_animation_available(tmp_path: Path):
    [
        (tmp_path / f"new_startup_animation_{i}_deck_startup.webm").touch()
        for i in range(1)
    ]
    animation_randomizer = AnimationRandomizer(tmp_path)
    animation_1 = animation_randomizer.randomize_boot_animation(random_seed=42)
    animation_2 = animation_randomizer.randomize_boot_animation(random_seed=42)
    assert animation_2.is_file()
    assert animation_1 == animation_2
    assert animation_randomizer.startup_animation_path.is_file()
