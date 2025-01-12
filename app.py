from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import mysql.connector
from datetime import datetime, timedelta
import os
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = "your_secret_key"
bcrypt = Bcrypt(app)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lost_and_founds"
    )

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["role"] = user["role"]
            session["email"] = user["email"]
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for("login"))
    
    # Handle GET request to render the login page
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_post():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if password != confirm_password:
        flash("Passwords do not match!", "danger")
        return redirect(url_for("register"))

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                       (name, email, hashed_password, "user"))
        conn.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))
    except mysql.connector.Error as err:
        flash("Error: Email already registered.", "danger")
        return redirect(url_for("register"))
    finally:
        conn.close()

@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get user's items
    cursor.execute("SELECT * FROM items WHERE created_by = %s", (session["user_id"],))
    user_items = cursor.fetchall()
    
    # Get user's claims
    cursor.execute("""
        SELECT claims.*, items.name as item_name, items.description, items.location 
        FROM claims 
        JOIN items ON claims.item_id = items.id 
        WHERE claims.claimed_by = %s
    """, (session["user_id"],))
    user_claims = cursor.fetchall()
    
    # Get user's messages
    cursor.execute("""
        SELECT messages.*, users.name as sender_name, items.name as item_name 
        FROM messages 
        JOIN users ON messages.sender_id = users.id 
        JOIN items ON messages.item_id = items.id 
        WHERE messages.receiver_id = %s 
        ORDER BY sent_at DESC
    """, (session["user_id"],))
    messages = cursor.fetchall()
    
    conn.close()
    return render_template("home.html", 
                         name=session["name"], 
                         items=user_items, 
                         claims=user_claims, 
                         messages=messages)

@app.route("/lost_found_items")
def lost_found_items():
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    search_query = request.args.get("search", "")
    status_filter = request.args.get("status", "")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    print("Search Query:", search_query)
    print("Status Filter:", status_filter)
    
    # Building the SQL query
    query = """
        SELECT items.*, users.name AS creator_name 
        FROM items
        LEFT JOIN users ON items.created_by = users.id
        WHERE 1=1
    """
    params = []
    
    if search_query:
        query += " AND (items.name LIKE %s OR items.description LIKE %s OR items.location LIKE %s)"
        params.extend(['%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'])
    
    if status_filter:
        query += " AND items.status = %s"
        params.append(status_filter)
    
    # Execute the query with parameters
    cursor.execute(query, params)
    items = cursor.fetchall()
    
    conn.close()
    return render_template("lost_found_items.html", 
                         items=items, 
                         search_query=search_query, 
                         status_filter=status_filter)

@app.route("/claim_item/<int:item_id>", methods=["POST"])
def claim_item(item_id):
    if "user_id" not in session:
        flash("Please log in to claim an item.", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Insert the claim
        cursor.execute("""
            INSERT INTO claims (item_id, claimed_by, claimant_name, claimant_email, claimed_at)
            VALUES (%s, %s, %s, %s, NOW())
        """, (item_id, session["user_id"], session["name"], session["email"]))

        # Update the item's status to 'claimed'
        cursor.execute("""
            UPDATE items
            SET status = 'claimed'
            WHERE id = %s
        """, (item_id,))
        conn.commit()

        flash("Item claimed successfully!", "success")
    except mysql.connector.Error as err:
        flash("Error claiming item. Please try again.", "danger")
    finally:
        conn.close()
    
    return redirect(url_for("lost_found_items"))


@app.route("/send_message", methods=["POST"])
def send_message():
    if "user_id" not in session:
        flash("Please log in to send messages.", "warning")
        return redirect(url_for("login"))

    receiver_id = request.form.get("receiver_id")
    item_id = request.form.get("item_id")
    message_text = request.form.get("message")

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO messages (sender_id, receiver_id, item_id, message)
            VALUES (%s, %s, %s, %s)
        """, (session["user_id"], receiver_id, item_id, message_text))
        conn.commit()
        flash("Message sent successfully!", "success")
    except mysql.connector.Error as err:
        flash("Error sending message. Please try again.", "danger")
    finally:
        conn.close()
    
    return redirect(request.referrer or url_for("home"))

@app.route("/reply_message", methods=["POST"])
def reply_message():
    if "user_id" not in session:
        flash("Please log in to send messages.", "warning")
        return redirect(url_for("login"))

    receiver_id = request.form.get("receiver_id")
    item_id = request.form.get("item_id")
    reply_text = request.form.get("reply")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO messages (sender_id, receiver_id, item_id, message)
            VALUES (%s, %s, %s, %s)
        """, (session["user_id"], receiver_id, item_id, reply_text))
        conn.commit()
        flash("Reply sent successfully!", "success")
    except mysql.connector.Error as err:
        flash("Error sending reply. Please try again.", "danger")
    finally:
        conn.close()

    return redirect(url_for("home"))

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    if "user_id" not in session:
        flash("Please log in to submit feedback.", "warning")
        return redirect(url_for("login"))

    feedback_text = request.form.get("feedback")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO feedback (user_id, feedback_text)
            VALUES (%s, %s)
        """, (session["user_id"], feedback_text))
        conn.commit()
        flash("Thank you for your feedback!", "success")
    except mysql.connector.Error as err:
        flash("Error submitting feedback. Please try again.", "danger")
    finally:
        conn.close()
    
    return redirect(url_for("home"))

@app.route("/register_item")
def register_item_page():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("register_item.html")

@app.route("/register_item", methods=["POST"])
def register_item():
    if "user_id" not in session:
        return redirect(url_for("login"))

    name = request.form["name"]
    description = request.form["description"]
    location = request.form["location"]
    status = request.form["status"]
    image = request.files["image"]
    image_filename = f"uploads/{image.filename}"
    image.save(f"static/{image_filename}")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO items (name, description, location, status, image, created_by)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, description, location, status, image_filename, session["user_id"]))
        conn.commit()
        flash("Item registered successfully!", "success")
    except mysql.connector.Error as err:
        flash("Error registering item.", "danger")
    finally:
        conn.close()
    return redirect(url_for("lost_found_items"))

@app.route("/admin")
def admin_page():
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get all items
    cursor.execute("""
        SELECT items.*, users.name as creator_name 
        FROM items 
        JOIN users ON items.created_by = users.id
    """)
    items = cursor.fetchall()

    # Get all claims
    cursor.execute("""
        SELECT claims.*, items.name as item_name, users.name as claimer_name 
        FROM claims
        JOIN items ON claims.item_id = items.id
        JOIN users ON claims.claimed_by = users.id
    """)
    claims = cursor.fetchall()

    # Get all users
    cursor.execute("SELECT * FROM users WHERE role != 'admin'")
    users = cursor.fetchall()
    
    # Get all feedback
    cursor.execute("""
        SELECT feedback.*, users.name as user_name 
        FROM feedback 
        JOIN users ON feedback.user_id = users.id
    """)
    feedback = cursor.fetchall()
    
    conn.close()
    return render_template("admin.html", 
                         items=items, 
                         claims=claims, 
                         users=users, 
                         feedback=feedback)
    
@app.route("/delete_item/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    if "user_id" not in session or session["role"] != "admin":
        flash("You are not authorized to perform this action.")
        return redirect(url_for("admin_page"))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # First delete any claims associated with the item
        cursor.execute("DELETE FROM claims WHERE item_id = %s", (item_id,))
        
        # Then delete the item from the items table
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        
        conn.commit()
        flash("Item deleted successfully!")
    except mysql.connector.Error as err:
        flash("Error deleting item.")
    finally:
        conn.close()

    return redirect(url_for("admin_page"))

@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if "user_id" not in session or session["role"] != "admin":
        flash("You are not authorized to perform this action.")
        return redirect(url_for("admin_page"))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Delete claims associated with the user
        cursor.execute("DELETE FROM claims WHERE claimed_by = %s", (user_id,))
        
        # Delete the user
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        conn.commit()
        flash("User deleted successfully!")
    except mysql.connector.Error as err:
        flash("Error deleting user.")
    finally:
        conn.close()

    return redirect(url_for("admin_page"))

@app.route("/delete_claim/<int:claim_id>", methods=["POST"])
def delete_claim(claim_id):
    if "user_id" not in session or session["role"] != "admin":
        flash("You are not authorized to perform this action.")
        return redirect(url_for("admin_page"))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Delete the claim from the claims table
        cursor.execute("DELETE FROM claims WHERE id = %s", (claim_id,))
        conn.commit()
        flash("Claim deleted successfully!")
    except mysql.connector.Error as err:
        flash("Error deleting claim.")
    finally:
        conn.close()

    return redirect(url_for("admin_page"))

def delete_old_claims():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Delete claims older than 1 minute (for testing)
        cursor.execute("""
            DELETE FROM claims WHERE claimed_at < %s
        """, (datetime.now() - timedelta(days=2),))
        conn.commit()
        print(f"Deleted {cursor.rowcount} old claims.")

        # Delete items with status 'claimed' and not associated with any claim
        cursor.execute("""
            DELETE FROM items 
            WHERE status = 'claimed' AND id NOT IN (SELECT item_id FROM claims)
        """)
        conn.commit()
        print(f"Deleted {cursor.rowcount} old claimed items.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_old_claims, trigger="interval", days=1)  
scheduler.start()

# Ensure the scheduler shuts down properly when the app exits
atexit.register(lambda: scheduler.shutdown())

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)