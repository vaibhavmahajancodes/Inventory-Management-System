from fastapi import FastAPI, Depends, HTTPException
from database import init_db, get_connection
from schemas import Product, UserCreate
from utils import check_low_stock
from auth import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import sqlite3
from jose import jwt, JWTError

app = FastAPI(title="Inventory Management System")

init_db()

# ADD THIS HERE (/)
@app.get("/")
def home():
    return {"message": "API is running"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ---------------- AUTH ----------------------------------------------------------

@app.post("/register/")
def register(user: UserCreate):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (user.username, hash_password(user.password), user.role)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": "User registered successfully"}


@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=?", (form_data.username,))
    user = cur.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user[1],
        "role": user[3]
    })

    return {"access_token": token, "token_type": "bearer"}


# ---------------- AUTH DEPENDENCY ----------------------------

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def admin_required(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user


# ---------------- PRODUCTS -------------------------------------------

@app.post("/product/")
def add_product(product: Product, user=Depends(admin_required)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO products (name, quantity, price, threshold) VALUES (?, ?, ?, ?)",
        (product.name, product.quantity, product.price, product.threshold)
    )

    conn.commit()
    return {"message": "Product added successfully"}


@app.get("/products/")
def get_products(user=Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

    return {"products": product}


@app.get("/low-stock/")
def low_stock(user=Depends(get_current_user)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

    return {"low_stock": check_low_stock(products)}
