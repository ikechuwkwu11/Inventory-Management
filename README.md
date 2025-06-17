# 📦 Flask Inventory Management API
Flask Inventory Management API is a RESTful backend application designed to handle a basic inventory system. Built with Flask and SQLAlchemy, this API provides endpoints for managing users, categories, suppliers, and items — with support for image uploads and secure authentication.

## 🚀 Features
- User Authentication
- User Registration
- Login with session management
- Logout
- Passwords are securely hashed using Werkzeug

## 📁 Inventory Management
- Categories
- Create, view, update, delete
- Suppliers
- Create, view, update, delete
- Items
- Create, view, update, delete
- Image Upload
- Upload category images (e.g., .jpg, .png)

All responses follow a clean JSON-based API format

## 🧰 Tech Stack
| Layer             | Technology                              |
| ----------------- | --------------------------------------- |
| Language          | Python 3.x                              |
| Backend Framework | Flask                                   |
| ORM               | SQLAlchemy                              |
| Authentication    | Flask-Login + Werkzeug Security         |
| Database          | SQLite (default, easily swappable)      |
| File Uploads      | Flask + `secure_filename` from Werkzeug |
| Response Format   | JSON                                    |


## 🔐 Authentication
- Use /register to create an account and /login to authenticate. Authentication is session-based via Flask-Login.
- You must be logged in to access protected endpoints (e.g., /items, /categories, /suppliers).

## 📦 Example API Endpoints
- POST /register — Register new user
- POST /login — Login
- POST /logout — Logout
- GET /categories — List categories
- POST /categories — Add category
- POST /categories/upload — Upload image for category
- GET /suppliers — List all suppliers
- GET /items — List all items
- POST /items — Create new item

All routes return JSON responses for easy integration with frontend or third-party clients.

## ✅ To-Do / Future Improvements
- Add token-based authentication (JWT)
- Pagination and filtering support
- Swagger/OpenAPI documentation
- Role-based permissions (Admin/User)
- Deploy to cloud (Render, Railway, etc.)
