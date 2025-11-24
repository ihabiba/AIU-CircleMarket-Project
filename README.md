# 🛒 CircleMarket – AIU Student Marketplace

**CircleMarket** is a web-based e-commerce platform developed to support small student-run businesses at **Albukhary International University (AIU)**.  
The platform connects buyers and sellers on campus, offering an organized and convenient way to browse, purchase, and manage products online.

> 🚀 Live Demo: https://aiu-circlemarket-project.onrender.com

---

## 📌 Project Overview

- 🎓 Developed as a **Software Engineering project**
- 🛍️ Designed to promote **student entrepreneurship**
- 🌱 Supports **SDG 9** – *Industry, Innovation & Infrastructure*

The system follows standard **requirements analysis**, **UML modeling**, **architecture design**, and **incremental development**, as documented in the full project report.

---

## 💡 Key Features

### 👤 Customer
- Browse products by category
- Search & filter items
- Add/remove items from cart
- View order summary
- Simple checkout (Cash on Delivery)

### 🛍️ Seller
- Create and manage a shop
- Add, update, and delete products
- View and confirm incoming orders

### 🔐 Admin
- Manage users, products, and orders
- Monitor marketplace activity

### 📱 UI/UX
- Fully responsive interface
- Clean, simple navigation

---

## 🧠 System Requirements 

### ✔️ Functional Requirements
- User authentication (buyer, seller, admin)
- Product browsing & searching
- Seller product management (CRUD)
- Cart and checkout flow
- Order processing workflow (Pending → Confirmed → Delivered)
- Admin monitoring dashboard

### ✔️ Non-Functional Requirements
- **Usability** – simple & intuitive for non-technical users  
- **Performance** – fast browsing & cart operations  
- **Security** – safe handling of user sessions and data  
- **Scalability** – supports increasing sellers/products  
- **Reliability** – consistent order tracking behavior  

---

## 🧩 System Design (UML & Architecture)

CircleMarket was modeled using standard UML diagrams (from the report).  
These should be included as images in the `docs/` folder (see section below).

### 📄 UML Models
- **Use Case Diagram**  
  Shows roles: *Customer*, *Seller*, *Admin* and their interactions.

- **Activity Diagram**  
  Demonstrates the full buyer journey:  
  *Browse → Cart → Checkout → Order → Delivery tracking*

- **Sequence Diagrams**  
  - Customer actions  
  - Seller actions  
  - Admin actions  

- **State Machine Diagrams**  
  For order processing and user behavior flows.

### 🏗️ Architecture Diagram
A **4-layer architecture** used in the report:
1. **User Interface Layer**  
2. **Application / Logic Layer**  
3. **Marketing / Analytics Layer**  
4. **Support Layer (Database + Deployment)**  

---

## 🛠️ Technologies Used

- **Backend**: Flask (Python), SQLite  
- **Frontend**: HTML5, CSS3, JavaScript  
- **Deployment**: Render  
- **Version Control**: Git & GitHub  

---
## 🖼️ UML & Architecture Diagrams

### 📘 Use Case Diagram
<img src="Diagrams/use%20case%20diagram.png" width="600">

### 🧭 Activity Diagram
<img src="Diagrams/activity%20diagram.png" width="600">

### 🔄 Sequence Diagram – Customer
<img src="Diagrams/customer%20sequence%20diagram.png" width="600">

### 🛍️ Sequence Diagram – Seller
<img src="Diagrams/seller%20sequence%20diagram.png" width="600">

### 🛡️ Sequence Diagram – Admin
<img src="Diagrams/admin%20sequence%20diagram.png" width="600">

### 🔁 State Machine – Customer
<img src="Diagrams/customer%20state%20diagram.png" width="600">

### 🔁 State Machine – Seller
<img src="Diagrams/seller%20state%20diagram.png" width="600">

### 🏗️ System Architecture
<img src="Diagrams/architecture%20design.png" width="600">
---

## 📂 Project Structure

```plaintext
├── app.py
├── templates/
│   └── HTML pages (Home, Shop, Cart, Orders, Admin)
├── static/
│   └── css, js, images
├── instance/
│   └── SQLite DB
├── requirements.txt
├── render.yaml
└── diagrams/              # UML diagrams & architecture
