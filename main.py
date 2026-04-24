from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

# 🆕 IMPORTS DO CALENDÁRIO
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar


# =========================
# CALENDÁRIO DE DATA
# =========================
def escolher_data():
    data_escolhida = []

    def pegar_data():
        data_escolhida.append(cal.get_date())
        janela.destroy()

    janela = tk.Tk()
    janela.title("Selecione a Data")
    janela.geometry("300x300")

    cal = Calendar(janela, selectmode='day', date_pattern='dd/mm/yyyy')
    cal.pack(pady=20)

    btn = ttk.Button(janela, text="Confirmar", command=pegar_data)
    btn.pack()

    janela.mainloop()

    return data_escolhida[0]


# =========================
# FUNÇÃO REUTILIZÁVEL
# =========================
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


# =========================
# AUTOMAÇÃO PRINCIPAL
# =========================
def rodar_automacao():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        wait = WebDriverWait(driver, 15)

        # LOGIN
        driver.get("https://agenda.fabritech.com.br/login/")
        driver.maximize_window()

        wait.until(EC.presence_of_element_located((By.ID, "id_username"))).send_keys("MATHEUS.FELIPE")
        wait.until(EC.presence_of_element_located((By.ID, "id_password"))).send_keys("Mv09112019@")
        wait.until(EC.element_to_be_clickable((By.ID, "loginBtn"))).click()

        # MENU
        xpath_menu_agendas = "/html/body/main/div/aside/nav/div[1]/a"
        botao_agendas = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_menu_agendas)))
        driver.execute_script("arguments[0].click();", botao_agendas)

        # =========================
        # 🆕 FILTRO DE DATA (COM CALENDÁRIO)
        # =========================
        entrada = escolher_data()

        data_obj = datetime.strptime(entrada, "%d/%m/%Y")
        hoje = data_obj.strftime("%Y-%m-%d")

        campo_data_inicio = wait.until(EC.presence_of_element_located((By.ID, "data_inicio")))
        driver.execute_script("arguments[0].value = arguments[1];", campo_data_inicio, hoje)
        campo_data_inicio.send_keys("\t")

        campo_data_fim = wait.until(EC.presence_of_element_located((By.ID, "data_fim")))
        driver.execute_script("arguments[0].value = arguments[1];", campo_data_fim, hoje)
        campo_data_fim.send_keys("\t")

        time.sleep(1)

        # BUSCAR
        xpath_buscar = '//*[@id="form-filtro-agendas"]/div[2]/div[3]/button'
        botao_buscar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_buscar)))
        driver.execute_script("arguments[0].click();", botao_buscar)

        # AÇÕES
        botao_acoes = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'btn-actions')]")
        ))
        driver.execute_script("arguments[0].click();", botao_acoes)

        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'dropdown-menu')]")
        ))

        # LANÇAR OS
        botao_lancar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'dropdown-menu')]//button[@type='submit']")
        ))
        driver.execute_script("arguments[0].click();", botao_lancar)

        # HORAS OS
        driver.execute_script("arguments[0].value = '08:00';",
            wait.until(EC.visibility_of_element_located((By.ID, "hora_inicio_os")))
        )

        driver.execute_script("arguments[0].value = '18:00';",
            wait.until(EC.visibility_of_element_located((By.ID, "hora_fim_os")))
        )

        # TIPO ATENDIMENTO
        campo_data = wait.until(EC.presence_of_element_located((By.NAME, "data_os")))
        data_obj = datetime.strptime(campo_data.get_attribute("value"), "%d/%m/%Y")

        tipo = "P" if data_obj.weekday() in (0, 3) else "R"

        Select(wait.until(
            EC.presence_of_element_located((By.NAME, "tipo_atendimento_os"))
        )).select_by_value(tipo)

        # ITENS
        preencher_item(driver, wait, 1, "08:00", "12:00", "primeiro turno")

        botao_add_item = wait.until(EC.element_to_be_clickable((By.ID, "btn-add-item")))
        driver.execute_script("arguments[0].click();", botao_add_item)

        preencher_item(driver, wait, 2, "12:00", "13:00", "Intervalo")

        botao_add_item_2 = wait.until(EC.element_to_be_clickable((By.ID, "btn-add-item")))
        driver.execute_script("arguments[0].click();", botao_add_item_2)

        preencher_item(driver, wait, 3, "13:00", "18:00", "segundo turno")

        # SALVAR
        botao_salvar = wait.until(
            EC.element_to_be_clickable((By.ID, "btn-salvar-lancamento"))
        )
        driver.execute_script("arguments[0].click();", botao_salvar)
    
        botao_agendas = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_menu_agendas)))
        driver.execute_script("arguments[0].click();", botao_agendas)
    
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    rodar_automacao()