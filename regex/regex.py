import re

def regex():
    target = "Número Agência: 1973\nDescrição Agência: Humberto Doisberto\nContato Agência: 11 9999-9999"

    # Buscar por número da agência
    match = re.search(r"Número Agência: (\d{4})", target)
    if match:
        numero_ag = match.group(1)
        print(f"{numero_ag}")
    else:
        print(f"Padrão de número de agências não encontrado")

    # Buscar por número de telefone
    match = re.search(r"\d{2} \d{4}-\d{4}", target)
    if match:
        telefone = match.group(0)
        print(f"{telefone}")
    else:
        print(f"Padrão de número de telefone não encontrado")

    # Buscar por descrição
    # (.+?) - Buscar carácteres após 'Descrição Agência: '
    # (\n|$) - Garante que o final da string seja um 'newline' ou o fim de uma string
    match = re.search(r"Descrição Agência: (.+?)(\n|$)", target)
    if match:
        descricao = match.group(1)
        print(f"{descricao}")

regex()