from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional, Dict


class MazeConfig(BaseModel):
    width: int = Field(alias="WIDTH", ge=4)  # Je pense qu'il faut au minimun un maze de 4x4 si on veut respecter la consigne
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
        # data = MazeConfig(**raw_data)  // a decommenter quand le MazeConfig seras opérationnel
        # return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found : '{filepath}'")
