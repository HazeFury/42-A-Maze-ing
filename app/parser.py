from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional, Dict
import sys


class MazeConfig(BaseModel):
    width: int = Field(alias="WIDTH", ge=4)
    height: int = Field(alias="HEIGHT", ge=4)
    entry_coord: tuple[int, int] = Field(alias="ENTRY")
    exit_coord: tuple[int, int] = Field(alias="EXIT")
    output_file: str = Field(alias="OUTPUT_FILE")
    perfect: bool = Field(alias="PERFECT")
    seed: Optional[int] = Field(None, alias="SEED", ge=0)

    # #### transformer AVANT validation la str de la valeur d'ENTRY et d'EXIT en tuple####
    # @field_validator
    # classmethod()

    # ### vérifier que l entree et la sortie sont bien dans le labyrinthe ###

    # ## vérifier ENTRY != EXIT###


def parsing_config_file() -> Dict[str, str | int | tuple[int, int]]:

    raw_data: dict[str, str | int] = dict()

    if len(sys.argv) > 2:
        print("Too many arguments ! This project takes only one argument to work")
        print("Try the following command : 'python3 a_maze_ing.py config.txt'")
        sys.exit(1)

    try:
        with open(sys.argv[1], "r") as config:
            for line in config:
                if not line.startswith("#"):
                    # print(f"-- {line}", end="")
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
        print(f"[ERROR] File not found : '{sys.argv[1]}'")
        sys.exit(1)
