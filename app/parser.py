from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from typing import Optional, Dict, Any


class MazeConfig(BaseModel):
    width: int = Field(alias="WIDTH", ge=2)
    height: int = Field(alias="HEIGHT", ge=2)
    entry_coord: tuple[int, int] = Field(alias="ENTRY")
    exit_coord: tuple[int, int] = Field(alias="EXIT")
    output_file: str = Field(alias="OUTPUT_FILE")
    perfect: bool = Field(alias="PERFECT")
    seed: Optional[int] = Field(None, alias="SEED", ge=0)

    @field_validator("entry_coord", "exit_coord", mode="before")
    @classmethod
    def parse_coord(cls, value: Any) -> Any:
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
    def check_entry_and_exit(self) -> 'MazeConfig':
        if self.entry_coord == self.exit_coord:
            raise ValueError("ENTRY or EXIT point must be different")

        x_entry, y_entry = self.entry_coord
        x_exit, y_exit = self.exit_coord

        if not (
            0 <= x_entry < self.width and
            0 <= y_entry < self.height
        ):
            raise ValueError(f"Invalid ENTRY : {self.entry_coord} "
                             f"it must be inside the maze bounds")

        if not (
            0 <= x_exit < self.width and
            0 <= y_exit < self.height
        ):
            raise ValueError(f"Invalid EXIT : {self.exit_coord} "
                             f"it must be inside the maze bounds")

        return self


def parsing_config_file(filepath: str) -> Dict[str, str | int | tuple[int, int]]:

    raw_data: dict[str, str | int] = dict()

    try:
        with open(filepath, "r") as config:
            for line in config:
                if not line.startswith("#"):
                    parts: list[str] = line.split("=")
                    if len(parts) == 2:
                        key: str = parts[0]
                        value: str = parts[1]
                        value = value.replace("\n", "")
                        raw_data.update({key: value})
        print(raw_data)
        data = MazeConfig(**raw_data)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found : '{filepath}'")
