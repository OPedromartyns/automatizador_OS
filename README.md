# 📌 Manual de Configuração da Automação de Lançamento de OS

## 📖 Objetivo

Esta automação realiza automaticamente o lançamento de Ordens de Serviço (OS) no sistema Agenda.

Ela foi desenvolvida para reduzir o preenchimento manual e permitir ajustes simples por futuros analistas.

As alterações permitidas são:

- Alteração de usuário
- Alteração de senha
- Alteração dos dias presenciais
- Geração de novo executável

---

# 🛠 Requisitos

Antes de utilizar a automação, é necessário possuir:

- Python instalado
- Visual Studio Code
- Google Chrome
- Conexão com internet

---

# 📥 Instalação das Dependências

Abra o terminal no VS Code e execute:

```bash
pip install selenium webdriver-manager tkcalendar pyinstaller
```

---

# 🔐 Alteração de Usuário e Senha

Sempre que houver troca de credenciais, localizar o trecho:

```python
wait.until(EC.presence_of_element_located((By.ID, "id_username"))).send_keys("USUARIO")
wait.until(EC.presence_of_element_located((By.ID, "id_password"))).send_keys("SENHA")
```

## Alterar usuário

Substituir:

```python
"USUARIO"
```

Exemplo:

```python
"joao.silva"
```

---

## Alterar senha

Substituir:

```python
"SENHA"
```

Exemplo:

```python
"Senha@123"
```

---

## ⚠️ Cuidados

**Nunca remover:**

- Aspas
- Parênteses
- `.send_keys`

✅ Correto

```python
send_keys("joao.silva")
```

❌ Incorreto

```python
send_keys(joao.silva)
```

---

# 📅 Alteração dos Dias Presenciais

Localizar o trecho:

```python
tipo = "P" if data_obj.weekday() in (0, 3) else "R"
```

---

## Tabela de dias

| Dia | Número |
|-----|--------|
| Segunda | 0 |
| Terça | 1 |
| Quarta | 2 |
| Quinta | 3 |
| Sexta | 4 |

---

## Configuração atual

Presencial em:

- Segunda
- Quinta

Código:

```python
(0, 3)
```

---

## Exemplos

### Presencial terça e quinta

```python
tipo = "P" if data_obj.weekday() in (1, 3) else "R"
```

---

### Presencial somente quarta

```python
tipo = "P" if data_obj.weekday() == 2 else "R"
```

---

### Presencial segunda, quarta e sexta

```python
tipo = "P" if data_obj.weekday() in (0, 2, 4) else "R"
```

---



## Função de preenchimento

```python
preencher_item()
```

---

## Loop principal

```python
while True:
```

---

## Seletores

```python
By.ID
By.XPATH
By.NAME
```

---

# ▶️ Executar no VS Code

No terminal do VS Code:

```bash
python main.py
```

---

# ⚙️ Gerar Executável (.exe)

Sempre que houver alteração no código, é necessário gerar um novo executável.

---

## Passo 1 — Abrir terminal no VS Code

No menu superior:

**Terminal → Novo Terminal**

---

## Passo 2 — Navegar até a pasta do projeto

Exemplo:

```bash
cd C:\Users\SeuUsuario\Documents\automatizador_OS
```

---

## Passo 3 — Gerar o executável

Executar:

```bash
python -m PyInstaller --onefile --noconsole --collect-all selenium --hidden-import=tkcalendar main.py
```

---

## Passo 4 — Localizar o executável

Após finalizar, o arquivo será criado em:

```bash
dist/
```

Exemplo:

```bash
dist/main.exe
```

---

# 🔄 Sempre que alterar

Após mudar:

- Usuário
- Senha
- Dias presenciais

É obrigatório gerar novamente o executável.

---

# ⚠️ Em caso de erro na geração

Se aparecer erro de dependência, executar:

```bash
pip install --upgrade pyinstaller
```

Se persistir:

```bash
pip install selenium webdriver-manager tkcalendar pyinstaller
```

---

# 🧪 Teste após gerar

Executar o `.exe`

Validar:

- Login realizado
- Calendário abre
- Busca agenda
- Lançamento ocorre normalmente

---

# 📞 Suporte Técnico

Caso a automação pare de funcionar sem alterações realizadas, o problema pode estar relacionado a:

- Mudança no sistema Agenda
- Alteração de campos HTML
- Mudança de seletores Selenium

Nestes casos será necessária manutenção técnica no código.

---🔧 Melhorias Futuras

Sugestões de evolução:

Tela para digitação de login/senha
Arquivo de configuração
Logs em arquivo
Interface gráfica completa
Geração de executável