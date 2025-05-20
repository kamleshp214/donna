import json
import os
from datetime import datetime
import random
import threading
import time
from win10toast import ToastNotifier

# Sample responses for DONNA's personality
RESPONSES = {
    "add": ["Task added. What’s next, world domination?", "Noted. Don’t expect me to do it for you."],
    "list": ["Here’s your chaos, neatly listed. You’re welcome.", "Your to-do list. Try not to cry."],
    "complete": ["Done? Impressive. I’ll alert the press.", "Task complete. Took you long enough."],
    "reminder": ["You’ve got a task due soon. Move it!", "Reminder: You’re not done yet. Shocker."],
    "delete": ["Task deleted. Poof, gone!", "Erased it. Hope you didn’t need that."]
}

# Load tasks from JSON and migrate old format if needed
def load_tasks():
    if not os.path.exists("tasks.json"):
        return []
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
    
    # Migrate old tasks to new format
    updated_tasks = []
    for task in tasks:
        new_task = {
            "id": task.get("id", len(updated_tasks) + 1),
            "description": task.get("description", ""),
            "due": task.get("due_time", task.get("due", datetime.now().isoformat())),
            "priority": task.get("priority", "medium"),
            "status": task.get("status", "pending")
        }
        updated_tasks.append(new_task)
    
    # Save migrated tasks
    save_tasks(updated_tasks)
    return updated_tasks

# Save tasks to JSON
def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)

# Add a task
def add_task(desc, due, priority):
    try:
        due_date = datetime.strptime(due, "%Y-%m-%d %H:%M")
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD HH:MM (e.g., 2025-05-20 20:30)."
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "description": desc,
        "due": due_date.isoformat(),
        "priority": priority,
        "status": "pending"
    }
    tasks.append(task)
    save_tasks(tasks)
    return random.choice(RESPONSES["add"])

# List tasks
def list_tasks():
    tasks = load_tasks()
    if not tasks:
        return "No tasks. Slacker."
    output = "Your tasks:\n"
    for task in tasks:
        due_date = datetime.fromisoformat(task['due']).strftime("%Y-%m-%d %H:%M")
        output += f"{task['id']}. {task['description']} (Due: {due_date}, Priority: {task['priority']}, {task['status']})\n"
    return output + "\n" + random.choice(RESPONSES["list"])

# Delete a task
def delete_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == int(task_id)), None)
    if not task:
        return f"No task with ID {task_id}. Try again."
    tasks = [t for t in tasks if t["id"] != int(task_id)]
    save_tasks(tasks)
    return random.choice(RESPONSES["delete"])

# Complete a task
def complete_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == int(task_id)), None)
    if not task:
        return f"No task with ID {task_id}. Try again."
    task["status"] = "completed"
    save_tasks(tasks)
    return random.choice(RESPONSES["complete"])

# Check reminders
def check_reminders():
    tasks = load_tasks()
    now = datetime.now()
    due_soon = [t for t in tasks if t["status"] == "pending" and datetime.fromisoformat(t["due"]) <= now]
    if not due_soon:
        return "No tasks due soon. You’re on top of things... for now."
    output = "Due tasks:\n"
    for task in due_soon:
        due_date = datetime.fromisoformat(task['due']).strftime("%Y-%m-%d %H:%M")
        output += f"{task['id']}. {task['description']} (Due: {due_date}, Priority: {task['priority']})\n"
    return output + "\n" + random.choice(RESPONSES["reminder"])

# Background thread for notifications
def notification_service():
    toaster = ToastNotifier()
    last_mod_time = 0
    while True:
        if os.path.exists("tasks.json"):
            current_mod_time = os.path.getmtime("tasks.json")
            if current_mod_time > last_mod_time:
                tasks = load_tasks()
                last_mod_time = current_mod_time
            else:
                tasks = load_tasks()
        else:
            tasks = []

        now = datetime.now()
        due_tasks = [t for t in tasks if t["status"] == "pending" and datetime.fromisoformat(t["due"]) <= now]
        for task in due_tasks:
            toaster.show_toast("DONNA", f"Reminder: {task['description']}", duration=10)
            task["status"] = "completed"  # Mark as completed after notification
        save_tasks(tasks)

        future_tasks = [t for t in tasks if t["status"] == "pending" and datetime.fromisoformat(t["due"]) > now]
        sleep_time = 60 if not future_tasks else min((datetime.fromisoformat(t["due"]) - now).total_seconds() for t in future_tasks)
        time.sleep(min(sleep_time, 60))

# Main CLI loop
def main():
    print("Welcome to DONNA, your sassy task assistant. Type 'help' for commands.")
    threading.Thread(target=notification_service, daemon=True).start()  # Start notification thread
    while True:
        cmd = input("> ").strip().lower()
        if cmd == "exit":
            print("Goodbye. Try not to fall apart without me.")
            break
        elif cmd.startswith("add task"):
            parts = cmd.split(" by ")
            if len(parts) != 2:
                print("Use: add task <description> by <YYYY-MM-DD HH:MM> with <priority>")
                continue
            desc = parts[0].replace("add task", "").strip()
            due_priority = parts[1].split(" with ")
            if len(due_priority) != 2:
                print("Use: add task <description> by <YYYY-MM-DD HH:MM> with <priority>")
                continue
            due = due_priority[0].strip()
            priority = due_priority[1].strip()
            print(add_task(desc, due, priority))
        elif cmd == "list tasks":
            print(list_tasks())
        elif cmd.startswith("delete task"):
            task_id = cmd.replace("delete task", "").strip()
            print(delete_task(task_id))
        elif cmd.startswith("complete task"):
            task_id = cmd.replace("complete task", "").strip()
            print(complete_task(task_id))
        elif cmd == "check reminders":
            print(check_reminders())
        elif cmd == "help":
            print("Commands:")
            print("  add task <desc> by <YYYY-MM-DD HH:MM> with <priority>  # e.g., add task Write code by 2025-05-20 20:30 with high")
            print("  list tasks")
            print("  delete task <id>")
            print("  complete task <id>")
            print("  check reminders")
            print("  exit")
        else:
            print("Huh? Type 'help' if you’re lost.")

if __name__ == "__main__":
    main()