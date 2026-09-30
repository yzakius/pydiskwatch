import pytest


@pytest.mark.parametrize(
    "caso, output, esperado",
    [
        (
            "particao raiz unica",
            [
                "Filesystem      Size  Used Avail Use% Mounted on",
                "/dev/vda1        40G   12G   26G  32% /",
            ],
            "32%",
        ),
        (
            "raiz entre outros mounts",
            [
                "Filesystem      Size  Used Avail Use% Mounted on",
                "/dev/vda15      105M  6.1M   99M   6% /boot/efi",
                "/dev/vda1        40G   33G  5.0G  87% /",
                "tmpfs           392M     0  392M   0% /run/user/1000",
            ],
            "87%",
        ),
        (
            "espacos e tabs misturados",
            [
                "Filesystem Size Used Avail Use% Mounted on",
                "/dev/sda1\t100G   50G\t50G   50%\t/",
            ],
            "50%",
        ),
    ],
)
def test_retorna_uso_da_particao_raiz(process_output, caso, output, esperado):
    assert process_output(output) == esperado


def test_retorna_a_primeira_raiz_encontrada(process_output):
    output = [
        "Filesystem      Size  Used Avail Use% Mounted on",
        "/dev/vda1        40G   33G  5.0G  87% /",
        "/dev/vdb1        40G   12G   26G  32% /",
    ]

    assert process_output(output) == "87%"


@pytest.mark.parametrize(
    "caso, output",
    [
        (
            "sem particao raiz",
            [
                "Filesystem      Size  Used Avail Use% Mounted on",
                "/dev/vda15      105M  6.1M   99M   6% /boot/efi",
                "tmpfs           392M     0  392M   0% /run/user/1000",
            ],
        ),
        ("saida vazia", []),
        ("apenas o cabecalho", ["Filesystem      Size  Used Avail Use% Mounted on"]),
    ],
)
def test_retorna_none_quando_nao_ha_raiz(process_output, caso, output):
    assert process_output(output) is None
