import streamlit as st
import datetime
import random

# -------- Session Initialization ---------
if 'users' not in st.session_state:
    st.session_state.users = {
        "admin@food.com": {"password": "admin123", "role": "admin"},
        "user@example.com": {"password": "password123", "role": "user"}
    }

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'cart' not in st.session_state:
    st.session_state.cart = []

if 'orders' not in st.session_state:
    st.session_state.orders = []

# Image with urls
if 'dishes' not in st.session_state:
    st.session_state.dishes = {
        "Main": {
            "Chicken Biryani": {
                "price": 450,
                "image": "https://i.pinimg.com/736x/57/58/8b/57588b32c55b721df9710bfe1093fe1f.jpg"
            },
            "Beef Kebab": {
                "price": 350,
                "image": "https://i.pinimg.com/736x/5a/70/2c/5a702c509b9622a795b3b1ed4c56cc59.jpg"
            },
            "Paneer Tikka": {
                "price": 400,
                "image": "https://i.pinimg.com/736x/49/e5/80/49e5800ada1c3a59021e2c84bf91c457.jpg"
            },
            "Zinger Burger": {
                "price": 300,
                "image": "https://i.pinimg.com/736x/98/3c/d0/983cd01a48bc32e9e095dedbd1033b3c.jpg"
            }
        },
        "Desserts": {
            "Chocolate Cake": {
                "price": 250,
                "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=600&q=80"
            },
            "Ice Cream Sundae": {
                "price": 180,
                "image": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?auto=format&fit=crop&w=600&q=80"
            }
        }
    }

# ------- Helper Functions -------
def login(email, password):
    user = st.session_state.users.get(email)
    if user and user["password"] == password:
        st.session_state.authenticated = True
        st.session_state.current_user = email
        return True
    return False

def signup(email, password):
    if email in st.session_state.users:
        return False
    st.session_state.users[email] = {"password": password, "role": "user"}
    return True

def get_user_role():
    return st.session_state.users[st.session_state.current_user]["role"]

def get_cart_total():
    return sum(item["price"] for item in st.session_state.cart)

def place_order():
    order = {
        "user": st.session_state.current_user,
        "items": st.session_state.cart.copy(),
        "total": get_cart_total(),
        "time": datetime.datetime.now(),
        "status": "Preparing"
    }
    st.session_state.orders.append(order)
    st.session_state.cart.clear()
    return order

# ---------------- Login/Signup UI ----------------
if not st.session_state.authenticated:
    st.title("🍱 FoodExpress - Login or Sign Up")
    mode = st.radio("Select Mode", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if mode == "Login":
        if st.button("Login"):
            if login(email, password):
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error("❌ Invalid email or password.")
    else:
        if st.button("Sign Up"):
            if signup(email, password):
                st.success(" Account created and logged in!")
                st.session_state.authenticated = True
                st.session_state.current_user = email
                st.rerun()
            else:
                st.error("❌ User already exists.")

# ------ Main App Interface ---------
else:
    st.title(f" Welcome, {st.session_state.current_user}!")

    tab1, tab2, tab3, tab4 = st.tabs(["Menu", "🧾 My Orders", "Track Orders", "🔐 Admin Panel"])

    # --------- MENU TAB ---------
    with tab1:
        st.subheader(" Main Dishes")
        for name, info in st.session_state.dishes["Main"].items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(info["image"], width=150)
            with col2:
                st.write(f"**{name}** — Rs {info['price']}")
                if st.button(f"Add {name}", key=f"add_{name}"):
                    st.session_state.cart.append({"name": name, "price": info["price"]})
                    st.success(f"{name} added to cart!")

        st.subheader(" Desserts")
        for name, info in st.session_state.dishes["Desserts"].items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(info["image"], width=150)
            with col2:
                st.write(f"**{name}** — Rs {info['price']}")
                if st.button(f"Add {name}", key=f"add_{name}_dessert"):
                    st.session_state.cart.append({"name": name, "price": info["price"]})
                    st.success(f"{name} added to cart!")

        #  Cart
        if st.session_state.cart:
            st.subheader(" Your Cart")
            for item in st.session_state.cart:
                st.write(f"- {item['name']} — Rs {item['price']}")
            st.write(f"**Total:** Rs {get_cart_total()}")

            payment_method = st.radio("Select payment method:", ["Cash on Delivery", "JazzCash", "Credit Card"])
            if st.button("Place Order"):
                order = place_order()
                st.success("Order placed successfully!")
                st.balloons()
                st.write(f"**Total Paid:** Rs {order['total']} via {payment_method}")
                st.write(" Your order is now being prepared!")

    # ---------------- ORDER HISTORY TAB ----------------
    with tab2:
        st.subheader(" Your Orders")
        user_orders = [o for o in st.session_state.orders if o["user"] == st.session_state.current_user]
        if not user_orders:
            st.info("You haven't placed any orders yet.")
        else:
            for o in reversed(user_orders):
                st.markdown(f"####  {o['time'].strftime('%Y-%m-%d %H:%M:%S')}")
                for item in o["items"]:
                    st.write(f"- {item['name']} — Rs {item['price']}")
                st.write(f"**Total:** Rs {o['total']}")
                st.write(f" Status: **{o['status']}**")
                st.markdown("---")

    # ----------- ORDER TRACKING TAB --------
    with tab3:
        st.subheader("Track Your Latest Order")
        user_orders = [o for o in st.session_state.orders if o["user"] == st.session_state.current_user]
        if user_orders:
            latest = user_orders[-1]
            current_status = random.choice(["Preparing", "On the Way", "Delivered"])
            latest["status"] = current_status
            st.info(f" Order Status: **{current_status}**")
        else:
            st.warning("No order found to track.")

    # ------- ADMIN PANEL TAB ----------
    with tab4:
        if get_user_role() == "admin":
            st.subheader("🔐 Admin: Upload New Dish")
            category = st.selectbox("Choose category", ["Main", "Desserts"])
            name = st.text_input("Dish Name")
            price = st.number_input("Price (Rs)", step=10)
            image = st.text_input("Image URL")
            if st.button("Upload Dish"):
                if name and price and image:
                    st.session_state.dishes[category][name] = {"price": price, "image": image}
                    st.success(f"{name} added to {category} menu!")
                else:
                    st.error("Please fill all fields.")
        else:
            st.warning("Admin access only.")

    # ---------------- Logout ----------------
    st.sidebar.title("🔐 Account")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.session_state.cart.clear()
        st.rerun()


