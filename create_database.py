import sqlite3

# Create and connect to the database
conn = sqlite3.connect('questions.db')
cursor = conn.cursor()

# Create questions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
)
''')

# Insert sample questions
sample_questions = [
    ("Is the sky blue?", "TRUE"),
    ("Do computers use electricity?", "TRUE"),
    ("Can humans breathe underwater?", "FALSE"),
    ("Is Python a programming language?", "TRUE"),
    ("Do cars fly?", "FALSE"),
    ("Is the Earth flat?", "FALSE"),
    ("Does water boil at 100 degrees Celsius?", "TRUE"),
    ("Can fish live without water?", "FALSE")
]

cursor.executemany('''
INSERT INTO questions (question, answer) VALUES (?, ?)
''', sample_questions)

# Commit and close
conn.commit()
conn.close()

print("Database created successfully with sample questions!")