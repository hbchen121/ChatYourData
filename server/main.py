import json
import time
import hashlib
import uvicorn
import asyncio
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Header, Form, Body
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta

from database.db_docs import Docs
from database.db_msg import Msg
from database.db_user import Users
from starlette.middleware.cors import CORSMiddleware
from ChatData.doc_util import Doc, set_api_key, get_api_key
from utils.structs import AddLink, Apikey, User
from models import UserModel, TokenData, UserWithHashModel
from utils.passwords import verify
import ipdb


app = FastAPI()
origins = ["http://127.0.0.1", "http://localhost:5173", "http://0.0.0.0:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])  # 允许跨域的headers，可以用来鉴别来源等作用。


app.mount("/static", StaticFiles(directory="data"), name="static")

# Auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.get("/all_docs")
async def handle():
    docs = Docs.get_all()
    # print("my_docs", docs)
    return {"data": docs}


@app.post("/my_docs")
async def handle(user: User):
    username = user.user.username
    docs = Docs.get_username_all(username)
    # print("my_docs", docs)
    return {"data": docs}


@app.delete("/del/{doc_id}")
async def handle(doc_id):
    Docs.del_by_doc_id(doc_id=doc_id)
    return {"data": "success"}


@app.post("/upload")
async def handle(background_task: BackgroundTasks, file: UploadFile, user: str = Header(...)):
    start = time.time()
    try:
        print(user)
        user = json.loads(user)
        username = user['username']
        size = file.size
        data = await file.read()
        doc_id = hashlib.md5((username + str(data)).encode('utf8')).hexdigest()
        filename = file.filename
        doc = Doc(doc_id=doc_id, filename=filename)
        await doc.save(content=data)
        Docs(uid=0, username=username, doc_id=doc_id, doc_name=filename, doc_type=file.content_type,
             size=size).insert()
        background_task.add_task(file_task, doc_id)
        return {"message": "success", 'time': time.time() - start, 'filename': filename}
    except Exception as e:
        print(e)
        return {"message": str(e), 'time': time.time() - start, 'filename': file.filename}


@app.post("/add_link")
async def handle(background_task: BackgroundTasks, link: AddLink):
    start = time.time()
    try:
        print(link)
        # username = link.user["username"]
        username = link.user.username
        doc_id = hashlib.md5((username + link.link).encode('utf8')).hexdigest()
        Docs(username=username, uid=0, doc_id=doc_id, doc_name=link.link, doc_type='web', size=0).insert()
        # print("add link task")
        # ipdb.set_trace()
        background_task.add_task(file_task, doc_id)
        # print("add link add task")
        return {"message": "success", 'time': time.time() - start}
    except Exception as e:
        print("add_link", e)
        # ipdb.set_trace()
        return {"message": str(e), 'time': time.time() - start}


@app.post("/add_apikey")
async def handle(api_key: Apikey):
    start = time.time()
    try:
        new_api_key = api_key.apikey
        username = api_key.user.username
        # username = api_key.user["username"]
        print("add api key", new_api_key)
        Users(userid=0, username=username).update(api_key=new_api_key)
        return {"message": "success", 'time': time.time() - start}
    except Exception as e:
        print("add api_key error", e)
        return {"message": str(e), 'time': time.time() - start}


# @app.get("/my_apikey")
# async def handle():
#     return {"data": "get_api_key()"}

@app.post("/my_apikey")
async def handle(user: User):
    username = user.user.username
    info = Users.get_by_username(username)
    # print("my api_key info", info)
    if info:
        return {"data": info["api_key"]}
    else:
        return {"data": "error"}


@app.get("/ask/{doc_id}")
async def handle(doc_id, question):
    asyncio.get_running_loop().set_debug(True)
    try:
        res = Docs.get_by_doc_id(doc_id=doc_id)
        doc = Doc(doc_id=doc_id, filename=res['doc_name'])
        Msg(uid=0, doc_id=doc_id, role="user", content=question).insert()
        res = doc.query(question=question)
        print(res.response)
        Msg(uid=0, doc_id=doc_id, role="chatdata", content=res).insert()
        return {"data": res, "doc_id": doc_id}
    except Exception as e:
        print(e)
        return {"message": str(e), "code": 500}


@app.get("/msg/{doc_id}")
async def handle(doc_id):
    res = Msg.get_by_doc_id(doc_id=doc_id, uid=0)
    return {"data": res, "doc_id": doc_id}


def file_task(doc_id: str):
    # ipdb.set_trace()
    # print(f"file_task {doc_id} start")
    res = Docs.get_by_doc_id(doc_id=doc_id)
    if res == None:
        print(f"file_task {doc_id} none")
        return

    # doc = Doc(doc_id=res['doc_id'], filename=res['doc_name'])
    # doc.build_txt(res['doc_type'])
    res['state'] = 1
    Docs(**res).update()

    # doc.build_index(res["doc_type"])
    res['state'] = 2
    # print(res)
    Docs(**res).update()
    # print(f"file_task {doc_id} done")


def get_user(username: str, password: str = ''):
    info = Users.get_by_username(username)
    if info is None:
        info = dict(userid=0, username=username, password=password)
        user = Users(**info).create()
    else:
        user = Users(**info)
    # if verify(user.password, password):
    #     return False
    return user


def authenticate_user(username: str, password: str):
    user = get_user(username, password)
    if not user:
        return False
    if not verify(user.password, password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserWithHashModel = Depends(get_current_user)):
    return current_user


@app.post("/token", response_model=TokenData)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = {
            "access_token": access_token,
            "token_type": "bearer",
            "username": user.username}
    return response

# Routes
@app.get("/")
# def read_root(current_user: UserModel = Depends(get_current_active_user)):
def read_root(current_user: UserModel = Depends()):
    return {"result": "Hello world"}


if __name__ == '__main__':
    print("start server...")
    uvicorn.run('main:app', host="0.0.0.0", reload=True, log_level="debug")
