from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from scrapper import scrape_flipkart
import os
import db

app = FastAPI(title="Flipkart Scraper UI")

# Ensure directories exist
os.makedirs("frontend", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Templates
templates = Jinja2Templates(directory="frontend")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/scrape/flipkart")
def run_scraper(query: str = "phone", budget: int = 15000):
    try:
        print(f"Scraping for {query} under {budget}...")
        data = scrape_flipkart(query, budget)
        return {"count": len(data), "products": data}
    except Exception as e:
        print(f"Error scraping: {e}")
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.on_event("startup")
def startup():
    print("Initializing DB...")
    db.init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



