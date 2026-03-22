# 🛵 FreshMart-Grocery Delivery APP

A full-featured **FastAPI-based Grocery Delivery Backend System** built as part of a FastAPI Internship Final Project.
This project simulates a real-world quick-commerce platform like **Blinkit / Zepto**, covering item management, cart workflow, order processing, and advanced APIs.

---

## 🚀 Features

### 🥦 Item Management

* View all grocery items
* Get item by ID
* Category-wise summary
* Add new items (with duplicate check)
* Update item price and stock
* Delete item (with active order protection)

---

### 🛒 Cart System

* Add items to cart
* Merge quantities automatically
* View cart with subtotal & grand total
* Remove items from cart

---

### 📦 Order System

* Place single orders
* Bulk order discount (8%)
* Delivery charges:

  * Morning → ₹40
  * Evening → ₹60
* Checkout system (cart → multiple orders)
* Prevent ordering out-of-stock items

---

### 🔍 Advanced APIs

* Filter items (category, price, unit, stock)
* Search items (name + category, case-insensitive)
* Sort items (price, name, category)
* Pagination for items and orders
* Combined browse API (search + filter + sort + pagination)

---

## 🧠 Concepts Covered

This project covers all FastAPI fundamentals:

* GET, POST, PUT, DELETE endpoints
* Pydantic models & validation
* Helper functions (clean architecture)
* CRUD operations
* Multi-step workflow (Cart → Checkout)
* Query parameters & filtering
* Search, sorting, pagination
* Error handling with HTTPException

---

## ⚙️ Tech Stack

* ⚡ FastAPI
* 🐍 Python 3
* 📦 Pydantic
* 🧪 Swagger UI (for API testing)

---

## ▶️ How to Run the Project

### 1. Install dependencies

```bash
pip install fastapi uvicorn
```

### 2. Run server

```bash
uvicorn main:app --reload
```

### 3. Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 📌 API Highlights

### 🔹 Sample Endpoints

| Method | Endpoint       | Description    |
| ------ | -------------- | -------------- |
| GET    | /items         | Get all items  |
| GET    | /items/{id}    | Get item by ID |
| POST   | /items         | Add new item   |
| PUT    | /items/{id}    | Update item    |
| DELETE | /items/{id}    | Delete item    |
| POST   | /cart/add      | Add to cart    |
| GET    | /cart          | View cart      |
| POST   | /cart/checkout | Checkout       |
| GET    | /items/search  | Search items   |
| GET    | /items/sort    | Sort items     |
| GET    | /items/page    | Pagination     |
| GET    | /items/browse  | Combined API   |

---

## 🧪 Example Use Case

1. Add items to cart
2. View cart
3. Checkout
4. Orders are created per item
5. Cart is cleared automatically

---

## 💡 Future Improvements

* Database integration (MongoDB / PostgreSQL)
* Authentication (JWT)
* Single-order checkout system (real-world model)
* AI-based recommendations
* Inventory prediction system

---

## 🧑‍💻 Author

**Rahul Dhumal**


---

## ⭐ Project Summary

This project demonstrates **real-world backend development skills** including API design, workflow handling, and scalable architecture using FastAPI.

---
