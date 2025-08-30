from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from openai import OpenAI

# Instância do FastAPI
app = FastAPI()
application = app  # Elastic Beanstalk espera que a app principal se chame "application"

# Monta pasta estática (se existir)
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Página inicial
@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse("<h1>Index.html não encontrado na pasta templates/</h1>", status_code=404)

# Endpoint para testar se a API está rodando
@app.get("/health")
def health():
    return {"status": "ok"}

# Endpoint de análise
@app.post("/analisar/")
async def analisar(file: UploadFile = None, texto: str = Form(...)):
    text = texto
    if file:
        content = await file.read()
        try:
            text = content.decode("utf-8")
        except Exception:
            return JSONResponse(content={"erro": "Erro ao ler arquivo. Use .txt simples."}, status_code=400)

    if not text.strip():
        return JSONResponse(content={"erro": "Texto vazio."}, status_code=400)

    try:
        prompt = f"Classifique o seguinte email como PRODUTIVO ou IMPRODUTIVO:\n{text}"
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um avaliador de emails."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0
        )
        resultado = resposta.choices[0].message.content.strip()

        # Normaliza categoria
        if "produtivo" in resultado.lower():
            categoria = "Produtivo"
        else:
            categoria = "Improdutivo"

        return {"category": categoria, "response": resultado}

    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)
