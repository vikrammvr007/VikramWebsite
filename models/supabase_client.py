from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ── PERSON ──────────────────────────────────────────────────────────────────
def get_person():
    res = supabase.table("persons").select("*").limit(1).execute()
    return res.data[0] if res.data else {}

def update_person(person_id, data):
    return supabase.table("persons").update(data).eq("id", person_id).execute()


# ── EMAILS ───────────────────────────────────────────────────────────────────
def get_emails(person_id):
    return supabase.table("emails").select("*").eq("person_id", person_id).execute().data

def add_email(person_id, email):
    return supabase.table("emails").insert({"person_id": person_id, "email": email}).execute()

def delete_email(email_id):
    return supabase.table("emails").delete().eq("id", email_id).execute()


# ── SOCIAL LINKS ─────────────────────────────────────────────────────────────
def get_social_links(person_id):
    return supabase.table("social_links").select("*").eq("person_id", person_id).execute().data

def upsert_social_link(person_id, platform, url):
    existing = supabase.table("social_links").select("id").eq("person_id", person_id).eq("platform", platform).execute().data
    if existing:
        return supabase.table("social_links").update({"url": url}).eq("id", existing[0]["id"]).execute()
    return supabase.table("social_links").insert({"person_id": person_id, "platform": platform, "url": url}).execute()


# ── SKILLS ───────────────────────────────────────────────────────────────────
def get_skill_categories():
    return supabase.table("skill_categories").select("*, skills(*)").execute().data

def add_skill(category_id, name, percentage):
    return supabase.table("skills").insert({"category_id": category_id, "name": name, "percentage": percentage}).execute()

def delete_skill(skill_id):
    return supabase.table("skills").delete().eq("id", skill_id).execute()

def add_skill_category(name):
    return supabase.table("skill_categories").insert({"name": name}).execute()

def delete_skill_category(category_id):
    return supabase.table("skill_categories").delete().eq("id", category_id).execute()


# ── WORK EXPERIENCE ──────────────────────────────────────────────────────────
def get_experience():
    exp = supabase.table("work_experience").select("*").execute().data
    for e in exp:
        e["responsibilities"] = supabase.table("experience_responsibilities").select("*").eq("experience_id", e["id"]).execute().data
        e["technologies"]     = supabase.table("experience_technologies").select("*").eq("experience_id", e["id"]).execute().data
    return exp

def add_experience(data):
    return supabase.table("work_experience").insert(data).execute()

def update_experience(exp_id, data):
    return supabase.table("work_experience").update(data).eq("id", exp_id).execute()

def delete_experience(exp_id):
    supabase.table("experience_responsibilities").delete().eq("experience_id", exp_id).execute()
    supabase.table("experience_technologies").delete().eq("experience_id", exp_id).execute()
    return supabase.table("work_experience").delete().eq("id", exp_id).execute()

def add_responsibility(exp_id, text):
    return supabase.table("experience_responsibilities").insert({"experience_id": exp_id, "description": text}).execute()

def delete_responsibility(resp_id):
    return supabase.table("experience_responsibilities").delete().eq("id", resp_id).execute()

def add_exp_technology(exp_id, name):
    return supabase.table("experience_technologies").insert({"experience_id": exp_id, "name": name}).execute()

def delete_exp_technology(tech_id):
    return supabase.table("experience_technologies").delete().eq("id", tech_id).execute()


# ── PROJECTS ─────────────────────────────────────────────────────────────────
def get_project_categories():
    return supabase.table("project_categories").select("*").order("name").execute().data

def add_project_category(name):
    return supabase.table("project_categories").insert({"name": name}).execute()

def delete_project_category(category_id):
    return supabase.table("project_categories").delete().eq("id", category_id).execute()

def _enrich_project(p):
    pid = p["id"]
    p["metrics"]    = supabase.table("project_metrics").select("*").eq("project_id", pid).execute().data
    p["tools"]      = supabase.table("project_tools").select("*").eq("project_id", pid).execute().data
    p["algorithms"] = supabase.table("project_algorithms").select("*").eq("project_id", pid).execute().data
    return p

def get_projects():
    return [_enrich_project(p) for p in supabase.table("projects").select("*").execute().data]

def get_resume_projects():
    """Only projects marked include_in_resume = true."""
    return [_enrich_project(p) for p in supabase.table("projects").select("*").eq("include_in_resume", True).execute().data]

def toggle_resume_project(project_id, include):
    return supabase.table("projects").update({"include_in_resume": include}).eq("id", project_id).execute()

def get_project(project_id):
    data = supabase.table("projects").select("*").eq("id", project_id).execute().data
    return _enrich_project(data[0]) if data else None

def add_project(data):
    return supabase.table("projects").insert(data).execute()

def update_project(project_id, data):
    return supabase.table("projects").update(data).eq("id", project_id).execute()

def delete_project(project_id):
    supabase.table("project_metrics").delete().eq("project_id", project_id).execute()
    supabase.table("project_tools").delete().eq("project_id", project_id).execute()
    supabase.table("project_algorithms").delete().eq("project_id", project_id).execute()
    return supabase.table("projects").delete().eq("id", project_id).execute()

def add_project_tool(project_id, name):
    return supabase.table("project_tools").insert({"project_id": project_id, "name": name}).execute()

def add_project_metric(project_id, metric_name, value):
    return supabase.table("project_metrics").insert({"project_id": project_id, "metric_name": metric_name, "value": value}).execute()

def add_project_algorithm(project_id, name):
    return supabase.table("project_algorithms").insert({"project_id": project_id, "name": name}).execute()


# ── CERTIFICATIONS ───────────────────────────────────────────────────────────
def get_certifications():
    certs = supabase.table("certifications").select("*").execute().data
    for cert in certs:
        cert["topics"] = supabase.table("certification_topics").select("*").eq("cert_id", cert["id"]).order("sort_order").execute().data
    return certs

def get_resume_certifications():
    certs = supabase.table("certifications").select("*").eq("include_in_resume", True).execute().data
    for cert in certs:
        cert["topics"] = supabase.table("certification_topics").select("*").eq("cert_id", cert["id"]).order("sort_order").execute().data
    return certs

def toggle_resume_certification(cert_id, include):
    return supabase.table("certifications").update({"include_in_resume": include}).eq("id", cert_id).execute()

def add_certification(data):
    return supabase.table("certifications").insert(data).execute()

def update_certification_image(cert_id, image_url):
    return supabase.table("certifications").update({"image_url": image_url}).eq("id", cert_id).execute()

def delete_certification(cert_id):
    supabase.table("certification_topics").delete().eq("cert_id", cert_id).execute()
    return supabase.table("certifications").delete().eq("id", cert_id).execute()

def add_cert_topic(cert_id, topic, sort_order=99):
    return supabase.table("certification_topics").insert({"cert_id": cert_id, "topic": topic, "sort_order": sort_order}).execute()

def delete_cert_topic(topic_id):
    return supabase.table("certification_topics").delete().eq("id", topic_id).execute()


# ── EDUCATION ────────────────────────────────────────────────────────────────
def get_education():
    return supabase.table("education").select("*").order("sort_order").execute().data

def get_education_by_id(edu_id):
    result = supabase.table("education").select("*").eq("id", edu_id).execute().data
    return result[0] if result else None

def add_education(data):
    return supabase.table("education").insert(data).execute()

def update_education(edu_id, data):
    return supabase.table("education").update(data).eq("id", edu_id).execute()

def delete_education(edu_id):
    return supabase.table("education").delete().eq("id", edu_id).execute()


# ── SOFT SKILLS ──────────────────────────────────────────────────────────────
def get_soft_skills():
    return supabase.table("soft_skills").select("*").execute().data

def add_soft_skill(name):
    return supabase.table("soft_skills").insert({"name": name}).execute()

def delete_soft_skill(skill_id):
    return supabase.table("soft_skills").delete().eq("id", skill_id).execute()
