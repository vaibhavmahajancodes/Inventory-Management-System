# 📦 Inventory Management System

A Role-Based Inventory Management System built with **FastAPI**, **SQLite**, and **JWT Authentication** for secure product and stock management.

## ✨ Features

* 📋 Product Management (Add & View Products)
* 📦 Stock Tracking
* ⚠️ Low Stock Alerts
* 🔐 JWT-Based Authentication
* 👥 Role-Based Access Control (Admin/User)
* 📊 Sales Reports (Basic Structure)
* 📚 Interactive API Documentation (Swagger UI)

## 🚀 Run Project

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## 🌐 Access API

* 🏠 API: `http://127.0.0.1:8000`
* 📖 Swagger Docs: `http://127.0.0.1:8000/docs`

## 🔗 API Endpoints

### 🔐 Authentication

* `POST /register/` — Register User
* `POST /login/` — Login & Generate JWT Token

### 📦 Product Management

* `POST /product/` — Add Product (Admin Only)
* `GET /products/` — View All Products
* `GET /low-stock/` — View Low Stock Products

