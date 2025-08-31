# Case Pratico Email
<br>
Para rodar localmente:
<br>
Passo 1: Pré-requisitos<br>
1 - Ter o Python 3.9+ instalado<br>
2 - Instalar o pip (gerenciador de pacotes do Python)<br>
3 - Ter uma chave válida da API da OpenAI<br>
<br>
Passo 2: Clonar ou baixar o projeto<br>
1 - Caso vá clonar, clone o repositório usando o terminal com: git clone https://github.com/iCantarino/casepraticoemail <br>
2 - Também é possivel baixar os arquivos pela página do repositório <br>
<br>
Passo 3: Criar ambiente virtual<br>
1 - Para isolar as dependências, python -m venv venv no terminal<br>
2 - Ativar no Windows CMD com venv\Scripts\activate ou Linux/Max com source venv/bin/activate<br>
<br>
Passo 4: Instalar dependências<br>
1 - pip install -r requirements.txt<br>
2 - No requirements temos: <br>
fastapi<br>
uvicorn[standard]<br>
gunicorn<br>
openai<br>
python-multipart<br>
PyPDF2<br>
<br>
Passo 5: Criar variável de ambiente da OpenAI para sua chave<br>
1 - No CMD execute setx OPENAI_API_KEY "sua_chave"<br>
2 - Linux/Mac: export OPENAI_API_KEY "sua_chave"<br>
(sem aspas)<br>
3 - Pegue sua chave API no site da OpenAI, necessário dizer que sem uma quantia já aplicada na sua conta OpenAI, não vai funcionar e receberá mensagem de fundos insuficientes.<br>
<br>
Passo 6: Rodar localmente<br>
1 - Execute uvicorn application:application --reload<br>
<br>
Paasso 7: Acessar no navegador<br>
1 - Abra: http://127.0.0.1:8000 <br>
