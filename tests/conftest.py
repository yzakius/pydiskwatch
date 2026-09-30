import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture(scope="session")
def pydiskwatch():
    """Importa o módulo sem deixar o load_dotenv() de import-time ler o .env."""
    with patch("dotenv.load_dotenv"):
        import pydiskwatch as module

    return module


@pytest.fixture
def process_output(pydiskwatch):
    return pydiskwatch.process_output


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    """Executa o teste em um diretório temporário (save_data grava em caminho relativo)."""
    monkeypatch.chdir(tmp_path)
    return tmp_path
