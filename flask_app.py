import secrets
from datetime import timedelta
from functools import wraps

from flask import (
    Flask, abort, flash, redirect, render_template, request, session, url_for,
)
from sqlalchemy import func, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

import config
import mailer
from db import engine, get_session, remove_session
from models import PasswordReset, Plan, account, membership, utcnow

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)
app.teardown_appcontext(remove_session)  # always release the DB session


def _ensure_schema():
    """Ensure new tables/columns (`password_resets`, `accounts.is_admin`) exist."""
    try:
        PasswordReset.__table__.create(bind=engine, checkfirst=True)
        insp = inspect(engine)
        if insp.has_table('accounts'):
            cols = {c['name'] for c in insp.get_columns('accounts')}
            if 'is_admin' not in cols:
                with engine.begin() as conn:
                    conn.execute(text('ALTER TABLE accounts ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0'))
            if config.ADMIN_USERNAME:
                with engine.begin() as conn:
                    conn.execute(
                        text('UPDATE accounts SET is_admin = 1 WHERE LOWER(username) = :u'),
                        {'u': config.ADMIN_USERNAME},
                    )
    except SQLAlchemyError:
        app.logger.warning("Could not check/update schema (is MySQL running?)")


_ensure_schema()

MINOR_MAX_PRICE = 15       # plans shown to under-18s
MINOR_SPEND_CAP = 10


# ── helpers ─────────────────────────────────────────────────────────────────
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


def get_plan(db_session, plan_id):
    """Fetch a plan by primary key (uses the identity map, no extra query if cached)."""
    try:
        return db_session.get(Plan, int(plan_id))
    except (TypeError, ValueError):
        return None


def new_membership_id(db_session):
    """Generate a unique 'FI-xxxxxx' id (the old 4-digit random id could collide)."""
    while True:
        candidate = f"FI-{secrets.randbelow(900000) + 100000}"
        exists = db_session.query(membership.id).filter(
            membership.membership_id == candidate
        ).first()
        if not exists:
            return candidate


def remember_memberships(results):
    session['lookup_membership_ids'] = ",".join(m.membership_id for m in results)


# ── template helpers ────────────────────────────────────────────────────────
@app.template_filter('gbp')
def gbp(value):
    """8.0 -> '£8', 8.5 -> '£8.50'."""
    if value is None:
        return ''
    value = float(value)
    return f"£{value:,.0f}" if value.is_integer() else f"£{value:,.2f}"


@app.template_filter('calls')
def calls(value):
    """Turn the stored 'unl/unl' or '500/500' into readable text."""
    if not value:
        return ''
    if value == 'unl/unl':
        return 'Unlimited calls and texts'
    minutes, _, texts = value.partition('/')
    return f"{minutes} minutes, {texts} texts" if texts else value


def get_csrf_token():
    """Return (and lazily create) the session's CSRF token."""
    token = session.get('_csrf_token')
    if not token:
        token = secrets.token_hex(16)
        session['_csrf_token'] = token
    return token


@app.before_request
def check_csrf():
    if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
        if not app.config.get('WTF_CSRF_ENABLED', True):
            return
        expected = session.get('_csrf_token')
        provided = request.form.get('csrf_token') or request.headers.get('X-CSRFToken', '')
        if not expected or not provided or not secrets.compare_digest(expected, provided):
            abort(403)


def current_user_is_admin():
    username = session.get('username')
    if not username:
        return False
    if 'is_admin' in session:
        return bool(session['is_admin'])
    user = get_session().query(account).filter(account.username == username).first()
    flag = bool(user and user.is_admin) or (username.lower() == config.ADMIN_USERNAME)
    session['is_admin'] = flag
    return flag


@app.context_processor
def inject_globals():
    return {
        'is_admin': current_user_is_admin(),
        'csrf_token': get_csrf_token,
    }


def password_problem(password):
    if len(password) < 8 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
        return 'Password must be at least 8 characters and include a capital letter and a number'
    return None


# ── pages ───────────────────────────────────────────────────────────────────
@app.route('/')
def base():
    providers = {}
    try:
        sim_plans = get_session().query(Plan).filter(Plan.phone.is_(None), Plan.data_gb.isnot(None)) \
            .order_by(Plan.provider, Plan.price_per_month).all()
    except SQLAlchemyError:
        app.logger.exception("Could not load plans for the home page")
        sim_plans = []
    for plan in sim_plans:
        providers.setdefault(plan.provider, []).append(plan)
    return render_template('base.html', providers=providers)


@app.route('/plans.html')
def view_plans():
    db_session = get_session()
    all_plans = db_session.query(Plan).order_by(Plan.provider, Plan.plan_ID).all()

    # SIM-only comparison table, built from the database instead of hard-coded
    sim_plans = [p for p in all_plans if p.phone is None and p.data_gb is not None]
    sim_providers = sorted({p.provider for p in sim_plans})
    table = {}
    for plan in sorted(sim_plans, key=lambda p: p.plan_ID):
        table.setdefault(plan.type_of_plan.capitalize(), {})[plan.provider] = plan
    return render_template(
        'plans.html', plans=all_plans, sim_table=list(table.items()), sim_providers=sim_providers,
    )


@app.route('/signup.html', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('signup.html')

    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    phone_number = request.form.get('phone_number', '').strip()
    age_raw = request.form.get('age')

    if not username or not email or not password:
        return render_template('signup.html', error='Please fill in all required fields', form=request.form)
    if password != confirm_password:
        return render_template('signup.html', error='Passwords do not match', form=request.form)
    problem = password_problem(password)
    if problem:
        return render_template('signup.html', error=problem, form=request.form)
    try:
        age = int(age_raw) if age_raw else 18
    except ValueError:
        return render_template('signup.html', error='Age must be a number', form=request.form)

    db_session = get_session()
    try:
        taken = db_session.query(account).filter(
            (account.email == email) | (account.username == username)
        ).first()
        if taken:
            msg = 'Email already exists' if taken.email == email else 'Username already exists'
            return render_template('signup.html', error=msg, form=request.form)

        is_admin = username.lower() == config.ADMIN_USERNAME
        db_session.add(account(
            username=username,
            email=email,
            hash_password=generate_password_hash(password),
            phone_number=phone_number,
            age=age,
            is_admin=is_admin,
        ))
        db_session.commit()
    except SQLAlchemyError:
        db_session.rollback()
        app.logger.exception("Sign-up failed")
        return render_template('signup.html', error='Something went wrong', form=request.form)

    session['username'] = username
    session['email'] = email
    session['age'] = age
    session['is_admin'] = is_admin
    return redirect(url_for('base'))


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        identifier = request.form.get('login_id', '').strip()
        password = request.form.get('password', '')
        user = get_session().query(account).filter(
            (account.username == identifier) | (account.email == identifier)
        ).first()
        if user and check_password_hash(user.hash_password, password):
            keep_plan = session.get('selected_plan_id')
            csrf = session.get('_csrf_token')
            is_admin = bool(user.is_admin) or (user.username.lower() == config.ADMIN_USERNAME)
            if is_admin and not user.is_admin:
                user.is_admin = True
                get_session().commit()
            session.clear()  # avoid carrying over stale/foreign session data
            if csrf:
                session['_csrf_token'] = csrf
            session['username'] = user.username
            session['age'] = user.age
            session['email'] = user.email
            session['is_admin'] = is_admin
            if keep_plan:
                session['selected_plan_id'] = keep_plan
                return redirect(url_for('confirmation'))
            return redirect(url_for('base'))
        error = "Invalid username or password. Please try again."
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('base'))


# ── forgot password: e-mail a one-time code ─────────────────────────────────
def issue_reset_code(email):
    """Create and e-mail a reset code. Silent if the e-mail is unknown, so the
    page never reveals which addresses are registered."""
    db_session = get_session()
    user = db_session.query(account).filter(func.lower(account.email) == email).first()
    if not user:
        return
    now = utcnow()
    too_soon = db_session.query(PasswordReset.id).filter(
        PasswordReset.account_id == user.account_id,
        PasswordReset.created > now - timedelta(seconds=config.RESET_RESEND_SECONDS),
    ).first()
    if too_soon:
        return

    db_session.query(PasswordReset).filter(
        PasswordReset.account_id == user.account_id, PasswordReset.used.is_(False)
    ).update({'used': True})
    code = f"{secrets.randbelow(1_000_000):06d}"
    db_session.add(PasswordReset(
        account_id=user.account_id,
        code_hash=generate_password_hash(code),
        expires_at=now + timedelta(minutes=config.RESET_CODE_MINUTES),
    ))
    db_session.commit()
    mailer.send_reset_code(user.email, user.username, code, config.RESET_CODE_MINUTES)


@app.route('/forgot_password.html', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')

    email = request.form.get('email', '').strip().lower()
    if not email:
        return render_template('forgot_password.html', error='Please enter your email address')
    try:
        issue_reset_code(email)
    except SQLAlchemyError:
        get_session().rollback()
        app.logger.exception("Could not create a reset code")
        return render_template('forgot_password.html', error='Something went wrong. Please try again.')

    session['reset_email'] = email
    flash(f"If that email is registered, we have sent a 6-digit code. It expires in {config.RESET_CODE_MINUTES} minutes.")
    return redirect(url_for('reset_password'))


@app.route('/reset_password.html', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        return render_template('reset_password.html', email=session.get('reset_email', ''))

    email = request.form.get('email', '').strip().lower()
    code = request.form.get('code', '').strip()
    password = request.form.get('password', '')

    def fail(message):
        return render_template('reset_password.html', error=message, email=email)

    if password != request.form.get('confirm_password', ''):
        return fail('Passwords do not match')
    problem = password_problem(password)
    if problem:
        return fail(problem)

    bad_code = 'That code is invalid or has expired. Request a new one.'
    db_session = get_session()
    user = db_session.query(account).filter(func.lower(account.email) == email).first()
    reset = None
    if user:
        reset = db_session.query(PasswordReset).filter(
            PasswordReset.account_id == user.account_id, PasswordReset.used.is_(False)
        ).order_by(PasswordReset.id.desc()).first()
    if not reset or reset.expires_at < utcnow() or reset.attempts >= config.RESET_MAX_ATTEMPTS:
        return fail(bad_code)

    if not check_password_hash(reset.code_hash, code):
        reset.attempts += 1
        db_session.commit()
        return fail(bad_code)

    user.hash_password = generate_password_hash(password)
    reset.used = True
    db_session.commit()
    session.pop('reset_email', None)
    flash('Your password has been changed. You can log in now.')
    return redirect(url_for('login'))


@app.route('/recommendation.html', methods=['POST', 'GET'])
@login_required
def recommend():
    username = session.get('username')
    if request.method == 'GET':
        return render_template('recommendation.html', username=username, recommended_plans=None)

    query = get_session().query(Plan)
    age = session.get('age') or 18

    if age < 18:
        query = query.filter(Plan.price_per_month <= MINOR_MAX_PRICE)
    else:
        try:
            desired_data = float(request.form['data_amount'])
            budget = float(request.form['maximum_budget'])
        except (KeyError, ValueError):
            return render_template('recommendation.html', username=username, recommended_plans=None), 400

        provider = request.form.get('provider')
        phone_required = request.form.get('phone_required') in ('yes', 'on')
        phone_models = request.form.getlist('phone_models')

        if provider:
            query = query.filter(Plan.provider == provider)
        query = query.filter((Plan.unlimited.is_(True)) | (Plan.data_gb >= desired_data))
        if phone_required:
            query = query.filter(Plan.phone.in_(phone_models))
        else:
            query = query.filter(Plan.phone.is_(None))
        if budget:
            query = query.filter(Plan.price_per_month <= budget)

    plan_list = query.order_by(Plan.price_per_month).all()
    session['selected_plan_id'] = plan_list[0].plan_ID if plan_list else None
    return render_template('recommendation.html', recommended_plans=plan_list, username=username)


@app.route('/confirmation.html', methods=['GET', 'POST'])
def confirmation():
    db_session = get_session()

    if request.method == 'GET':
        plan_id = session.get('selected_plan_id')
        if not plan_id:
            return redirect(url_for('view_plans'))
        return render_template('confirmation.html', plan=get_plan(db_session, plan_id), age=session.get('age'))

    # User picked a plan
    if 'plan_id' in request.form:
        plan_id = request.form.get('plan_id')
        session['selected_plan_id'] = plan_id
        if not session.get('username'):
            return redirect(url_for('login'))
        return render_template('confirmation.html', plan=get_plan(db_session, plan_id), age=session.get('age'))

    # User confirmed payment
    if request.form.get('confirm_payment') == 'true':
        plan_id = session.get('selected_plan_id')
        username = session.get('username')
        if not plan_id:
            return "Error: No plan selected. Your session might have expired."
        if not username:
            return redirect(url_for('login'))

        user_account = db_session.query(account).filter(account.username == username).first()
        selected_plan = get_plan(db_session, plan_id)
        if not user_account or not selected_plan:
            return redirect(url_for('view_plans'))

        payment_method = request.form.get('payment_method', 'card').strip().lower()
        if payment_method not in ('card', 'apple_pay'):
            return render_template(
                'confirmation.html', plan=selected_plan, age=session.get('age'),
                error='Please choose a valid payment method.', form=request.form,
            )

        payment_summary = 'Apple Pay'
        if payment_method == 'card':
            card_name = request.form.get('card_name', '').strip()
            card_number = ''.join(ch for ch in request.form.get('card_number', '') if ch.isdigit())
            card_expiry = request.form.get('card_expiry', '').strip()
            card_cvc = ''.join(ch for ch in request.form.get('card_cvc', '') if ch.isdigit())

            def fail_card(msg):
                return render_template(
                    'confirmation.html', plan=selected_plan, age=session.get('age'),
                    error=msg, form=request.form,
                )

            if not card_name:
                return fail_card('Please enter the name on your card.')
            if not (13 <= len(card_number) <= 19):
                return fail_card('Please enter a valid 16-digit card number.')
            if len(card_expiry) != 5 or card_expiry[2] != '/' or not (card_expiry[:2].isdigit() and card_expiry[3:].isdigit()):
                return fail_card('Please enter expiry date in MM/YY format.')
            exp_month = int(card_expiry[:2])
            if not (1 <= exp_month <= 12):
                return fail_card('Expiry month must be between 01 and 12.')
            if not (3 <= len(card_cvc) <= 4):
                return fail_card('Please enter a valid 3 or 4 digit CVC.')

            payment_summary = f"Card ending in {card_number[-4:]}"

        age = user_account.age or 18
        is_minor = age < 18
        membership_id = new_membership_id(db_session)
        db_session.add(membership(
            membership_id=membership_id,
            full_name=username,
            email=user_account.email or f"{username}@email.com",
            age=age,
            plan_id=selected_plan.plan_ID,
            spend_cap=MINOR_SPEND_CAP if is_minor else selected_plan.price_per_month,
            age_restricted=is_minor,
            phone_number=user_account.phone_number,
        ))
        try:
            db_session.commit()
        except SQLAlchemyError:
            db_session.rollback()
            app.logger.exception("Could not create membership")
            return "Database Error: could not save your membership. Please try again."
        session['success_membership_id'] = membership_id
        session['payment_summary'] = payment_summary
        return redirect(url_for('payment_success'))

    return redirect(url_for('view_plans'))


@app.route('/success.html')
def payment_success():
    plan_id = session.get('selected_plan_id')
    selected_plan = get_plan(get_session(), plan_id) if plan_id else None
    return render_template(
        'success.html',
        plan=selected_plan,
        age=session.get('age'),
        membership_id=session.get('success_membership_id', 'FI-PENDING'),
        payment_summary=session.get('payment_summary'),
    )


@app.route('/membership_lookup.html', methods=['GET', 'POST'])
def membership_lookup():
    db_session = get_session()

    def find_by_email(email):
        return db_session.query(membership).filter(membership.email == email).all()

    if session.get('email'):
        results = find_by_email(session['email'])
        if results:
            remember_memberships(results)
            return redirect(url_for('membership_result'))

    error_msg = None
    if request.method == 'POST':
        search_email = request.form.get('email', '').strip()
        if search_email:
            results = find_by_email(search_email)
            if results:
                remember_memberships(results)
                return redirect(url_for('membership_result'))
            error_msg = "No plans found."
    return render_template('membership_lookup.html', error_msg=error_msg)


@app.route('/membership_result.html')
def membership_result():
    id_string = session.get('lookup_membership_ids', '')
    if not id_string:
        return redirect(url_for('membership_lookup'))

    # `membership.plan` is joined-loaded, so there is no extra query per record
    records = get_session().query(membership).filter(
        membership.membership_id.in_(id_string.split(','))
    ).all()
    plans = {r.plan_id: r.plan for r in records}
    return render_template('membership_result.html', records=records, plans=plans)


@app.route('/admin.html')
def admin_dashboard():
    if not current_user_is_admin():
        abort(403)
    db_session = get_session()
    return render_template(
        'admin.html',
        accounts=db_session.query(account).all(),
        memberships=db_session.query(membership).all(),
    )


def render_error(code, title, message):
    return render_template('error.html', code=code, title=title, message=message), code


@app.errorhandler(403)
def forbidden_error(error):
    return render_error(403, 'Access denied', 'You do not have permission to view this page.')


@app.errorhandler(404)
def not_found_error(error):
    return render_error(404, 'Page not found', 'We could not find the page you were looking for.')


@app.errorhandler(500)
def internal_error(error):
    return render_error(500, 'Something went wrong', 'An unexpected error occurred. Please try again later.')


if __name__ == '__main__':
    app.run(debug=config.DEBUG)
