# 1. Налаштування логування має бути НАЙПЕРШИМ
import logging
logging.basicConfig(
    level=logging.INFO,
    filename="smart_app.log",
    filemode="a", # "a" - дописувати, "w" - переписувати
    format="%(asctime)s - %(processName)s - %(name)s - %(levelname)s - %(message)s",
    force=True
)

# 2. Тепер решта імпортів
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from controller.app_controller import AppController
import uvicorn

app = FastAPI(title="SmartApp IoT System")
templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

controller = AppController() # Ініціалізуємо контролер

# --- Допоміжна функція ---
def get_dashboard_response(request: Request, updated_device=None):
    status = controller.get_all_status()
    context = {"request": request, "devices": status}
    if updated_device:
        context["updated_device"] = updated_device
    return templates.TemplateResponse("index.html", context)


# 3. ОСЬ ВІН, ВІДСУТНІЙ ЕНДПОІНТ!
@app.get("/", response_class=HTMLResponse) # Ендпоінт для головної сторінки
async def read_root(request: Request):
    """
    Показати головний дашборд з усіма статусами.
    """
    # Викликаємо синхронну функцію
    return get_dashboard_response(request)
# --- Кінець відсутнього блоку ---


@app.post("/toggle_speaker")
async def toggle_speaker(request: Request):
    controller.toggle_device("speaker_001")
    return RedirectResponse(url="/", status_code=303)

@app.post("/toggle_light")
async def toggle_light(request: Request):
    controller.toggle_device("light_001")
    return RedirectResponse(url="/", status_code=303)

@app.post("/set_volume")
async def set_volume(request: Request, volume: int = Form(...)):
    controller.set_device_value("speaker_001", "set_volume", volume)
    return RedirectResponse(url="/", status_code=303)

@app.post("/set_brightness")
async def set_brightness(request: Request, brightness: int = Form(...)):
    controller.set_device_value("light_001", "set_brightness", brightness)
    return RedirectResponse(url="/", status_code=303)

@app.post("/toggle_curtains")
async def toggle_curtains(request: Request):
    controller.toggle_device("curtains_001")
    return RedirectResponse(url="/", status_code=303)

@app.post("/set_position")
async def set_position(request: Request, position: int = Form(...)):
    controller.set_device_value("curtains_001", "position", position)
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__": 
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)