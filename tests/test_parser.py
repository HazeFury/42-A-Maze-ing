import pytest
from pydantic import ValidationError
from app.parser import MazeConfig, parsing_config_file


def test_maze_config_valid_data() -> None:
    """Test that the model accepts a perfectly valid dictionary."""
    raw_data = {
        "WIDTH": "20",
        "HEIGHT": "15",
        "ENTRY": "0,0",
        "EXIT": "19,14",
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": "True",
        "SEED": "42"
    }
    config = MazeConfig(**raw_data)

    assert config.width == 20
    assert config.height == 15
    assert config.perfect is True
    assert config.seed == "42"
    assert config.entry_coord == (0, 0)
    assert config.exit_coord == (19, 14)


def test_maze_config_invalid_size() -> None:
    """Test that the width/height cannot be strictly less than 2."""
    raw_data = {
        "WIDTH": "1",
        "HEIGHT": "15",
        "ENTRY": "0,0",
        "EXIT": "19,14",
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": "True"
    }
    with pytest.raises(ValidationError):
        MazeConfig(**raw_data)


def test_maze_config_entry_equals_exit() -> None:
    """Test that the model rejects identical entry and exit coordinates."""
    raw_data = {
        "WIDTH": "20",
        "HEIGHT": "15",
        "ENTRY": "5,5",
        "EXIT": "5,5",
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": "True"
    }
    with pytest.raises(ValidationError):
        MazeConfig(**raw_data)


def test_parsing_config_file_success(tmp_path) -> None:
    """Test reading a valid configuration file while ignoring comments."""
    fake_config = tmp_path / "config.txt"
    fake_config.write_text(
        "# Ceci est un commentaire\n"
        "WIDTH=10\n"
        "HEIGHT=10\n"
        "ENTRY=1,1\n"
        "EXIT=8,8\n"
        "OUTPUT_FILE=test.txt\n"
        "PERFECT=True\n"
    )

    data = parsing_config_file(str(fake_config))

    assert data.width == 10
    assert data.height == 10
    assert data.entry_coord == (1, 1)
    assert data.exit_coord == (8, 8)
    assert data.output_file == "test.txt"
    assert data.perfect is True


def test_parsing_config_file_not_found() -> None:
    """
    Test that the function raises a FileNotFoundError
    if the file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        parsing_config_file("fichier_fantome.txt")


def test_parsing_missing_key(tmp_path) -> None:
    """Verify the error when a mandatory key (WIDTH) is missing."""
    bad_config = tmp_path / "missing_width.txt"
    bad_config.write_text(
        "HEIGHT=10\n"
        "ENTRY=1,1\n"
        "EXIT=8,8\n"
        "OUTPUT_FILE=out.txt\n"
        "PERFECT=True\n"
    )


def test_parsing_out_of_bounds_coords(tmp_path) -> None:
    """Verify the error if ENTRY is outside the maze dimensions."""
    bad_config = tmp_path / "out_of_bounds.txt"
    bad_config.write_text(
        "WIDTH=10\n"
        "HEIGHT=10\n"
        "ENTRY=15,15\n"
        "EXIT=8,8\n"
        "OUTPUT_FILE=out.txt\n"
        "PERFECT=True\n"
    )
