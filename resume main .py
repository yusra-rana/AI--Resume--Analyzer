import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
from textblob import TextBlob
import re

# Skills database
skills_db = [
    "python", "java", "c++", "sql", "html", "css",
    "machine learning", "data analysis", "git",
    "django", "flask", "javascript"
]

# Read PDF Resume
def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text.lower()

# Analyze Resume
def analyze_resume():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

    if not file_path:
        return

    try:
        text = read_pdf(file_path)

        # Find skills
        found_skills = []
        missing_skills = []

        for skill in skills_db:
            if skill in text:
                found_skills.append(skill)
            else:
                missing_skills.append(skill)

        # Grammar Check
        blob = TextBlob(text)
        corrected = str(blob.correct())

        # ATS Score
        score = int((len(found_skills) / len(skills_db)) * 100)

        # Show Result
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Resume Analysis Report\n")
        result_text.insert(tk.END, f"=========================\n\n")

        result_text.insert(tk.END, f"ATS Score: {score}/100\n\n")

        result_text.insert(tk.END, "Skills Found:\n")
        for skill in found_skills:
            result_text.insert(tk.END, f"✔ {skill}\n")

        result_text.insert(tk.END, "\nMissing Skills:\n")
        for skill in missing_skills:
            result_text.insert(tk.END, f"✘ {skill}\n")

        result_text.insert(tk.END, "\nGrammar Suggestions:\n")
        result_text.insert(tk.END, corrected[:1000])

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Window
root = tk.Tk()
root.title("AI Resume Analyzer")
root.geometry("700x600")
root.config(bg="#f0f0f0")

title = tk.Label(root, text="AI Resume Analyzer", font=("Arial", 20, "bold"), bg="#f0f0f0")
title.pack(pady=10)

btn = tk.Button(root, text="Upload Resume PDF", font=("Arial", 14), command=analyze_resume)
btn.pack(pady=10)

result_text = tk.Text(root, width=80, height=30)
result_text.pack(pady=10)

root.mainloop()
