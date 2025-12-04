from flask import Flask, request, render_template, redirect, url_for
from models import Task, db
from datetime import datetime


def create_task(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    # Add The Tasks

    @app.route("/add_task", methods=["GET", "POST"])
    def add_task():
        if request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            deadline = request.form.get("deadline")
            category = request.form.get("category")
            status = request.form.get("status")

            # Convert deadline to Python date
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()

            new_task = Task(
                title=title,
                description=description,
                deadline=deadline_date,
                category=category,
                status=status,
            )

            db.session.add(new_task)
            db.session.commit()

            return redirect(url_for("add_task"))

        return render_template("add_task.html")

    # Edit the tasks

    @app.route("/edit_task", methods=["GET", "POST"])
    def edit_task():
        tasks = Task.query.all()
        return render_template("edit_task.html", tasks=tasks)

    @app.route("/update_task", methods=["POST"])
    def update_task():
        task_id = request.form.get("id")
        task = Task.query.get(task_id)

        if task:
            task.title = request.form.get("title")
            task.description = request.form.get("description")
            task.deadline = datetime.strptime(
                request.form.get("deadline"), "%Y-%m-%d"
            ).date()
            task.category = request.form.get("category")
            task.status = request.form.get("status")

            db.session.commit()

        return redirect(url_for("edit_task"))

    # Show all tasks

    @app.route("/show_tasks")
    def show_tasks():
        
        # Get filter parameters from query string
        status_filter = request.args.get("status")
        sort_order = request.args.get("sort")

        tasks_query = Task.query

        # Filter by status
        if status_filter and status_filter != "all":
            tasks_query = tasks_query.filter_by(status=status_filter)

        # Sort by deadline
        if sort_order == "new_to_old":
            tasks_query = tasks_query.order_by(Task.deadline.desc())
        elif sort_order == "old_to_new":
            tasks_query = tasks_query.order_by(Task.deadline.asc())

        tasks = tasks_query.all()
        return render_template("tasks_detail.html", tasks=tasks, status_filter=status_filter, sort_order=sort_order)


    # Delete the tasks

    @app.route("/delete_task/<int:task_id>", methods=["POST"])
    def delete_task(task_id):
        task = Task.query.get(task_id)

        if task:
            db.session.delete(task)
            db.session.commit()

        return redirect(url_for("show_tasks"))
