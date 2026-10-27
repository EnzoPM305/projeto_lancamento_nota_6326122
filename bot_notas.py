import time

import pyautogui
import pyperclip

from validacao_notas import analisar_alunos, calcular_resultado


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

CAMPOS_FORMULARIO = ["RA", "Nome", "Nota01", "Nota02", "TF01", "TF02"]


def normalizar_busca(texto):
    return " ".join(texto.split()).casefold()


def buscar_aluno(resultados, busca):
    # Compara o RA ou o nome completo, sem escolher entre homônimos.
    termo = normalizar_busca(busca)
    encontrados = []

    for resultado in resultados:
        dados = resultado["dados"]

        if (
            normalizar_busca(dados["RA"]) == termo
            or normalizar_busca(dados["Nome"]) == termo
        ):
            encontrados.append(resultado)

    return encontrados


def preencher_formulario(dados):
    print("\nVocê tem 10 segundos para clicar na resposta do campo RA.")
    time.sleep(10)

    for indice, campo in enumerate(CAMPOS_FORMULARIO):
        pyautogui.hotkey("ctrl", "a")
        pyperclip.copy(dados[campo])
        pyautogui.hotkey("ctrl", "v")

        if indice < len(CAMPOS_FORMULARIO) - 1:
            pyautogui.press("tab")

    print("Preenchimento concluído.")
    print("Confira os dados no formulário antes de continuar.")

    input("Volte ao terminal e pressione Enter para tentar enviar...")

    print("Você tem 5 segundos para voltar ao formulário.")
    time.sleep(5)

    # Parte do último campo para o botão Enviar.
    pyautogui.press("tab")
    pyautogui.press("enter")

    print("Comando de envio executado.")
    print("Confira no navegador se a resposta foi registrada.")


def executar():
    resultados = analisar_alunos()
    busca = input("Digite o RA ou o nome completo do aluno: ").strip()

    if not busca:
        print("Informe um RA ou nome para pesquisar.")
        return

    encontrados = buscar_aluno(resultados, busca)

    if not encontrados:
        print("Aluno não encontrado.")
        return

    if len(encontrados) > 1:
        print("Mais de um registro encontrado. É necessária uma revisão.")
        return

    resultado = encontrados[0]

    if resultado["pendencias"]:
        print("\nPreenchimento bloqueado pelas seguintes pendências:")

        for pendencia in resultado["pendencias"]:
            print(f"- {pendencia}")

        return

    print("\nDados que serão preenchidos:")

    for campo in CAMPOS_FORMULARIO:
        print(f"{campo}: {resultado['dados'][campo]}")

        periodo_1, periodo_2, media, situacao = calcular_resultado(
        resultado["dados"]
    )

    print("\nResultado da simulação:")
    print(f"Período 1: {periodo_1:.2f}")
    print(f"Período 2: {periodo_2:.2f}")
    print(f"Média final: {media:.2f}")
    print(f"Situação simulada: {situacao}")
    print("Hipótese: notas de 0 a 10, pesos 8 e 2, aprovação a partir de 6.")

    preencher_formulario(resultado["dados"])

if __name__ == "__main__":
    executar()