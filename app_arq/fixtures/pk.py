import json

def corrigir_pk(arquivo_json):
    with open(arquivo_json, 'r') as file:
        data = json.load(file)

    pk_set = set()  # Conjunto para rastrear valores de "pk" já usados

    for entry in data:
        current_pk = entry.get("pk")

        # Verificar se o valor de "pk" já foi usado
        while current_pk in pk_set:
            current_pk += 1

        entry["pk"] = current_pk
        pk_set.add(current_pk)

    with open(arquivo_json, 'w') as file:
        json.dump(data, file, indent=2)

# Chamando a função para corrigir o arquivo JSON
corrigir_pk("codigos.json")
