# Case Prático Email

## Introdução
Este projeto é um desafio prático de classificação de e-mails com resposta automatizada.  
Ele utiliza FastAPI como backend e a API da OpenAI para realizar a classificação e sugerir respostas.

---

## Passo a Passo para rodar localmente

### Passo 1: Pré-requisitos
1. Ter o **Python 3.9+** instalado  
2. Ter o **pip** (gerenciador de pacotes do Python) instalado  
3. Possuir uma **chave válida da API da OpenAI**  

---

### Passo 2: Clonar ou baixar o projeto
- Clonar o repositório via terminal:  
git clone https://github.com/iCantarino/casepraticoemail
- Ou baixar os arquivos diretamente pela página do repositório no GitHub.

---

###  Passo 3: Criar ambiente virtual
-No terminal, dentro da pasta do projeto, execute:  
python -m venv venv
  
-Ativar o ambiente virtual:  
- **Windows (CMD):**
venv\Scriptsctivate
- **Linux/Mac:**
source venv/bin/activate


---

### Passo 4: Instalar dependências
Com o ambiente virtual ativado, rode:  
pip install -r requirements.txt

Dependências principais:  
- fastapi  
- uvicorn[standard]  
- gunicorn  
- openai  
- python-multipart  
- PyPDF2  

---

### Passo 5: Configurar variável de ambiente da OpenAI
Defina sua chave de API:  

- **Windows (CMD):**
setx OPENAI_API_KEY "sua_chave"

- **Linux/Mac:**
export OPENAI_API_KEY="sua_chave"

Observação: É necessário ter créditos ativos na conta OpenAI. Caso contrário, retornará erro de fundos insuficientes.

---

### Passo 6: Rodar localmente
No terminal, dentro da pasta do projeto, rode:  
uvicorn application:application --reload

---

### Passo 7: Acessar no navegador
Abra no navegador:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Observações
- O sistema aceita upload de arquivos **.txt** e **.pdf**.  
- Em caso de erro na ativação do ambiente no Windows PowerShell, rode antes:  
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

---

## Conclusão
Este projeto demonstra uma integração prática de **IA + Web** para classificação automática de e-mails, com possibilidade de expansão para outros tipos de documentos.
