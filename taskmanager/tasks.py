from celery import shared_task


@shared_task
def check_deadlines():
    from .models import Task
    from datetime import date

    today = date.today()
    overdue_tasks = Task.objects.filter(
        deadline__lt=today,
        status__in=['pending', 'in_progress']
    )

    for task in overdue_tasks:
        print(f"OVERDUE TASK: {task.title} - Deadline was {task.deadline} - User: {task.user.username}")

    return f"{overdue_tasks.count()} overdue tasks found"