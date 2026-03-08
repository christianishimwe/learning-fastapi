from fastapi import FastAPI, Request
import secrets
import os
import urllib.parse
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import httpx
from google.oauth2 import id_token
from google.auth.transport import requests
import redis
# Load environment variables from .env file
load_dotenv()


app = FastAPI()
# open a redis connection
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


SESSION_SECRET = os.getenv("SESSION_SECRET")

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    session_cookie="lala_session",
    https_only=False,
    same_site="lax",
)


@app.get("/")
async def root(request: Request):
    return JSONResponse({"message": "Hello World"}, status_code=200)

@app.get("/login/google")
async def login_google(request: Request):
    # generate a random state and nonce
    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)

    # generate a session id
    session_id = secrets.token_urlsafe(32)

    # store them in the user's session
    #request.session["oauth_state"] = state
    #request.session["oauth_nonce"] = nonce
    # store the session id in redis
    request.session["session_id"] = session_id
    # store the state and nonce in redis
    r.hset(f"session:{session_id}", mapping={"oauth_state": state, "oauth_nonce": nonce}, ex=600)
    # redirect to Google's OAuth consent screen
    params = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URL"),
        "response_type": "code",
        "scope": "openid email profile https://www.googleapis.com/auth/calendar.readonly",
        "state": state,
        "nonce": nonce
    }
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params))
    return RedirectResponse(google_auth_url)


# we will check state in this callback


@app.get("/auth/callback")
async def check_callback(request: Request, code: str = None, state: str = None):
    session_id = request.session.get("session_id")
    saved_state = r.hget(f"session:{session_id}", "oauth_state")
    if not session_id or not saved_state or saved_state != state:
        return JSONResponse({"error": "invalid session id", "session_id": session_id}, status_code=400)

    

    # now let's exchange code for tokens
    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URL"),
        "grant_type": "authorization_code"
    }


    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)

    #return JSONResponse(response.json())


    #  let's verify the id token
    tokens = response.json()
    raw_id_token = tokens.get("id_token")
    if not raw_id_token:
        return JSONResponse({"error": "no id token in response"}, status_code=400)

    idinfo = id_token.verify_oauth2_token(raw_id_token, requests.Request(), os.getenv("GOOGLE_CLIENT_ID"))

    if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
        return JSONResponse({"error": "Invalid issuer"}, status_code=401)

    if idinfo["aud"] != os.getenv("GOOGLE_CLIENT_ID"):
        return JSONResponse({"error": "Invalid audience"}, status_code=401)

    if idinfo["email_verified"] != True:
        return JSONResponse({"error": "Email not verified"}, status_code=401)

    if idinfo["azp"] != os.getenv("GOOGLE_CLIENT_ID"):
        return JSONResponse({"error": "Invalid client ID"}, status_code=401)

    # now let's verify the nonce
    saved_nonce = r.hget(f"session:{session_id}", "oauth_nonce")
    if not saved_nonce or saved_nonce != idinfo["nonce"]:
        return JSONResponse({"error": "Invalid nonce"}, status_code=401)
        

    # not add data to the session
    r.hset(f"session:{session_id}", mapping={
        "sub": idinfo["sub"],
        "email": idinfo["email"],
        "name": idinfo["name"],
        "picture": idinfo["picture"],
    })
    # store the access token separately
    r.set(f"access_token:{session_id}", tokens["access_token"], ex=3600)


@app.get("/calendar")
async def get_calendar(request: Request):
    session_id = request.session.get("session_id")
    # get the access token if it is still valid on redis
    access_token = r.get(f"access_token:{session_id}")
    
    if not access_token:
        return JSONResponse({"error": "Access token expired"}, status_code=401)

    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.googleapis.com/calendar/v3/calendars/primary/events", headers={"Authorization": f"Bearer {access_token}"})
        return JSONResponse(response.json())
