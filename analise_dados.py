
import re
import csv

# EXCEÇÕES PERSONALIZADAS

class FormatoInvalidoError(Exception):
    """Erro quando o formato de um campo não bate com o padrão esperado."""
    pass


class IdadeInvalidaError(Exception):
    """Erro quando a idade está fora do intervalo aceito (0 a 120)."""
    pass

# PADRÕES DE REGEX (raw strings)

PADRAO_EMAIL = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
PADRAO_CPF = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
PADRAO_TELEFONE = r"^\(\d{2}\) \d{4,5}-\d{4}$"
PADRAO_DATA = r"^\d{2}/\d{2}/\d{4}$"

# FUNÇÕES DE VALIDAÇÃO

def validar_campo(nome_campo, valor, padrao):
    # se não casar com o padrão, lança o erro personalizado
    if not re.match(padrao, valor):
        raise FormatoInvalidoError(f"{nome_campo} com formato inválido: '{valor}'")


def validar_email(email):
    validar_campo("E-mail", email, PADRAO_EMAIL)


def validar_cpf(cpf):
    validar_campo("CPF", cpf, PADRAO_CPF)


def validar_telefone(telefone):
    validar_campo("Telefone", telefone, PADRAO_TELEFONE)


def validar_data(data):
    validar_campo("Data", data, PADRAO_DATA)


def validar_idade(texto_idade):
    # int() pode lançar ValueError se não for número
    idade = int(texto_idade)
    if idade < 0 or idade > 120:
        raise IdadeInvalidaError(f"Idade fora do intervalo permitido: {idade}")

# LEITURA DO ARQUIVO

def ler_arquivo(caminho):
    registros = []
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                registros.append(linha)
    except FileNotFoundError:
        print(f"Erro: o arquivo '{caminho}' não foi encontrado.")
        return None
    else:
        print(f"Arquivo '{caminho}' lido com sucesso ({len(registros)} registros).")
        return registros
    finally:
        # sempre executa, dando erro ou não
        print("Leitura do arquivo finalizada.")


# PROCESSAMENTO DOS REGISTROS

def processar_registros(registros):
    validos = []
    invalidos = []  # cada item: (nome, motivo)

    for registro in registros:
        try:
            nome = registro["nome"]
            validar_email(registro["email"])
            validar_cpf(registro["cpf"])
            validar_telefone(registro["telefone"])
            validar_data(registro["data"])
            validar_idade(registro["idade"])
        except KeyError as erro:
            # coluna ausente no CSV: não adianta continuar
            print(f"Erro: coluna {erro} ausente no arquivo.")
            return None, None
        except FormatoInvalidoError as erro:
            invalidos.append((registro["nome"], str(erro)))
        except IdadeInvalidaError as erro:
            invalidos.append((registro["nome"], str(erro)))
        except ValueError:
            invalidos.append((registro["nome"], f"Idade não é um número: '{registro['idade']}'"))
        else:
            validos.append(nome)

    return validos, invalidos


# RELATÓRIO FINAL (f-strings)

def gerar_relatorio(total, validos, invalidos):
    percentual = (len(validos) / total) * 100 if total > 0 else 0

    linhas = []
    linhas.append("=" * 45)
    linhas.append("RELATÓRIO DE ANÁLISE DE DADOS")
    linhas.append("=" * 45)
    linhas.append(f"Total de registros: {total}")
    linhas.append(f"Registros válidos: {len(validos)}")
    linhas.append(f"Registros inválidos: {len(invalidos)}")
    linhas.append(f"Percentual de aprovação: {percentual:.1f}%")

    linhas.append("\nDados válidos:")
    for nome in validos:
        linhas.append(f"  [OK] {nome}")

    linhas.append("\nDados inválidos:")
    for nome, motivo in invalidos:
        linhas.append(f"  [ERRO] {nome} -> {motivo}")

    return "\n".join(linhas)


def main():
    registros = ler_arquivo("dados.csv")
    if registros is None:
        return

    validos, invalidos = processar_registros(registros)
    if validos is None:
        return

    relatorio = gerar_relatorio(len(registros), validos, invalidos)
    print("\n" + relatorio)

main()
