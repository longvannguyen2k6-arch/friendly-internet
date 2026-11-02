# Friendly Internet – UK Mobile Network Portal

A Flask + SQLAlchemy + MySQL web application for **Friendly Internet**, a UK mobile network company managing three partner networks (**Fone**, **Gap**, and **Flipper**). Users can browse and compare mobile plans, get personalised recommendations, create accounts, purchase memberships (via Card or Apple Pay), look up registered plans, reset forgotten passwords by e-mail code, and manage records through an admin dashboard.

---

## Features

- **Home & Plan Comparison (`/` & `/plans.html`):**
  - Dynamic SIM-only summary and side-by-side comparison table loaded from MySQL.
  - Client-side provider filtering (`Fone`, `Gap`, `Flipper`), SIM-only toggle, price range slider, and price sorting.
- **Plan Recommendation Quiz (`/recommendation.html`):**
  - Matches users to plans by preferred network, monthly data usage, handset inclusion, and maximum budget.
  - Under-18 accounts automatically filter to plans up to £15/month and receive a £10/month spending cap.
- **Authentication & Password Recovery (`/signup.html`, `/login.html`, `/forgot_password.html`, `/reset_password.html`):**
  - Password hashing with Werkzeug, password-strength rules (8+ characters, uppercase letter, digit), and live strength indicator.
  - 6-digit one-time reset code sent via SMTP (or printed to console in local development), stored hashed in `password_resets` with expiry and attempt limits.
- **Checkout & Membership Lookup (`/confirmation.html`, `/success.html`, `/membership_lookup.html`, `/membership_result.html`):**
  - Supports **Debit/Credit Card** (with validation and input formatting) or **Apple Pay**.
  - Generates unique `FI-xxxxxx` membership IDs and allows looking up active plans by e-mail.
- **Admin Dashboard (`/admin.html`):**
  - Protected by the `accounts.is_admin` database flag; displays all registered user accounts and active memberships.
- **Security & Performance:**
  - Session-based **CSRF protection** on all `POST` forms.
  - Pooled SQLAlchemy engine (`scoped_session`) with automatic session cleanup on request teardown.

---

## Project Structure

```text
.
├── flask_app.py                  # Main Flask routes, CSRF hook, filters, error handlers
├── config.py                     # Environment variable & .env configuration loader
├── db.py                         # SQLAlchemy engine & scoped_session management
├── models.py                     # ORM models: Plan, membership, account, PasswordReset
├── mailer.py                     # SMTP e-mail helper for password-reset codes
├── app.py                        # Backwards-compatible shim importing from db.py
├── requirements.txt              # Python dependencies
├── .env.example                  # Template for local environment variables
├── optimize_db.sql               # Optional index & schema updates for existing MySQL DB
├── webprogramming_accounts.sql   # MySQL dump: accounts table
├── webprogramming_plans.sql      # MySQL dump: plans table & seed data
├── webprogramming_memberships.sql# MySQL dump: memberships table
├── webprogramming_routines.sql   # MySQL dump: routines
├── static/
│   ├── style.css                 # Stylesheet
│   └── app.js                    # Progressive-enhancement JavaScript
└── templates/
    ├── layout.html               # Base template (shared header, flash messages, footer)
    ├── base.html                 # Home page
    ├── plans.html                # All plans & SIM-only comparison table
    ├── recommendation.html       # "Find My Plan" quiz
    ├── signup.html               # Account registration
    ├── login.html                # User login
    ├── forgot_password.html      # Request password reset code
    ├── reset_password.html       # Verify 6-digit code & set new password
    ├── confirmation.html         # Order summary & Card / Apple Pay checkout
    ├── success.html              # Order confirmation & membership ID
    ├── membership_lookup.html    # Search memberships by e-mail
    ├── membership_result.html    # Display memberships for an e-mail
    ├── admin.html                # Admin dashboard
    └── error.html                # 403 / 404 / 500 error page
```

---

## Setup & Installation

### 1. Prerequisites
- **Python 3.10+**
- **MySQL 8.0+**

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Import the MySQL database
Create the `webprogramming` database and import the SQL dump files in order:

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS webprogramming;"
mysql -u root -p webprogramming < webprogramming_plans.sql
mysql -u root -p webprogramming < webprogramming_memberships.sql
mysql -u root -p webprogramming < webprogramming_accounts.sql
mysql -u root -p webprogramming < webprogramming_routines.sql
```

*(Optional)* Apply the index and schema optimizations:
```bash
mysql -u root -p webprogramming < optimize_db.sql
```

> Note: On startup, the app automatically creates the `password_resets` table and adds the `is_admin` column to `accounts` if they do not exist yet.

### 4. Configure environment variables
Copy `.env.example` to `.env` and fill in your local settings:

```bash
cp .env.example .env
```

```ini
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_NAME=webprogramming
SECRET_KEY=replace-with-a-random-secret-key
ADMIN_USERNAME=longdepzaii
FLASK_DEBUG=1

# Optional SMTP settings for e-mailing password-reset codes.
# If SMTP_HOST is left empty, reset codes are printed to the server console.
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM=
```

### 5. Run the application
```bash
python flask_app.py
```
Then open **http://127.0.0.1:5000** in your browser.
