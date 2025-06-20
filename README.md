# AI-INTERVIEW-BOT-FOR-FRESHERS
AI Interview Bot Project

AI-Powered Voice-Based Interview Bot with Resume Scanner
What this project does:
1. user upload their resume (`PDF` or `DOCX`)
2. Scans the resume for skills and projects
3. Asks voice questions based on the resume skills
4. Records the interview video from the webcam
5. 📝 Saves a transcript of Q\&A
6.  Sends resume + transcript to HR via email
7. Allows the user to watch their recorded interview video

 Folder Structure (after running):
AI Interview Bot
│
├── resume_uploaded.pdf                   ← Uploaded resume (copied here)
├── interview_record.avi                       ← Video recorded from webcam
├── interview_transcript.txt                ← Questions, answers & final score
├── your_script.py                                   ← Main Python script
└── README.txt                                          ← This instruction file
Technologies Used:
* 🐍 Python
* 🎤 `speech recognition` for voice input
* 🗣️ `pyttsx3` for text-to-speech
* 📄 `pdf plumber` and `docx` for reading resumes
* 🤖 `re` and `custom logic` for skill & project extraction
* 🎥 `OpenCV` (`cv2`) for video recording
* 🧵 `threading` to record video and ask questions at the same time
* 💌 `smtplib`, `ssl`, and `email` for sending mail
* 🪟 `tkinter` for GUI
* 🖥️ Built to run on Windows 

How to Run This Project:

1. ✅ Install all required packages:
pip install pyttsx3 speechrecognition pdfplumber python-docx opencv-python
2. ✅ Replace the email and password in this section of code:

Python(you want to cange this in code)

sender_email = "your_email@gmail.com"
sender_password = "your_password"
receiver_email = "hr_email@example.com"
3. ✅ Run the Python file:
python your_script.py
4. ✅ A GUI window will open automatically:
  * Click Upload Resume
   * Interview will start
   * After 10 minutes, report is sent to HR
 Features:
* 🎯 Skill-specific questions
* 🤖 Friendly female voice
* 📝 Real-time Q\&A recording
* 📹 Webcam-based video recording
* 📧 One-click automated email to HR
* 🗂️ All interview data saved in one place
 Important:
* Do not share your Gmail password in public code
* If Gmail blocks login, enable “App Passwords” or “Less Secure App Access”
 How to Stop the App:

* Close the GUI window, or press `Ctrl + C` in terminal
 Output Sent to HR Includes:
* ✅ Uploaded Resume (`resume_uploaded.pdf`)
* ✅ Q\&A Transcript (`interview_transcript.txt`)
Who can use this:

* Students preparing for interviews
* HRs who want to pre-screen candidates
* Developers learning AI + voice + email automation.
