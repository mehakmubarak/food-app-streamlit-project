
# FoodExpress – Streamlit-Based Food Delivery App

**FoodExpress** is a simple and interactive food delivery application built using **Python and Streamlit**. It includes user authentication, a dynamic menu, cart system, order tracking, and an admin panel for dish uploads.
## Features

###  User Authentication
- Users must sign up or log in to use the app.
- Each user has a personalized experience and order history.

###  Menu (Main Dishes + Desserts)
- Includes items like Chicken Biryani, Paneer Tikka, Zinger Burger, Chocolate Cake, and more.
- Each dish displays an image and price.
- Users can add items to their cart.

###  Cart & Payment
- Cart automatically calculates the total amount.
- Payment options include:
  - Cash on Delivery
  - JazzCash
  - Credit Card

###  Order History
- Logged-in users can view their previous orders and receipts.

###  Order Tracking
- Simulated real-time tracking with random statuses:
  - Preparing
  - On the Way
  - Delivered

###  Admin Panel
- Admin users can upload new dishes with name, price, and image URL.
- Admin access is protected and limited to authorized users.

---

##  Tech Stack

- **Python 3.9+**
- **Streamlit**

All session data is stored in memory (no database required for demo).

---

##  Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mehakmubarak/foodexpress.git
   cd foodexpress
Install dependencies:
bash:pip install streamlit
Run the app: uvx streamlit run app.py
Default Admin Account
Email: admin@gmail.com

Password: admin123

You can change or add more users in the session initialization section of the code.

 Future Improvements
 Add database support (Firebase, PostgreSQL, etc.)

 Quantity selector for items in the cart

 Secure password encryption

 File upload for dish images (instead of URLs)

 Mobile responsive UI

