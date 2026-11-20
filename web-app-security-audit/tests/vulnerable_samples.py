# Test fixture containing intentional vulnerable Python (Django, FastAPI, Flask) patterns

# 1. Django DEBUG mode in production
DEBUG = True

# 2. Django mark_safe with user input (XSS)
def view_comment(request):
    safe_bio = mark_safe("<p>" + request.GET['bio'] + "</p>")
    return safe_bio

# 3. Raw SQL with f-string in Django ORM
def get_user(request):
    username = request.GET['user']
    users = User.objects.raw(f"SELECT * FROM users WHERE username = '{username}'")
    return users

# 4. Insecure Deserialization with pickle
def load_session(data):
    return pickle.loads(data)

# 5. Flask Jinja2 SSTI via render_template_string
def greet_user(name):
    return render_template_string(f"Hello {name}!")

# 6. Command injection via os.system
def ping_server(host):
    os.system("ping -c 1 " + host)
