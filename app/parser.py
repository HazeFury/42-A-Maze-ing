from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationError,
    Field,
    field_validator,
    model_validator)
from typing import Any


class MazeConfig(BaseModel):
    """Configuration schema for maze generation and validation.

    Attributes:
        width (int): Maze width, must be >= 2.
        height (int): Maze height, must be >= 2.
        entry_coord (Tuple[int, int]): Starting coordinates (x, y).
        exit_coord (Tuple[int, int]): Ending coordinates (x, y).
        output_file (str): Path to the output file.
        perfect (bool): Whether the maze is perfect (one unique path).
        seed (int | None): Seed for reproducibility.
        imperfection_rate (float | None): Rate of the maze imperfection
        (between 0 and 1)
    """
    # extra="forbid" => Throw error if any other key is provided in config file
    # popultate_by_name=True => allow use of alias (ex: WIDTH)
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    width: int = Field(alias="WIDTH", ge=2, le=100)
    height: int = Field(alias="HEIGHT", ge=2, le=100)
    entry_coord: tuple[int, int] = Field(alias="ENTRY")
    exit_coord: tuple[int, int] = Field(alias="EXIT")
    output_file: str = Field(alias="OUTPUT_FILE")
    perfect: bool = Field(alias="PERFECT")
    seed: int | None = Field(None, alias="SEED", ge=0)
    imperfection_rate: float | None = Field(
        None, alias="IMPERFECTION_RATE", gt=0, lt=1
        )

    @field_validator("entry_coord", "exit_coord", mode="before")
    @classmethod
    def parse_coord(cls, value: Any) -> Any:
        """Parse coordinate string into an integer tuple.

        Args:
            value (Any): Input value, expected to be 'x,y' string or tuple.

        Returns:
            Any: A tuple of two integers.

        Raises:
            ValueError: If the format is invalid or contains non-integers.
        """

        if isinstance(value, tuple):
            return value

        if isinstance(value, str):
            try:
                coord = value.replace(" ", "").split(",")
                if len(coord) != 2:
                    raise ValueError("Exactly two numbers required")
                return (int(coord[0]), int(coord[1]))
            except (ValueError, IndexError):
                raise ValueError(f"Invalid coordinates: {value}")

        return value

    @model_validator(mode='after')
    def validate_maze_logic(self) -> 'MazeConfig':
        """Validate the maze consistency:
            Check that entry and exit are distinct and within bounds.
            Check Perfection vs Imperfection Rate

        Returns:
            MazeConfig: The validated instance.

        Raises:
            ValueError: If invalid maze logic
        """
        if self.entry_coord == self.exit_coord:
            raise ValueError("ENTRY or EXIT point must be different")

        x_entry, y_entry = self.entry_coord
        x_exit, y_exit = self.exit_coord

        if not (
            0 <= x_entry < self.width and
            0 <= y_entry < self.height
        ):
            raise ValueError(f"Invalid ENTRY : {self.entry_coord} "
                             f"is outside the maze bounds")

        if not (
            0 <= x_exit < self.width and
            0 <= y_exit < self.height
        ):
            raise ValueError(f"Invalid EXIT : {self.exit_coord} "
                             f"is outside the maze bounds")

        if (
            self.perfect and
            self.imperfection_rate is not None and
            self.imperfection_rate > 0
        ):
            raise ValueError(
                "IMPERFECTION_RATE must be 0 or None if PERFECT is True"
            )

        if not self.perfect and self.imperfection_rate == 0:
            raise ValueError(
                "IMPERFECTION_RATE must be greater than 0 if PERFECT is False")

        return self


def parsing_config_file(filepath: str) -> MazeConfig:
    """Parse and validate configuration from a text file.

    Args:
        filepath (str): Path to the configuration file.

    Returns:
        MazeConfig: Validated configuration object.

    Raises:
        FileNotFoundError: If the config file is missing.
        ValueError: If duplicate keys or validation errors are found.
    """
    raw_data: dict[str, Any] = {}

    try:
        with open(filepath, "r") as config:

            for line in config:
                line = line.strip()

                if line and not line.startswith("#"):
                    parts: list[str] = line.split("=", 1)
                    if len(parts) == 2:
                        key: str = parts[0].strip()
                        value: str = parts[1].strip().strip('"').strip("'")
                        value = value.replace("\n", "")

                        if key in raw_data:
                            raise ValueError(f"Duplicate key '{key}' "
                                             f"in config file")

                        raw_data[key] = value

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found : '{filepath}'")

    try:
        return MazeConfig(**raw_data)

    except ValidationError as e:
        error_messages = []

        for error in e.errors():
            field = error['loc'][0] if error['loc'] else "Global"
            message = error['msg']
            error_messages.append(f"- {field}: {message}")

        raise ValueError(f"Invalid configuration in {filepath}:\n" +
                         "\n".join(error_messages))
