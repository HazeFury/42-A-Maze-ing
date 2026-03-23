import pytest
from pydantic import ValidationError
from app.parser import MazeConfig, parsing_config_file

# --- TESTS POUR LE MODELE PYDANTIC (MazeConfig) ---


def test_maze_config_valid_data():
    """Test que le modèle accepte un dictionnaire parfait."""
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

    # On vérifie que Pydantic a bien casté les types
    assert config.width == 20
    assert config.height == 15
    assert config.perfect is True
    assert config.seed == 42
    assert config.entry_coord == (0, 0)
    assert config.exit_coord == (19, 14)


def test_maze_config_invalid_size():
    """Test que la largeur/hauteur ne peut pas être inférieure à 2."""
    raw_data = {
        "WIDTH": "1",  # Invalide !
        "HEIGHT": "15",
        "ENTRY": "0,0",
        "EXIT": "19,14",
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": "True"
    }
    with pytest.raises(ValidationError):
        MazeConfig(**raw_data)


def test_maze_config_entry_equals_exit():
    """Test que le modèle refuse une entrée et une sortie identiques."""
    raw_data = {
        "WIDTH": "20",
        "HEIGHT": "15",
        "ENTRY": "5,5",
        "EXIT": "5,5",  # Invalide car identique à ENTRY !
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": "True"
    }
    with pytest.raises(ValidationError):
        MazeConfig(**raw_data)

# --- TESTS POUR LA LECTURE DU FICHIER (parsing_config_file) ---


def test_parsing_config_file_success(tmp_path):
    """Test la lecture d'un fichier de configuration
    valide en ignorant les commentaires.
    """
    # tmp_path est fourni par pytest. On crée un faux fichier config.txt
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

    # On vérifie les attributs de l'objet MazeConfig (Pydantic a déjà converti les types)
    assert data.width == 10
    assert data.height == 10
    assert data.entry_coord == (1, 1)
    assert data.exit_coord == (8, 8)
    assert data.output_file == "test.txt"
    assert data.perfect is True


def test_parsing_config_file_not_found():
    """Test que la fonction lève bien une erreur si le fichier n'existe pas."""
    with pytest.raises(FileNotFoundError):
        parsing_config_file("fichier_fantome.txt")

##########

def test_parsing_missing_key(tmp_path):
    """Vérifie l'erreur quand une clé obligatoire (WIDTH) manque."""
    bad_config = tmp_path / "missing_width.txt"
    # On oublie volontairement la ligne WIDTH
    bad_config.write_text(
        "HEIGHT=10\n"
        "ENTRY=1,1\n"
        "EXIT=8,8\n"
        "OUTPUT_FILE=out.txt\n"
        "PERFECT=True\n"
    )


def test_parsing_out_of_bounds_coords(tmp_path):
    """Vérifie l'erreur si ENTRY est en dehors du labyrinthe (15,15 pour un 10x10)."""
    bad_config = tmp_path / "out_of_bounds.txt"
    bad_config.write_text(
        "WIDTH=10\n"
        "HEIGHT=10\n"
        "ENTRY=15,15\n"  # <--- Erreur ici
        "EXIT=8,8\n"
        "OUTPUT_FILE=out.txt\n"
        "PERFECT=True\n"
    )
