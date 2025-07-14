# 🚗 Nexlot Vehicle Parking App

A full-stack web application to manage vehicle parking using Flask, Bootstrap, and SQLite. Built as part of the MAD-I course project at IIT Madras.

---

## 📌 Features

- 👤 User registration & login
- 🅿️ Book and release parking spots
- 📊 Admin dashboard with stats and visualizations
- 📍 Search parking lots by location or pin code
- 🔐 Role-based access (User/Admin)

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, Bootstrap, Jinja2
- **Backend:** Python (Flask)
- **Database:** SQLite
- **Other:** Flask-SQLAlchemy, Chart.js

---
## 🗂️ Data Models

The application uses SQLAlchemy ORM to define its core data models and their relationships:

### User

- Represents a user of the system (either regular user or admin).
- **Fields:** `id`, `email`, `password`, `name`, `address`, `pin_code`, `role`
- **Relationships:** Can have multiple reservations.

### ParkingLot

- Represents a parking lot location.
- **Fields:** `id`, `location`, `address`, `pin_code`, `price_per_hour`, `max_spots`
- **Relationships:** Has multiple parking spots.

### ParkingSpot

- Represents an individual parking spot within a parking lot.
- **Fields:** `id`, `lot_id`, `status`, `created_at`
- **Relationships:** Belongs to a `ParkingLot` (via `lot_id`). Can have multiple reservations over time.

### Reservation

- Represents a booking of a parking spot by a user.
- **Fields:** `id`, `user_id`, `spot_id`, `in_time`, `out_time`, `cost`
- **Relationships:** 
    - Belongs to a `User` (via `user_id`)
    - Belongs to a `ParkingSpot` (via `spot_id`)
    - Each reservation is linked to a specific parking spot and user.

**Model Relationships Overview:**

- **User** ⟶ (one-to-many) ⟶ **Reservation**
- **ParkingLot** ⟶ (one-to-many) ⟶ **ParkingSpot**
- **ParkingSpot** ⟶ (one-to-many) ⟶ **Reservation**

This structure allows users to reserve specific spots in specific lots, and supports tracking of spot availability and reservation history.

## 🙋 Author

**Anas Khan**  
_BS Data Science, IIT Madras_


