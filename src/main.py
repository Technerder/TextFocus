import nltk
import asyncio
import aiohttp
import uvicorn
import newspaper

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse


app = FastAPI()
app.mount('/static', StaticFiles(directory='frontend/static'), name='static')
templates = Jinja2Templates(directory='frontend/templates')
nltk.download('punkt')


@app.get("/")
async def serve_index():
    return FileResponse('frontend/index.html')


@app.get("/focus", response_class=HTMLResponse)
async def serve_page(request: Request, url: str):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                html = await response.read()
                page = newspaper.Article(url)
                page.set_html(html)
                page.parse()
                page.nlp()
                return templates.TemplateResponse('page.html', {
                    'request': request,
                    'title': page.title,
                    'authors': page.authors,
                    'publish_date': page.publish_date,
                    'text': page.text,
                    'image': page.top_image,
                    'keywords': page.keywords,
                    'summary': page.summary
                })
    except Exception as e:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'error': str(e)
        })


if __name__ == '__main__':
    config = uvicorn.Config(app=app, reload=True, host='0.0.0.0', port=80, debug=False)
    server = uvicorn.Server(config=config)
    asyncio.run(server.serve())
