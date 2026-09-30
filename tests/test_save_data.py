import json

HISTORY = "history_disc_usage.json"


def test_cria_o_arquivo_quando_nao_existe(pydiskwatch, workdir):
    dados = {"user@a": [{"datetime": "2026-09-30", "usage": "42%"}]}

    pydiskwatch.save_data(dados)

    assert json.loads((workdir / HISTORY).read_text()) == dados


def test_acrescenta_ao_historico_do_host_existente(pydiskwatch, workdir):
    (workdir / HISTORY).write_text(
        json.dumps({"user@a": [{"datetime": "2026-09-29", "usage": "40%"}]})
    )

    pydiskwatch.save_data({"user@a": [{"datetime": "2026-09-30", "usage": "42%"}]})

    assert json.loads((workdir / HISTORY).read_text()) == {
        "user@a": [
            {"datetime": "2026-09-29", "usage": "40%"},
            {"datetime": "2026-09-30", "usage": "42%"},
        ]
    }


def test_preserva_hosts_que_nao_estao_na_coleta_atual(pydiskwatch, workdir):
    (workdir / HISTORY).write_text(
        json.dumps({"user@antigo": [{"datetime": "2026-09-29", "usage": "10%"}]})
    )

    pydiskwatch.save_data({"user@novo": [{"datetime": "2026-09-30", "usage": "42%"}]})

    historico = json.loads((workdir / HISTORY).read_text())
    assert historico["user@antigo"] == [{"datetime": "2026-09-29", "usage": "10%"}]
    assert historico["user@novo"] == [{"datetime": "2026-09-30", "usage": "42%"}]


def test_grava_json_legivel_e_sem_escapar_acentos(pydiskwatch, workdir):
    pydiskwatch.save_data({"servidor-são-paulo": [{"datetime": "2026-09-30", "usage": "42%"}]})

    conteudo = (workdir / HISTORY).read_text()
    assert "servidor-são-paulo" in conteudo
    assert "\n  " in conteudo


def test_dados_vazios_geram_historico_vazio(pydiskwatch, workdir):
    pydiskwatch.save_data({})

    assert json.loads((workdir / HISTORY).read_text()) == {}
