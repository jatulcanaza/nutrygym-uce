from fastapi import FastAPI, Request, HTTPException
import httpx
import os

app = FastAPI(title="NutriGym API Gateway")

AUTH_SERVICE = "http://auth-service:3001"
PROFILE_SERVICE = "http://user-profile-service:3002"
AUTHZ_SERVICE = "http://role_permission-service:3003"
NUTRITION_SERVICE = "http://nutrition-form-service:3004"


async def proxy(request: Request, url: str):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method,
            url,
            headers=dict(request.headers),
            content=await request.body()
        )
    return response.json()


@app.post("/auth/login")
async def login(request: Request):
    return await proxy(request, f"{AUTH_SERVICE}/auth/login")


@app.get("/auth/me")
async def me(request: Request):
    return await proxy(request, f"{AUTH_SERVICE}/auth/me")


@app.get("/authorize/my-role")
async def my_role(request: Request):
    return await proxy(request, f"{AUTHZ_SERVICE}/authorize/my-role")


@app.post("/nutrition-form")
async def nutrition_form(request: Request):
    return await proxy(request, f"{NUTRITION_SERVICE}/nutrition-form")


@app.get("/health")
def health():
    return {"status": "gateway ok"}
