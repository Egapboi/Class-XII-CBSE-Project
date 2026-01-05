
# TrackIt — Order Tracking & Management System

**TrackIt** is a **console-based Python application** developed as a **Class XII CBSE Computer Science project**.
It simulates a real-world **e-commerce order tracking system** with support for **users, admins, and delivery personnel**, backed by a **MariaDB/MySQL database** and a rich terminal UI.

---

## Project Objective

The objective of this project is to:

* Demonstrate **database connectivity using Python**
* Implement **role-based access control**
* Simulate **order placement, tracking, and delivery management**
* Apply **real-world logic** such as delivery assignment, order status updates, and analytics

---

## User Roles

### Normal User

* Sign up / Login
* Edit profile (name, city, state, password)
* Browse and search items
* Place orders
* View order status (live simulated tracking)
* View personal order history

### Admin

* Add / remove / edit:

  * Users
  * Delivery men
  * Items
  * Orders
* Assign / unassign delivery men
* View:

  * All users
  * All orders
  * Delivery men details
* View **project statistics**:

  * Total users
  * Total orders
  * Revenue
  * City-wise order distribution

### Delivery Man

* Secure login
* View assigned orders
* See delivery location and expected delivery date
* Auto-refresh order list

---

## Key Features

* **Rich terminal UI** using the `rich` library
* Email & password authentication
* Email format validation using regex
* Realistic delivery status simulation
* Capacity-based delivery man assignment
* Admin analytics dashboard
* Modular, function-based design
* Environment-variable–based configuration (`.env`)

---

## Technologies Used

| Technology      | Purpose                      |
| --------------- | ---------------------------- |
| Python 3        | Core programming language    |
| MariaDB / MySQL | Backend database             |
| `rich`          | Terminal UI (tables, colors) |
| `datetime`      | Date & delivery handling     |
| `random`        | Delivery simulation          |
| `re`            | Email validation             |
| `python-dotenv` | Environment variable loading |

---

## Database Schema

The project uses a database named **`TrackIt`** with the following tables:

* `admin_data`
* `normal_user_data`
* `delivery_men_data`
* `order_items`
* `orders`

The full schema is provided in **`schema.sql`**.

---

## Setup Instructions

### 1️⃣ Install Dependencies

```bash
pip install rich mariadb python-dotenv
```

---

### 2️⃣ Configure Environment Variables

This project uses environment variables for database configuration.

1. Copy the example file:

```bash
cp .env.example .env
```

2. Edit `.env` and **set your database password**:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=TrackIt
```

---

### 3️⃣ Create the Database & Tables

Run the provided schema file:(Inside the mariaDB shell)

```bash
create database TrackIt;
```

```bash
mysql -u root -p TrackIt < schema.sql
```

(or use `mariadb` if applicable)

This will:

* Create all required tables
* Insert predefined admin and item data

---

### 4️⃣ Run the Program

```bash
python ProjectSunilGroup-1.py
```

---

## How It Works

1. User selects role (User / Admin / Delivery Man)
2. Authenticates via email & password
3. Role-specific menu is displayed
4. Database operations are performed in real time
5. Order delivery status updates dynamically based on date logic

---

## Delivery Status Logic

Delivery status is automatically generated using the expected delivery date:

* In Warehouse
* Shipping
* Out for Delivery
* Delivered

This simulates a **real e-commerce logistics pipeline**.

---

## Exit Shortcut

At **any input prompt**, type:

```
-1
```

to safely exit or return to the main menu.

---

## Project Details

* **Project Name:** TrackIt
* **Language:** Python
* **Board:** CBSE
* **Class:** XII
* **Academic Year:** 2025–26

---

## Disclaimer

This project is developed **strictly for educational purposes** as part of a CBSE practical examination.
Passwords are stored in plain text for simplicity and learning purposes (not recommended for real-world systems).

---

## License

This project is licensed under the **MIT License**.
See the `LICENSE` file for details.

---
