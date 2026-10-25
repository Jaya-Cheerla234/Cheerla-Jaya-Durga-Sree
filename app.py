"""
=============================================================================
Prakriti: Nature & Belief Explorer - Flask Application Server
=============================================================================
This is the main application server for Prakriti. It defines the routes
for browsing nature elements, exploring the 'Belief vs Science' comparison,
viewing the eco-festivals calendar, running the interactive quiz, and
managing content through the Admin Portal.
=============================================================================
"""

import os
import json
from functools import wraps
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify
)

# Import our custom database module
import database

# Initialize the Flask application
app = Flask(__name__)

# Secret key used for secure session cookies and flash notifications
# Can be configured via environment variable for production deployments
app.secret_key = os.environ.get("SECRET_KEY", "prakriti_sacred_nature_secret_key_2026")

# Admin password for the curator management portal
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "prakriti2026")


# =============================================================================
# HELPER DECORATOR: ADMIN LOGIN REQUIRED
# =============================================================================
def admin_required(f):
    """
    Decorator to protect admin routes.
    If the user is not authenticated in the session, redirects to login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Please log in with the admin password to access this page.", "error")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function


# =============================================================================
# PUBLIC ROUTES
# =============================================================================

@app.route("/")
def index():
    """
    Home Page:
    Displays the hero section, spiritual & scientific harmony introduction,
    quick stats, and the grid of all 12 nature elements.
    """
    elements = database.get_all_elements()
    stats = database.get_stats()
    return render_template(
        "index.html",
        elements=elements,
        stats=stats,
        active_page="home"
    )


@app.route("/browse")
def browse():
    """
    Browse Page:
    Allows visitors to search and filter elements by name, category, or linked festival.
    Provides data for both server-rendered filtering and client-side live filtering.
    """
    category = request.args.get("category", "All")
    search = request.args.get("search", "").strip()
    festival_id = request.args.get("festival_id", "")

    elements = database.get_all_elements(
        category=category,
        search=search,
        festival_id=festival_id if festival_id else None
    )
    categories = database.get_categories()
    festivals = database.get_all_festivals()

    return render_template(
        "browse.html",
        elements=elements,
        categories=categories,
        festivals=festivals,
        current_category=category,
        current_search=search,
        current_festival_id=festival_id,
        active_page="browse"
    )


@app.route("/element/<int:element_id>")
def element_detail(element_id):
    """
    Detail Page for a Nature Element:
    Shows the 'Belief vs Science' card, the synthesis takeaway, and linked festivals.
    """
    result = database.get_element_by_id(element_id)
    if not result:
        flash("The requested nature element was not found.", "error")
        return redirect(url_for("browse"))

    return render_template(
        "detail.html",
        element=result["element"],
        festivals=result["festivals"],
        prev_id=result["prev_id"],
        next_id=result["next_id"],
        active_page="browse"
    )


@app.route("/festivals")
def festivals():
    """
    Festivals Page:
    Lists all nature-honoring festivals with the calendar month,
    the element each one honors, and detailed cultural/ecological context.
    """
    all_festivals = database.get_all_festivals()
    return render_template(
        "festivals.html",
        festivals=all_festivals,
        active_page="festivals"
    )


@app.route("/quiz")
def quiz():
    """
    Quiz Page: 'Superstition or Science?':
    Renders the 10-question interactive challenge with live score tracking,
    instant answers, and detailed scientific explanations.
    """
    questions_rows = database.get_quiz_questions(limit=10)
    
    # Convert SQLite Row objects into standard serializable Python dictionaries
    questions_list = []
    for q in questions_rows:
        questions_list.append({
            "id": q["id"],
            "question": q["question"],
            "option_a": q["option_a"],
            "option_b": q["option_b"],
            "option_c": q["option_c"],
            "option_d": q["option_d"],
            "correct_option": q["correct_option"],
            "explanation": q["explanation"]
        })

    # Pass JSON string for safe client-side execution in quiz.js
    questions_json = json.dumps(questions_list)

    return render_template(
        "quiz.html",
        questions=questions_list,
        questions_json=questions_json,
        active_page="quiz"
    )


@app.route("/api/quiz")
def api_quiz():
    """
    JSON API returning all quiz questions.
    Useful for client fetch requests or external integration.
    """
    questions_rows = database.get_quiz_questions()
    data = [dict(q) for q in questions_rows]
    return jsonify(data)


# =============================================================================
# ADMIN AUTHENTICATION ROUTES
# =============================================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """
    Admin Login Page:
    Authenticates curator using simple password access.
    """
    if session.get("is_admin"):
        return redirect(url_for("admin"))

    if request.method == "POST":
        entered_password = request.form.get("password", "").strip()
        if entered_password == ADMIN_PASSWORD:
            session["is_admin"] = True
            flash("Welcome back, Curator! Admin session started.", "success")
            return redirect(url_for("admin"))
        else:
            flash("Incorrect password. Please try again or use the default key.", "error")

    return render_template("admin_login.html", active_page="admin")


@app.route("/admin/logout")
def admin_logout():
    """
    Logs out the current admin curator and ends the session.
    """
    session.pop("is_admin", None)
    flash("You have logged out of the Admin Portal.", "success")
    return redirect(url_for("index"))


# =============================================================================
# ADMIN DASHBOARD & CRUD ROUTES
# =============================================================================

@app.route("/admin")
@admin_required
def admin():
    """
    Admin Management Dashboard:
    Tabs for Elements, Beliefs, Festivals, and Quiz Questions.
    """
    elements = database.get_all_elements()
    beliefs = database.get_all_beliefs()
    festivals_list = database.get_all_festivals()
    quiz_questions = database.get_quiz_questions()
    stats = database.get_stats()

    return render_template(
        "admin.html",
        elements=elements,
        beliefs=beliefs,
        festivals=festivals_list,
        quiz_questions=quiz_questions,
        stats=stats,
        active_page="admin"
    )


# --- Element CRUD ---
@app.route("/admin/element/add", methods=["POST"])
@admin_required
def admin_add_element():
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()
    image_url = request.form.get("image_url", "").strip() or "/static/images/tulsi.svg"

    if name and category and description:
        new_id = database.add_element(name, category, description, image_url)
        flash(f"Element '{name}' (ID #{new_id}) successfully added!", "success")
    else:
        flash("Please fill in all required fields for the element.", "error")
    return redirect(url_for("admin"))


@app.route("/admin/element/edit/<int:element_id>", methods=["GET", "POST"])
@admin_required
def admin_edit_element(element_id):
    elem_data = database.get_element_by_id(element_id)
    if not elem_data:
        flash("Element not found.", "error")
        return redirect(url_for("admin"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        image_url = request.form.get("image_url", "").strip() or "/static/images/tulsi.svg"

        if name and category and description:
            database.update_element(element_id, name, category, description, image_url)
            flash(f"Element '{name}' successfully updated!", "success")
            return redirect(url_for("admin"))
        else:
            flash("All fields are required.", "error")

    return render_template(
        "admin_edit.html",
        item_type="element",
        item=elem_data["element"],
        active_page="admin"
    )


@app.route("/admin/element/delete/<int:element_id>", methods=["POST"])
@admin_required
def admin_delete_element(element_id):
    database.delete_element(element_id)
    flash(f"Element #{element_id} deleted successfully.", "success")
    return redirect(url_for("admin"))


# --- Belief CRUD ---
@app.route("/admin/belief/add", methods=["POST"])
@admin_required
def admin_add_belief():
    element_id = request.form.get("element_id")
    belief_text = request.form.get("belief_text", "").strip()
    science_text = request.form.get("science_text", "").strip()

    if element_id and belief_text and science_text:
        database.add_belief(int(element_id), belief_text, science_text)
        flash("Tradition vs Science card added successfully!", "success")
    else:
        flash("Please complete all belief and science fields.", "error")
    return redirect(url_for("admin"))


@app.route("/admin/belief/edit/<int:belief_id>", methods=["GET", "POST"])
@admin_required
def admin_edit_belief(belief_id):
    belief = database.get_belief_by_id(belief_id)
    if not belief:
        flash("Belief record not found.", "error")
        return redirect(url_for("admin"))

    elements = database.get_all_elements()

    if request.method == "POST":
        element_id = request.form.get("element_id")
        belief_text = request.form.get("belief_text", "").strip()
        science_text = request.form.get("science_text", "").strip()

        if element_id and belief_text and science_text:
            database.update_belief(belief_id, int(element_id), belief_text, science_text)
            flash("Belief record successfully updated!", "success")
            return redirect(url_for("admin"))
        else:
            flash("All fields are required.", "error")

    return render_template(
        "admin_edit.html",
        item_type="belief",
        item=belief,
        elements=elements,
        active_page="admin"
    )


@app.route("/admin/belief/delete/<int:belief_id>", methods=["POST"])
@admin_required
def admin_delete_belief(belief_id):
    database.delete_belief(belief_id)
    flash(f"Belief entry #{belief_id} deleted successfully.", "success")
    return redirect(url_for("admin"))


# --- Festival CRUD ---
@app.route("/admin/festival/add", methods=["POST"])
@admin_required
def admin_add_festival():
    name = request.form.get("name", "").strip()
    month = request.form.get("month", "").strip()
    element_id = request.form.get("element_id")
    description = request.form.get("description", "").strip()

    if name and month and description:
        elem_val = int(element_id) if element_id else None
        database.add_festival(name, month, elem_val, description)
        flash(f"Festival '{name}' added successfully!", "success")
    else:
        flash("Please complete all required festival fields.", "error")
    return redirect(url_for("admin"))


@app.route("/admin/festival/edit/<int:festival_id>", methods=["GET", "POST"])
@admin_required
def admin_edit_festival(festival_id):
    festival = database.get_festival_by_id(festival_id)
    if not festival:
        flash("Festival not found.", "error")
        return redirect(url_for("admin"))

    elements = database.get_all_elements()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        month = request.form.get("month", "").strip()
        element_id = request.form.get("element_id")
        description = request.form.get("description", "").strip()

        if name and month and description:
            elem_val = int(element_id) if element_id else None
            database.update_festival(festival_id, name, month, elem_val, description)
            flash(f"Festival '{name}' updated successfully!", "success")
            return redirect(url_for("admin"))
        else:
            flash("All fields are required.", "error")

    return render_template(
        "admin_edit.html",
        item_type="festival",
        item=festival,
        elements=elements,
        active_page="admin"
    )


@app.route("/admin/festival/delete/<int:festival_id>", methods=["POST"])
@admin_required
def admin_delete_festival(festival_id):
    database.delete_festival(festival_id)
    flash(f"Festival #{festival_id} deleted successfully.", "success")
    return redirect(url_for("admin"))


# --- Quiz Question CRUD ---
@app.route("/admin/quiz/add", methods=["POST"])
@admin_required
def admin_add_quiz():
    question = request.form.get("question", "").strip()
    option_a = request.form.get("option_a", "").strip()
    option_b = request.form.get("option_b", "").strip()
    option_c = request.form.get("option_c", "").strip()
    option_d = request.form.get("option_d", "").strip()
    correct_option = request.form.get("correct_option", "A").strip()
    explanation = request.form.get("explanation", "").strip()

    if question and option_a and option_b and option_c and option_d and explanation:
        database.add_quiz_question(
            question, option_a, option_b, option_c, option_d, correct_option, explanation
        )
        flash("Quiz question successfully added!", "success")
    else:
        flash("Please provide question text, all four options, and explanation.", "error")
    return redirect(url_for("admin"))


@app.route("/admin/quiz/edit/<int:question_id>", methods=["GET", "POST"])
@admin_required
def admin_edit_quiz(question_id):
    q = database.get_quiz_question_by_id(question_id)
    if not q:
        flash("Quiz question not found.", "error")
        return redirect(url_for("admin"))

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        option_a = request.form.get("option_a", "").strip()
        option_b = request.form.get("option_b", "").strip()
        option_c = request.form.get("option_c", "").strip()
        option_d = request.form.get("option_d", "").strip()
        correct_option = request.form.get("correct_option", "A").strip()
        explanation = request.form.get("explanation", "").strip()

        if question and option_a and option_b and option_c and option_d and explanation:
            database.update_quiz_question(
                question_id, question, option_a, option_b, option_c, option_d, correct_option, explanation
            )
            flash("Quiz question updated successfully!", "success")
            return redirect(url_for("admin"))
        else:
            flash("All fields are required.", "error")

    return render_template(
        "admin_edit.html",
        item_type="quiz",
        item=q,
        active_page="admin"
    )


@app.route("/admin/quiz/delete/<int:question_id>", methods=["POST"])
@admin_required
def admin_delete_quiz(question_id):
    database.delete_quiz_question(question_id)
    flash(f"Quiz question #{question_id} deleted successfully.", "success")
    return redirect(url_for("admin"))


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        "base.html",
        content="""
        <div class="container" style="text-align: center; padding: 80px 20px;">
          <h1 style="font-size: 3rem; color: var(--green-deep); margin-bottom: 12px;">404</h1>
          <h2 style="margin-bottom: 16px;">Nature Element or Page Not Found</h2>
          <p style="color: var(--text-muted); margin-bottom: 24px;">The path you ventured into has returned to the wilderness.</p>
          <a href="/" class="btn btn-primary">&larr; Return Home</a>
        </div>
        """
    ), 404


@app.errorhandler(500)
def server_error(e):
    return render_template(
        "base.html",
        content="""
        <div class="container" style="text-align: center; padding: 80px 20px;">
          <h1 style="font-size: 3rem; color: var(--terracotta); margin-bottom: 12px;">500</h1>
          <h2 style="margin-bottom: 16px;">Internal Server Error</h2>
          <p style="color: var(--text-muted); margin-bottom: 24px;">An unexpected error occurred. Please try again later.</p>
          <a href="/" class="btn btn-primary">&larr; Return Home</a>
        </div>
        """
    ), 500


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import sys
    # Ensure UTF-8 output encoding on Windows console
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Ensure database tables exist and are seeded with rich data
    database.init_db()
    database.seed_db()
    print("=" * 60)
    print("Prakriti: Nature & Belief Explorer Server Starting...")
    print("Local Address: http://127.0.0.1:5000")
    print("Admin Login:   http://127.0.0.1:5000/admin/login")
    print("Admin Key:     prakriti2026")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False)
