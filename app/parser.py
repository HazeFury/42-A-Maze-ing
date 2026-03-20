from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional


class MazeConfig(BaseModel):
    width: int = Field(alias="WIDTH", ge=2)
    height: int = Field(alias="HEIGHT", ge=2)
    entry: tuple[int, int] = Field(alias="ENTRY")
    exit: tuple[int, int] = Field(alias="EXIT")
    output_file: str = Field(alias="OUTPUT_FILE")
    perfect: bool = Field(alias="PERFECT")
    seed: Optional[int] = Field(None, alias="SEED", ge=0)
    algorithm: str = Field(alias="ALGORITHM")
    display: str = Field(alias="DISPLAY")

    ##### transformer AVANT validation la str de la valeur d'ENTRY et d'EXIT en tuple####
    @field_validator
    classmethod()

    #### vérifier que l entree et la sortie sont bien dans le labyrinthe ###

    ### vérifier ENTRY != EXIT###

    ### Possibilite du 42 ###


