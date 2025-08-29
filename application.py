from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from openai import OpenAI

app = FastAPI()
application = app  # Elastic Beanstalk espera 'application'

# Monta pasta estática
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/analisar/")
async def analisar(file: UploadFile = None, texto: str = Form(...)):
    text = texto
    if file:
        content = await file.read()
        try:
            text = content.decode("utf-8")
        except:
            return JSONResponse(content={"erro": "Erro ao ler arquivo. Use .txt simples."}, status_code=400)
    if not text.strip():
        return JSONResponse(content={"erro": "Texto vazio."}, status_code=400)

    try:
        prompt = f"Classifique o seguinte email como PRODUTIVO ou IMPRODUTIVO:\n{text}"
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"Você é um avaliador de emails."},
                {"role":"user","content":prompt}
            ],
            max_tokens=100,
            temperature=0
        )
        resultado = resposta.choices[0].message.content.strip()
        if "produtivo" in resultado.lower():
            categoria = "Produtivo"
        else:
            categoria = "Improdutivo"

        return {"category": categoria, "response": resultado}
    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)
