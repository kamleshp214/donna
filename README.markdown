# DONNA: Your Sassy Task Assistant

Inspired by the sharp and witty Donna Paulsen from *Suits*, DONNA is a text-based AI assistant built in Python to manage your tasks with flair. She runs locally on your laptop, sends Windows notifications for due tasks, and delivers sassy responses to keep you motivated (or mildly roasted). Perfect for introverts who prefer a CLI over voice commands, DONNA is your go-to for staying organized with style.

## Features

- **Task Management**: Add, list, delete, and complete tasks with descriptions, due dates, and priorities.
- **Windows Notifications**: Get timely pop-up reminders for due tasks, labeled with DONNA’s name.
- **Sassy Personality**: Enjoy witty, *Suits*-style responses like “Task added. What’s next, world domination?”
- **Local Storage**: Tasks are stored in a simple `tasks.json` file—no internet required.
- **Command-Line Interface**: Fully text-based, introvert-friendly interaction.

## Demo

![DONNA in action](demo.gif) *(Add a screen recording of DONNA’s CLI and notification to your repo for this!)*

Example interaction:
```
> add task Hack the mainframe like a pro by 2025-05-20 20:21 with epic priority
Task added. What’s next, world domination?

> list tasks
Your tasks:
1. Hack the mainframe like a pro (Due: 2025-05-20 20:21, Priority: epic, pending)

Here’s your chaos, neatly listed. You’re welcome.
```

At 20:21, a Windows notification pops up: “DONNA: Reminder: Hack the mainframe like a pro”.

## Installation

1. **Prerequisites**:
   - Python 3.6+ (tested on Python 3.11)
   - Git
   - Windows OS (for notifications)

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/kamleshp214/donna.git
   cd donna
   ```

3. **Install Dependencies**:
   ```bash
   pip install win10toast
   ```

## Usage

1. **Run DONNA**:
   ```bash
   python donna.py
   ```

2. **Available Commands**:
   - `add task <description> by <YYYY-MM-DD HH:MM> with <priority>`: Add a task (e.g., `add task Write code by 2025-05-20 20:30 with high`).
   - `list tasks`: Show all tasks with due dates, priorities, and status.
   - `delete task <id>`: Remove a task by ID.
   - `complete task <id>`: Mark a task as completed.
   - `check reminders`: List tasks due now or soon.
   - `help`: Display all commands.
   - `exit`: Close DONNA.

3. **Notifications**:
   - Keep the CLI running to receive Windows notifications for due tasks.
   - Tasks are marked as completed after notification.

## Project Structure

- `donna.py`: Main script with CLI and notification logic.
- `tasks.json`: Stores tasks (auto-created on first use).

## Example `tasks.json`

```json
[
    {
        "id": 1,
        "description": "Hack the mainframe like a pro",
        "due": "2025-05-20T20:21:00",
        "priority": "epic",
        "status": "pending"
    }
]
```

## Contributing

Feel free to fork, submit issues, or send pull requests to add features like recurring tasks or a GUI. Let’s make DONNA even sassier!

## License

MIT License. See [LICENSE](LICENSE) for details.

## About

Built by Kamlesh Prajapat as a fun side project to bring *Suits*’ Donna to life as a task manager. Connect with me on [LinkedIn](https://www.linkedin.com/in/kamleshp214) to chat about Python, automation, or witty AI assistants!