import pytest


def uso(valor):
    return [{"datetime": "2026-09-30", "usage": valor}]


def test_agrupa_hosts_nas_duas_faixas(pydiskwatch, capsys):
    pydiskwatch.print_summary(
        {"critico": uso("91%"), "atencao": uso("65%"), "tranquilo": uso("12%")}
    )

    saida = capsys.readouterr().out
    assert "Acima de 80%" in saida
    assert "critico -> 91%" in saida
    assert "Acima de 50%" in saida
    assert "atencao -> 65%" in saida
    assert "tranquilo" not in saida


def test_faixa_de_80_vem_antes_da_de_50(pydiskwatch, capsys):
    pydiskwatch.print_summary({"critico": uso("91%"), "atencao": uso("65%")})

    saida = capsys.readouterr().out
    assert saida.index("critico") < saida.index("Acima de 50%") < saida.index("atencao")


@pytest.mark.parametrize(
    "valor, faixa_80, faixa_50",
    [
        ("81%", True, False),
        ("80%", False, True),
        ("51%", False, True),
        ("50%", False, False),
    ],
)
def test_limites_das_faixas(pydiskwatch, capsys, valor, faixa_80, faixa_50):
    pydiskwatch.print_summary({"host": uso(valor)})

    acima_80, acima_50 = capsys.readouterr().out.split("Acima de 50%")
    assert ("host" in acima_80) is faixa_80
    assert ("host" in acima_50) is faixa_50


def test_imprime_os_cabecalhos_mesmo_sem_hosts(pydiskwatch, capsys):
    pydiskwatch.print_summary({})

    saida = capsys.readouterr().out
    assert "Acima de 80%" in saida
    assert "Acima de 50%" in saida


def test_falha_quando_o_uso_nao_foi_coletado(pydiskwatch):
    """process_output retorna None quando nao acha a raiz; o resumo nao trata esse caso."""
    with pytest.raises(AttributeError):
        pydiskwatch.print_summary({"host": uso(None)})
