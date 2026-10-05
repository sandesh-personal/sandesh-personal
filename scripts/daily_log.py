#!/usr/bin/env python3
"""
Updates data/activity.log with a timestamp and a curated developer quote/tip.
Used by the daily green streak GitHub Action to generate consistent, meaningful contributions.
"""
import datetime
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(HERE, "..", "data", "activity.log")

QUOTES = [
    "Clean code always looks like it was written by someone who cares. — Michael Feathers",
    "Simplicity is prerequisite for reliability. — Edsger W. Dijkstra",
    "Make it work, make it right, make it fast. — Kent Beck",
    "First, solve the problem. Then, write the code. — John Johnson",
    "Experience is the name everyone gives to their mistakes. — Oscar Wilde",
    "Knowledge is power. Code is craft. — Sandesh",
    "Any fool can write code that a computer can understand. Good programmers write code that humans can understand. — Martin Fowler",
    "Premature optimization is the root of all evil. — Donald Knuth",
    "Code is like humor. When you have to explain it, it’s bad. — Cory House",
    "Optimism is an occupational hazard of programming: feedback is the treatment. — Kent Beck",
    "Before software can be reusable it first has to be usable. — Ralph Johnson",
    "Fix the cause, not the symptom. — Steve Maguire",
    "Software is a great combination between artistry & engineering. — Bill Gates",
    "Continuously ship, measure, learn, and iterate. — Sandesh Koirala",
    "Don't comment bad code — rewrite it. — Brian Kernighan"
]

def update_activity():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    quote = random.choice(QUOTES)
    entry = f"[{now}] Streak Check-in: {quote}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
    
    print(f"Logged activity at {now}: {quote}")

if __name__ == "__main__":
    update_activity()
