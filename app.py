from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret"

tasks = []
completed_tasks = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Mini Task Manager</title>
    <link rel="icon" type="image/png" href="/static/favicon.ico">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

    <style>
        * {
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }

        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
        }

        /* Toast */
        .toast {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%) translateY(-20px);
            background: rgba(34, 197, 94, 0.95);
            color: white;
            padding: 12px 20px;
            border-radius: 10px;
            font-size: 14px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            opacity: 0;
            animation: slideDown 0.4s ease forwards;
        }

        @keyframes slideDown {
            to {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
        }

        .toast.hide {
            animation: fadeOut 0.8s ease forwards;
        }

        @keyframes fadeOut {
            to {
                opacity: 0;
                transform: translateX(-50%) translateY(-20px);
            }
        }

        .card {
            width: 520px;
            padding: 32px;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
            color: white;
        }

        .logo {
            text-align: center;
            margin-bottom: 20px;
        }

        .logo img {
            height: 40px;
        }

        h2 {
            font-size: 14px;
            margin-top: 24px;
            margin-bottom: 8px;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        form {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            padding: 10px;
            border-radius: 8px;
            border: none;
            outline: none;
        }

        .btn-primary {
            background: white;
            color: #111827;
            border-radius: 8px;
            padding: 10px 14px;
            border: none;
            font-weight: 500;
            cursor: pointer;
        }

        ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        li {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.18);
            padding: 10px 12px;
            border-radius: 12px;
            margin-bottom: 8px;
        }

        .actions {
            display: flex;
            gap: 10px;
        }

        .icon-btn {
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 8px;
            padding: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .icon-btn svg {
            width: 16px;
            height: 16px;
            stroke: white;
        }

        .completed span {
            text-decoration: line-through;
            opacity: 0.7;
        }

        .empty {
            opacity: 0.6;
            font-size: 14px;
        }

        .edit-form {
            display: flex;
            gap: 6px;
            width: 100%;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .header h1 {
            font-size: 20px;
            font-weight: 600;
            margin: 0;
            color: white;
        }

        .header img {
            height: 28px;
            opacity: 0.9;
        }

    </style>
</head>
<body>

{% with messages = get_flashed_messages() %}
    {% if messages %}
        <div id="toast" class="toast">
            {{ messages[0] }}
        </div>
    {% endif %}
{% endwith %}

<div class="card">

    <div class="header">
        <h1>Task Manager</h1>
        <img src="{{ url_for('static', filename='testdino-logo.png') }}" alt="TestDino Logo">
    </div>

    <form method="POST" action="/add">
        <input type="text" name="task" placeholder="Enter task" required>
        <button type="submit" class="btn-primary">Add</button>
    </form>

    <h2>To Do</h2>
    <ul>
        {% if tasks %}
            {% for task in tasks %}
                <li>
                    {% if edit_index == loop.index0 %}
                        <form method="POST" action="/update/{{ loop.index0 }}" class="edit-form">
                            <input type="text" name="updated_task" value="{{ task }}" required>
                            <button type="submit" class="btn-primary">Save</button>
                        </form>
                    {% else %}
                        <span>{{ task }}</span>
                        <div class="actions">
                            <a href="/complete/{{ loop.index0 }}" class="icon-btn">
                                <svg fill="none" viewBox="0 0 24 24" stroke-width="2">
                                    <path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </a>

                            <a href="/edit/{{ loop.index0 }}" class="icon-btn">
                                <svg fill="none" viewBox="0 0 24 24" stroke-width="2">
                                    <path d="M4 20l4-1 9-9-3-3-9 9-1 4z" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </a>
                        </div>
                    {% endif %}
                </li>
            {% endfor %}
        {% else %}
            <li class="empty">No pending tasks</li>
        {% endif %}
    </ul>

    <h2>Completed</h2>
    <ul>
        {% if completed_tasks %}
            {% for task in completed_tasks %}
                <li class="completed">
                    <span>{{ task }}</span>
                    <a href="/delete_completed/{{ loop.index0 }}" class="icon-btn">
                        <svg fill="none" viewBox="0 0 24 24" stroke-width="2">
                            <path d="M3 6h18" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M8 6V4h8v2" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M19 6l-1 14H6L5 6" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M10 11v6M14 11v6" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </a>
                </li>
            {% endfor %}
        {% else %}
            <li class="empty">Nothing completed yet</li>
        {% endif %}
    </ul>

</div>

<script>
    const toast = document.getElementById("toast");

    if (toast) {
        setTimeout(() => {
            toast.classList.add("hide");

            setTimeout(() => {
                toast.remove();
            }, 400);

        }, 2500);
    }
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML,
        tasks=tasks,
        completed_tasks=completed_tasks,
        edit_index=None
    )

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        tasks.append(task)
        flash("Task added successfully")
    return redirect(url_for("home"))

@app.route("/complete/<int:index>")
def complete(index):
    if 0 <= index < len(tasks):
        completed_tasks.append(tasks.pop(index))
        flash("Task marked as completed")
    return redirect(url_for("home"))

@app.route("/edit/<int:index>")
def edit(index):
    return render_template_string(
        HTML,
        tasks=tasks,
        completed_tasks=completed_tasks,
        edit_index=index
    )

@app.route("/update/<int:index>", methods=["POST"])
def update(index):
    updated_task = request.form.get("updated_task")
    if 0 <= index < len(tasks) and updated_task:
        tasks[index] = updated_task
        flash("Task updated successfully")
    return redirect(url_for("home"))

@app.route("/delete_completed/<int:index>")
def delete_completed(index):
    if 0 <= index < len(completed_tasks):
        completed_tasks.pop(index)
        flash("Task deleted successfully")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)