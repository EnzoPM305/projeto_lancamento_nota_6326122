import time

import pyautogui
import pyperclip

from leitor_notas import carregar_alunos


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


def preencher_campo(valor):
    # Usa a área de transferência para preservar acentos.
    pyperclip.copy(str(valor))
    pyautogui.hotkey("ctrl", "v")


def testar_preenchimento():
    alunos = carregar_alunos()
    aluno = alunos.iloc[0]

    # Segue a ordem dos campos no formulário.
    campos = ["RA", "Nome", "Nota01", "Nota02", "TF01", "TF02"]

    print("Você tem 10 segundos para clicar dentro do campo RA.")
    time.sleep(10)

    for indice, coluna in enumerate(campos):
        pyautogui.hotkey("ctrl", "a")
        preencher_campo(aluno[coluna])

        if indice < len(campos) - 1:
            pyautogui.press("tab")

    print("Preenchimento concluído. Confira os campos sem enviar.")


if __name__ == "__main__":
    testar_preenchimento()