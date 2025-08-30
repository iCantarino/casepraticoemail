from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from io import BytesIO
from openai import OpenAI
from PyPDF2 import PdfReader  # pip install PyPDF2

# Instância do FastAPI
app = FastAPI()
application = app  # Elastic Beanstalk espera "application"

# Monta pasta estática (se existir)
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Cliente OpenAI (defina OPENAI_API_KEY no ambiente)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Página inicial
@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse("<h1>templates/index.html não encontrado</h1>", status_code=404)

# Healthcheck
@app.get("/health")
def health():
    return {"status": "ok"}

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts).strip()

@app.post("/analisar/")
async def analisar(file: UploadFile | None = None, texto: str = Form("")):
    text = (texto or "").strip()

    if file is not None:
        filename = (file.filename or "").lower()
        content = await file.read()

        if filename.endswith(".txt"):
            try:
                text = content.decode("utf-8", errors="replace")
            except Exception:
                return JSONResponse({"erro": "Erro ao ler .txt. Use UTF-8."}, status_code=400)
        elif filename.endswith(".pdf"):
            try:
                text = extract_text_from_pdf_bytes(content)
            except Exception as e:
                return JSONResponse({"erro": f"Erro ao processar PDF: {e}"}, status_code=400)
        else:
            return JSONResponse({"erro": "Formato inválido. Envie .txt ou .pdf."}, status_code=400)

    if not text.strip():
        return JSONResponse({"erro": "Texto vazio."}, status_code=400)

    try:
        prompt = (
            "Você é um avaliador de emails. "
            "Classifique como 'PRODUTIVO' ou 'IMPRODUTIVO' e sugira uma resposta curta e educada. "
            "Responda no formato:\n"
            "Categoria: <PRODUTIVO|IMPRODUTIVO>\n"
            "Resposta: <texto>\n\n"
            f"Email:\n{text}"
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente criterioso e conciso."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0
        )
        raw = resp.choices[0].message.content.strip()

        # Classificação robusta (evita 'produtivo' dentro de 'improdutivo')
        low = raw.lower()
        if "improdutivo" in low:
            categoria = "Improdutivo"
        elif "produtivo" in low:
            categoria = "Produtivo"
        else:
            categoria = "Indefinido"

        # Tenta extrair só o trecho após "Resposta:"
        suggested = raw
        for marker in ["resposta:", "resposta sugerida:", "resposta -", "resposta "]:
            idx = low.find(marker)
            if idx != -1:
                suggested = raw[idx + len(marker):].strip()
                break

        return {"category": categoria, "response": suggested, "raw": raw}
    except Exception as e:
        return JSONResponse({"erro": str(e)}, status_code=500)
