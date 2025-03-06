from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.scraping.scraper import fetch_alternative_sources

from src.nlp.bias_analysis import analyze_bias
from src.nlp.text_rewriter import rewrite_text

app = FastAPI()

class ArticleRequest(BaseModel):
    text: str

@app.post("/analyze-bias")
async def analyze_bias_api(request: ArticleRequest):
    try:
        alternative_articles = await fetch_alternative_sources(request.text)
        bias_score, highlights, _ = analyze_bias(request.text, alternative_articles)
        rewritten_text, redlined_text = rewrite_text(request.text, alternative_articles)

        return {
            "bias_score": bias_score,
            "highlights": highlights,
            "rewritten_text": rewritten_text,
            "redlined_text": redlined_text,
            "alternative_sources": alternative_articles
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
