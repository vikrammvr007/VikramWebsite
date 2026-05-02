from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
import base64
from config import ADMIN_EMAIL
from models.supabase_client import (
    get_person, update_person,
    get_emails, add_email, delete_email,
    get_social_links, upsert_social_link,
    get_skill_categories, add_skill, delete_skill, add_skill_category, delete_skill_category,
    get_experience, add_experience, update_experience, delete_experience,
    add_responsibility, delete_responsibility,
    add_exp_technology, delete_exp_technology,
    get_projects, get_project, add_project, update_project, delete_project,
    get_project_categories, add_project_category, delete_project_category,
    toggle_resume_project,
    add_project_tool, add_project_metric, add_project_algorithm,
    get_certifications, add_certification, delete_certification,
    toggle_resume_certification, update_certification_image,
    add_cert_topic, delete_cert_topic,
    get_education, get_education_by_id, add_education, update_education, delete_education,
    get_soft_skills, add_soft_skill, delete_soft_skill,
)
from models.supabase_client import supabase

admin_bp = Blueprint("admin", __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated


# ── AUTH ─────────────────────────────────────────────────────────────────────
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if res.user:
                session["admin_logged_in"] = True
                session["admin_email"]     = email
                flash("Welcome back!", "success")
                return redirect(url_for("admin.dashboard"))
        except Exception as e:
            flash("Invalid credentials. Try again.", "danger")
    return render_template("login.html")


@admin_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("public.index"))



# ── DASHBOARD ────────────────────────────────────────────────────────────────
@admin_bp.route("/dashboard")
@login_required
def dashboard():
    person       = get_person()
    projects     = get_projects()
    skills       = get_skill_categories()
    certifications = get_certifications()
    education    = get_education()
    soft_skills  = get_soft_skills()
    experience   = get_experience()
    return render_template(
        "admin/dashboard.html",
        person=person,
        projects=projects,
        skills=skills,
        certifications=certifications,
        education=education,
        soft_skills=soft_skills,
        experience=experience,
    )


# ── PROFILE ──────────────────────────────────────────────────────────────────
@admin_bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    person = get_person()
    if request.method == "POST":
        data = {
            "name":    request.form.get("name"),
            "phone":   request.form.get("phone"),
            "role":    request.form.get("role"),
            "summary": request.form.get("summary"),
            "age":     request.form.get("age"),
        }
        update_person(person["id"], data)
        # social links
        for platform in ["github", "linkedin"]:
            url = request.form.get(platform)
            if url:
                upsert_social_link(person["id"], platform, url)
        flash("Profile updated.", "success")
        return redirect(url_for("admin.dashboard"))
    socials = {s["platform"]: s["url"] for s in get_social_links(person["id"])}
    return render_template("admin/edit_profile.html", person=person, socials=socials)


# ── PROJECTS ─────────────────────────────────────────────────────────────────
@admin_bp.route("/add-project", methods=["GET", "POST"])
@login_required
def add_project_route():
    categories = get_project_categories()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add_category":
            add_project_category(request.form.get("category_name"))
            flash("Project category added.", "success")
            return redirect(url_for("admin.add_project_route"))
        else:
            person = get_person()
            data = {
                "person_id":   person["id"],
                "title":       request.form.get("title"),
                "description": request.form.get("description"),
                "category":    request.form.get("category"),
                "github_url":  request.form.get("github_url"),
                "demo_url":    request.form.get("demo_url"),
            }
            res = add_project(data)
            project_id = res.data[0]["id"]
            # tools
            tools = request.form.get("tools", "")
            for t in [x.strip() for x in tools.split(",") if x.strip()]:
                add_project_tool(project_id, t)
            # metrics
            metric_name  = request.form.get("metric_name")
            metric_value = request.form.get("metric_value")
            if metric_name and metric_value:
                add_project_metric(project_id, metric_name, metric_value)
            flash("Project added.", "success")
            return redirect(url_for("admin.dashboard"))
    return render_template("admin/add_project.html", categories=categories)


@admin_bp.route("/delete-project-category/<category_id>")
@login_required
def delete_project_category_route(category_id):
    delete_project_category(category_id)
    flash("Project category deleted. Related projects will need new categories.", "success")
    return redirect(url_for("admin.add_project_route"))


@admin_bp.route("/edit-project/<project_id>", methods=["GET", "POST"])
@login_required
def edit_project_route(project_id):
    project = get_project(project_id)
    if request.method == "POST":
        data = {
            "title":       request.form.get("title"),
            "description": request.form.get("description"),
            "category":    request.form.get("category"),
            "github_url":  request.form.get("github_url"),
            "demo_url":    request.form.get("demo_url"),
        }
        update_project(project_id, data)
        flash("Project updated.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/edit_project.html", project=project)


@admin_bp.route("/delete-project/<project_id>")
@login_required
def delete_project_route(project_id):
    delete_project(project_id)
    flash("Project deleted.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/toggle-resume-project/<project_id>")
@login_required
def toggle_resume_project_route(project_id):
    project = get_project(project_id)
    current = project.get("include_in_resume", True)
    toggle_resume_project(project_id, not current)
    status = "included in" if not current else "excluded from"
    flash(f"'{project['title']}' {status} resume.", "success")
    return redirect(url_for("admin.dashboard"))



# ── SKILLS ───────────────────────────────────────────────────────────────────
@admin_bp.route("/add-skill", methods=["GET", "POST"])
@login_required
def add_skill_route():
    categories = get_skill_categories()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add_category":
            add_skill_category(request.form.get("category_name"))
            flash("Category added.", "success")
        else:
            add_skill(
                request.form.get("category_id"),
                request.form.get("name"),
                int(request.form.get("percentage", 80))
            )
            flash("Skill added.", "success")
        return redirect(url_for("admin.add_skill_route"))
    return render_template("admin/add_skill.html", categories=categories)


@admin_bp.route("/delete-skill/<skill_id>")
@login_required
def delete_skill_route(skill_id):
    delete_skill(skill_id)
    flash("Skill deleted.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/delete-skill-category/<category_id>")
@login_required
def delete_skill_category_route(category_id):
    delete_skill_category(category_id)
    flash("Skill category and all related skills deleted.", "success")
    return redirect(url_for("admin.add_skill_route"))


# ── CERTIFICATIONS ───────────────────────────────────────────────────────────
@admin_bp.route("/add-certification", methods=["GET", "POST"])
@login_required
def add_certification_route():
    if request.method == "POST":
        # Handle certificate image upload
        image_url = None
        cert_image = request.files.get("cert_image")
        if cert_image and cert_image.filename:
            allowed = {"png", "jpg", "jpeg", "gif", "webp"}
            ext = cert_image.filename.rsplit(".", 1)[-1].lower()
            if ext in allowed:
                image_data = cert_image.read()
                if len(image_data) > 5 * 1024 * 1024:  # 5MB limit
                    flash("Image too large. Please upload an image under 5MB.", "danger")
                    return redirect(url_for("admin.add_certification_route"))
                b64 = base64.b64encode(image_data).decode("utf-8")
                image_url = f"data:image/{ext};base64,{b64}"
            else:
                flash("Invalid file type. Please upload PNG, JPG, GIF, or WEBP.", "danger")
                return redirect(url_for("admin.add_certification_route"))

        res = add_certification({
            "name":       request.form.get("name"),
            "platform":   request.form.get("platform"),
            "duration":   request.form.get("duration"),
            "start_date": request.form.get("start_date") or None,
            "image_url":  image_url,
        })
        cert_id = res.data[0]["id"]
        # Add topics if provided
        topics = request.form.get("topics", "")
        if topics:
            for idx, topic in enumerate([t.strip() for t in topics.split(",") if t.strip()], start=1):
                add_cert_topic(cert_id, topic, idx)
        flash("Certification added.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/add_certification.html")


@admin_bp.route("/upload-cert-image/<cert_id>", methods=["POST"])
@login_required
def upload_cert_image_route(cert_id):
    cert_image = request.files.get("cert_image")
    if cert_image and cert_image.filename:
        allowed = {"png", "jpg", "jpeg", "gif", "webp"}
        ext = cert_image.filename.rsplit(".", 1)[-1].lower()
        if ext not in allowed:
            flash("Invalid file type. Please upload PNG, JPG, GIF, or WEBP.", "danger")
            return redirect(url_for("admin.dashboard"))
        image_data = cert_image.read()
        if len(image_data) > 5 * 1024 * 1024:
            flash("Image too large. Please upload an image under 5MB.", "danger")
            return redirect(url_for("admin.dashboard"))
        b64 = base64.b64encode(image_data).decode("utf-8")
        image_url = f"data:image/{ext};base64,{b64}"
        update_certification_image(cert_id, image_url)
        flash("Certificate image uploaded.", "success")
    else:
        flash("No image selected.", "danger")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/delete-certification/<cert_id>")
@login_required
def delete_certification_route(cert_id):
    delete_certification(cert_id)
    flash("Certification deleted.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/toggle-resume-certification/<cert_id>")
@login_required
def toggle_resume_certification_route(cert_id):
    certs = get_certifications()
    cert  = next((c for c in certs if c["id"] == cert_id), None)
    if cert:
        current = cert.get("include_in_resume", True)
        toggle_resume_certification(cert_id, not current)
        status = "included in" if not current else "excluded from"
        flash(f"'{cert['name']}' {status} resume.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/add-cert-topic/<cert_id>", methods=["POST"])
@login_required
def add_cert_topic_route(cert_id):
    topic = request.form.get("topic")
    sort_order = int(request.form.get("sort_order", 99))
    add_cert_topic(cert_id, topic, sort_order)
    flash("Topic added.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/delete-cert-topic/<topic_id>")
@login_required
def delete_cert_topic_route(topic_id):
    delete_cert_topic(topic_id)
    flash("Topic deleted.", "success")
    return redirect(url_for("admin.dashboard"))


# ── EDUCATION ────────────────────────────────────────────────────────────────
@admin_bp.route("/add-education", methods=["GET", "POST"])
@login_required
def add_education_route():
    if request.method == "POST":
        add_education({
            "degree":     request.form.get("degree"),
            "institution":request.form.get("institution"),
            "place":      request.form.get("place"),
            "year":       request.form.get("year") or None,
            "percentage": request.form.get("percentage") or None,
            "status":     request.form.get("status") or None,
            "sort_order": int(request.form.get("sort_order", 99)),
        })
        flash("Education added.", "success")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/add_education.html")


@admin_bp.route("/edit-education/<edu_id>", methods=["GET", "POST"])
@login_required
def edit_education_route(edu_id):
    if request.method == "POST":
        update_education(edu_id, {
            "degree":     request.form.get("degree"),
            "institution":request.form.get("institution"),
            "place":      request.form.get("place"),
            "year":       request.form.get("year") or None,
            "percentage": request.form.get("percentage") or None,
            "status":     request.form.get("status") or None,
            "sort_order": int(request.form.get("sort_order", 99)),
        })
        flash("Education updated.", "success")
        return redirect(url_for("admin.dashboard"))
    
    education = get_education_by_id(edu_id)
    return render_template("admin/edit_education.html", education=education)


@admin_bp.route("/delete-education/<edu_id>")
@login_required
def delete_education_route(edu_id):
    delete_education(edu_id)
    flash("Education deleted.", "success")
    return redirect(url_for("admin.dashboard"))


# ── SOFT SKILLS ──────────────────────────────────────────────────────────────
@admin_bp.route("/add-soft-skill", methods=["POST"])
@login_required
def add_soft_skill_route():
    add_soft_skill(request.form.get("name"))
    flash("Soft skill added.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/delete-soft-skill/<skill_id>")
@login_required
def delete_soft_skill_route(skill_id):
    delete_soft_skill(skill_id)
    flash("Soft skill deleted.", "success")
    return redirect(url_for("admin.dashboard"))



# ── EXPERIENCE ───────────────────────────────────────────────────────────────
@admin_bp.route("/manage-experience")
@login_required
def manage_experience():
    experience = get_experience()
    return render_template("admin/manage_experience.html", experience=experience)


@admin_bp.route("/add-experience", methods=["POST"])
@login_required
def add_experience_route():
    person = get_person()
    data = {
        "person_id":  person["id"],
        "role":       request.form.get("role"),
        "company":    request.form.get("company"),
        "start_year": request.form.get("start_year") or None,
        "end_year":   request.form.get("end_year") or None,
        "duration":   request.form.get("duration") or None,
    }
    add_experience(data)
    flash("Job added.", "success")
    return redirect(url_for("admin.manage_experience"))


@admin_bp.route("/edit-experience/<exp_id>", methods=["POST"])
@login_required
def edit_experience_route(exp_id):
    update_experience(exp_id, {
        "role":       request.form.get("role"),
        "company":    request.form.get("company"),
        "start_year": request.form.get("start_year") or None,
        "end_year":   request.form.get("end_year") or None,
        "duration":   request.form.get("duration") or None,
    })
    flash("Experience updated.", "success")
    return redirect(url_for("admin.manage_experience"))


@admin_bp.route("/delete-experience/<exp_id>")
@login_required
def delete_experience_route(exp_id):
    delete_experience(exp_id)
    flash("Job deleted.", "success")
    return redirect(url_for("admin.manage_experience"))


@admin_bp.route("/add-responsibility/<exp_id>", methods=["POST"])
@login_required
def add_responsibility_route(exp_id):
    add_responsibility(exp_id, request.form.get("description"))
    flash("Responsibility added.", "success")
    return redirect(url_for("admin.manage_experience"))


@admin_bp.route("/delete-responsibility/<resp_id>")
@login_required
def delete_responsibility_route(resp_id):
    delete_responsibility(resp_id)
    flash("Responsibility deleted.", "success")
    return redirect(url_for("admin.manage_experience"))


@admin_bp.route("/add-exp-technology/<exp_id>", methods=["POST"])
@login_required
def add_exp_technology_route(exp_id):
    add_exp_technology(exp_id, request.form.get("name"))
    flash("Technology added.", "success")
    return redirect(url_for("admin.manage_experience"))


@admin_bp.route("/delete-exp-technology/<tech_id>")
@login_required
def delete_exp_technology_route(tech_id):
    delete_exp_technology(tech_id)
    flash("Technology deleted.", "success")
    return redirect(url_for("admin.manage_experience"))
