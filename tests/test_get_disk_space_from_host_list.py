from datetime import datetime

DF_OUTPUT = """Filesystem      Size  Used Avail Use% Mounted on
/dev/vda15      105M  6.1M   99M   6% /boot/efi
/dev/vda1        40G   33G  5.0G  87% /
"""


def test_consulta_cada_host_via_ssh(pydiskwatch, monkeypatch):
    chamadas = []

    def fake_check_output(cmd, text):
        chamadas.append((cmd, text))
        return DF_OUTPUT

    monkeypatch.setattr(pydiskwatch.subprocess, "check_output", fake_check_output)

    pydiskwatch.get_disk_space_from_host_list(["user@a", "user@b"])

    assert chamadas == [
        (["ssh", "user@a", "df -h"], True),
        (["ssh", "user@b", "df -h"], True),
    ]


def test_monta_resultado_com_data_e_uso(pydiskwatch, monkeypatch):
    monkeypatch.setattr(
        pydiskwatch.subprocess, "check_output", lambda cmd, text: DF_OUTPUT
    )
    hoje = datetime.now().strftime("%Y-%m-%d")

    resultado = pydiskwatch.get_disk_space_from_host_list(["user@a"])

    assert resultado == {"user@a": [{"datetime": hoje, "usage": "87%"}]}


def test_lista_de_hosts_vazia_nao_chama_ssh(pydiskwatch, monkeypatch):
    def nao_deve_ser_chamado(cmd, text):
        raise AssertionError("subprocess.check_output nao deveria ser chamado")

    monkeypatch.setattr(pydiskwatch.subprocess, "check_output", nao_deve_ser_chamado)

    assert pydiskwatch.get_disk_space_from_host_list([]) == {}


def test_uso_fica_none_quando_host_nao_tem_particao_raiz(pydiskwatch, monkeypatch):
    sem_raiz = "Filesystem Size Used Avail Use% Mounted on\ntmpfs 392M 0 392M 0% /run\n"
    monkeypatch.setattr(
        pydiskwatch.subprocess, "check_output", lambda cmd, text: sem_raiz
    )

    resultado = pydiskwatch.get_disk_space_from_host_list(["user@a"])

    assert resultado["user@a"][0]["usage"] is None
