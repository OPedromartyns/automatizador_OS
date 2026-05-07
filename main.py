from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar


# ---------------- CALENDÁRIO ----------------

def escolher_data():
    data_escolhida = []

    def pegar_data():
        data_escolhida.append(cal.get_date())
        janela.destroy()

    def fechar():
        janela.destroy()

    janela = tk.Tk()
    janela.title("Selecionar OS")
    janela.geometry("350x350")

    tk.Label(
        janela,
        text="Selecionar OS",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    cal = Calendar(
        janela,
        selectmode='day',
        date_pattern='dd/mm/yyyy'
    )
    cal.pack(pady=20)

    btn = ttk.Button(janela, text="Lançar OS", command=pegar_data)
    btn.pack()

    janela.protocol("WM_DELETE_WINDOW", fechar)
    janela.mainloop()

    return data_escolhida[0] if data_escolhida else None


# ---------------- FUNÇÃO ITEM ----------------

def preencher_item(driver, wait, num, inicio, fim, desc):
    Select(wait.until(EC.presence_of_element_located(
        (By.NAME, f"tipo_tarefa_{num:03d}")
    ))).select_by_value("SUP")

    Select(wait.until(EC.presence_of_element_located(
        (By.NAME, f"modulo_{num:03d}")
    ))).select_by_value("COM")

    driver.execute_script(
        "arguments[0].value = arguments[1];",
        wait.until(EC.presence_of_element_located(
            (By.NAME, f"hora_inicial_{num:03d}")
        )),
        inicio
    )

    driver.execute_script(
        "arguments[0].value = arguments[1];",
        wait.until(EC.presence_of_element_located(
            (By.NAME, f"hora_final_{num:03d}")
        )),
        fim
    )

    driver.execute_script(
        "arguments[0].value = arguments[1];",
        wait.until(EC.presence_of_element_located(
            (By.NAME, f"descricao_{num:03d}")
        )),
        desc
    )


# ---------------- AUTOMAÇÃO ----------------

def rodar_automacao():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        # LOGIN
        driver.get("https://agenda.fabritech.com.br/login/")
        driver.maximize_window()

        wait.until(EC.presence_of_element_located((By.ID, "id_username"))).send_keys("PEDRO.MARTINS")
        wait.until(EC.presence_of_element_located((By.ID, "id_password"))).send_keys("123456@Pp")
        wait.until(EC.element_to_be_clickable((By.ID, "loginBtn"))).click()

        xpath_menu_agendas = "/html/body/main/div/aside/nav/div[1]/a"

        while True:
            entrada = escolher_data()

            if entrada is None:
                print("Encerrado pelo usuário.")
                break

            # Só clica se não estiver na tela agendas
            if "agendas" not in driver.current_url.lower():
                botao_agendas = wait.until(
                    EC.element_to_be_clickable((By.XPATH, xpath_menu_agendas))
                )
                driver.execute_script("arguments[0].click();", botao_agendas)

            hoje = datetime.strptime(entrada, "%d/%m/%Y").strftime("%Y-%m-%d")

            campo_data_inicio = wait.until(
                EC.presence_of_element_located((By.ID, "data_inicio"))
            )
            driver.execute_script(
                "arguments[0].value = arguments[1];",
                campo_data_inicio,
                hoje
            )

            campo_data_fim = wait.until(
                EC.presence_of_element_located((By.ID, "data_fim"))
            )
            driver.execute_script(
                "arguments[0].value = arguments[1];",
                campo_data_fim,
                hoje
            )

            # BUSCAR
            botao_buscar = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="form-filtro-agendas"]/div[2]/div[3]/button')
                )
            )
            driver.execute_script("arguments[0].click();", botao_buscar)

            # AÇÕES
            botao_acoes = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class,'btn-actions')]")
                )
            )
            driver.execute_script("arguments[0].click();", botao_acoes)

            # LANÇAR
            botao_lancar = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'dropdown-menu')]//button[@type='submit']")
                )
            )
            driver.execute_script("arguments[0].click();", botao_lancar)

            # HORÁRIOS
            driver.execute_script(
                "arguments[0].value = '08:00';",
                wait.until(EC.visibility_of_element_located((By.ID, "hora_inicio_os")))
            )

            driver.execute_script(
                "arguments[0].value = '18:00';",
                wait.until(EC.visibility_of_element_located((By.ID, "hora_fim_os")))
            )

            # PRESENCIAL / REMOTO
            campo_data = wait.until(
                EC.presence_of_element_located((By.NAME, "data_os"))
            )

            data_obj = datetime.strptime(
                campo_data.get_attribute("value"),
                "%d/%m/%Y"
            )

            tipo = "P" if data_obj.weekday() in (0, 3) else "R"

            Select(
                wait.until(
                    EC.presence_of_element_located(
                        (By.NAME, "tipo_atendimento_os")
                    )
                )
            ).select_by_value(tipo)

            # ITENS
            preencher_item(driver, wait, 1, "08:00", "12:00", "primeiro turno")

            wait.until(
                EC.element_to_be_clickable((By.ID, "btn-add-item"))
            ).click()

            preencher_item(driver, wait, 2, "12:00", "13:00", "Intervalo")

            wait.until(
                EC.element_to_be_clickable((By.ID, "btn-add-item"))
            ).click()

            preencher_item(driver, wait, 3, "13:00", "18:00", "segundo turno")

            # SALVAR
            botao_salvar = wait.until(
                EC.element_to_be_clickable((By.ID, "btn-salvar-lancamento"))
            )
            driver.execute_script("arguments[0].click();", botao_salvar)

            print(f"OS lançada para {entrada} | Tipo: {'Presencial' if tipo == 'P' else 'Remoto'}")

            # Espera salvar
            time.sleep(3)

            # Volta para agenda
            botao_agendas = wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath_menu_agendas))
            )
            driver.execute_script("arguments[0].click();", botao_agendas)

            time.sleep(2)

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    rodar_automacao()