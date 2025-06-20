import pyttsx3
import speech_recognition as sr
import pdfplumber
import docx
import tkinter as tk
from tkinter import filedialog
import re
import random
import time
import cv2
import threading
import shutil
import smtplib
from email.message import EmailMessage
import ssl
import os

# Text-to-Speech setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
engine.setProperty('rate', 150)

def speak(text):
    print("Bot:", text)
    engine.say(text)
    engine.runAndWait()

def listen(timeout=6, phrase_time_limit=10):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            response = r.recognize_google(audio)
            print("You:", response)
            return response.lower()
        except sr.WaitTimeoutError:
            speak("You took too long to respond.")
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
    return ""

def extract_resume_text(file_path):
    if file_path.endswith(".pdf"):
        try:
            with pdfplumber.open(file_path) as pdf:
                return " ".join([page.extract_text() or "" for page in pdf.pages])
        except Exception as e:
            print("Error reading PDF:", e)
            return ""
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

def extract_keywords(text):
    tech_keywords = ['python', 'java', 'c++', 'c', 'javascript', 'react', 'node.js', 'html', 'css', 'devops', 'cybersecurity']
    return list(set([word for word in tech_keywords if word in text.lower()]))

def extract_projects(text):
    pattern = r'projects?\s*[:\-]?\s*(.*?)(?=experience|skills|education|$)'
    matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
    return [proj.strip() for proj in matches if proj.strip()]

def record_video(stop_event):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('interview_record.avi', fourcc, 20.0, (640, 480))
    while not stop_event.is_set():
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('Recording...', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                stop_event.set()
                break
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def save_transcript(lines, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("AI Interview Transcript\n" + "="*30 + "\n")
        f.write("\n".join(lines) + "\n")

def send_email_with_documents():
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"
    receiver_email = "hr_email@example.com"

    msg = EmailMessage()
    msg['Subject'] = 'Interview Report and Resume'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content("Hi,\n\nPlease find attached the candidate's resume and interview transcript.\n\nRegards,\nAI Bot")

    attachments = ['resume_uploaded.pdf', 'interview_transcript.txt']
    for file in attachments:
        if os.path.exists(file):
            with open(file, 'rb') as f:
                file_data = f.read()
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

def start_gui():
    def upload_resume():
        file_path = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.docx")])
        if not file_path:
            speak("No file selected. Please upload your resume.")
            return

        shutil.copy(file_path, 'resume_uploaded.pdf')
        resume_text = extract_resume_text(file_path)

        if not resume_text.strip():
            speak("Sorry, I couldn't read the resume. Please upload another file.")
            return

        skills = extract_keywords(resume_text)
        projects = extract_projects(resume_text)

        if not skills:
            speak("I couldn't detect any major technologies.")
            return

        speak("Resume uploaded successfully.")
        speak(f"I found these skills: {', '.join(skills)}")
        if projects:
            speak(f"I found these projects: {', '.join(projects[:3])}")

        stop_event = threading.Event()
        recording_thread = threading.Thread(target=record_video, args=(stop_event,))
        recording_thread.start()

        run_interview(skills)

        stop_event.set()
        recording_thread.join()

        speak("Sending your interview report to HR.")
        send_email_with_documents()
        speak("Interview report sent successfully.")

    def run_interview(skills):
        score = 0
        total = 0
        transcript = []
        start_time = time.time()

        for skill in skills:
            if time.time() - start_time > 600:
                break
            questions = question_bank.get(skill, [])
            if not questions:
                continue
            for q in questions[:2]:
                if time.time() - start_time > 600:
                    break
                speak(q)
                transcript.append("Bot: " + q)
                answer = listen()
                transcript.append("User: " + (answer if answer else "No response"))
                if answer:
                    score += 1
                    reply = random.choice(["Good!", "Nice answer!", "Great!"])
                    speak(reply)
                    transcript.append("Bot: " + reply)
                else:
                    speak("Please try to answer next time.")
                    transcript.append("Bot: Please try to answer next time.")
                total += 1

        speak(f"You scored {score} out of {total}")
        result = "Result: " + ("Fit for the interview." if total and score / total >= 0.6 else "Needs improvement.")
        transcript.append("Bot: " + result)
        save_transcript(transcript, 'interview_transcript.txt')

    def play_video():
        cap = cv2.VideoCapture('interview_record.avi')
        if not cap.isOpened():
            speak("Video not found.")
            return
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Recorded Interview', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    root = tk.Tk()
    root.title("AI Interview Bot")
    root.geometry("400x250")

    tk.Label(root, text="Upload Your Resume", font=("Arial", 14)).pack(pady=20)
    tk.Button(root, text="Upload Resume", command=upload_resume).pack(pady=5)
    tk.Button(root, text="Play Interview Video", command=play_video).pack(pady=5)

    root.after(1000, upload_resume)
    root.mainloop()

question_bank = {
    "python": ["What is a Python decorator?", "Explain list comprehension."],
    "java": ["What is JVM?", "Explain OOPs concepts."],
    "c++": ["Difference between C and C++?", "Explain constructors."],
    "html": ["What are semantic tags?", "How to create a table in HTML?"],
    "css": ["What is Flexbox?", "Difference between id and class?"],
    "javascript": ["What is closure?", "What is event bubbling?"],
    "node.js": ["What is middleware in Express?", "Explain Node.js event loop."],
    "devops": ["What is CI/CD?", "Docker vs Virtual Machines?"],
    "cybersecurity": ["What is SQL Injection?", "Hashing vs Encryption?"],
    "c": ["What is a pointer?", "What is a segmentation fault?"]
}

start_gui()
