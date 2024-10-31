import tkinter as tk
from tkinter import filedialog
import PyPDF2
import pytesseract
from PIL import Image
import pyttsx3
import threading

class PDFScanner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Scanner")
        self.file_path = None
        self.engine = pyttsx3.init()
        self.speaking = False

        self.create_widgets()

    def create_widgets(self):
        # Create a button to select a PDF file
        select_button = tk.Button(self.root, text="Select PDF File", command=self.pdf_scanner)
        select_button.pack()

        # Create a variable to store the selected voice
        self.voice_var = tk.StringVar(self.root)
        self.voice_var.set("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")  # default value
        voices = [
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_KIRA_11.0",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_JASMIN_11.0",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_AMELIA_11.0",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ADELE_11.0",
        ]

        # Create a dropdown menu for voices
        voice_menu = tk.OptionMenu(self.root, self.voice_var, *voices)
        voice_menu.pack()

        # Create a variable to store the selected speed
        self.speed_var = tk.StringVar(self.root)
        self.speed_var.set("150")  # default value
        speeds = ["100", "125", "150", "175", "200"]

        # Create a dropdown menu for speeds
        speed_menu = tk.OptionMenu(self.root, self.speed_var, *speeds)
        speed_menu.pack()

        # Create a button to start speaking
        self.start_button = tk.Button(self.root, text="Start Speaking", command=self.start_speaking)
        self.start_button.pack()

        # Create a button to stop speaking
        self.stop_button = tk.Button(self.root, text="Stop Speaking", command=self.stop_speaking, state=tk.DISABLED)
        self.stop_button.pack()

    def pdf_scanner(self):
        try:
            self.file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])
            self.root.title(f"PDF Scanner - {self.file_path}")
        except Exception as e:
            print(f"Error selecting PDF file: {e}")

    def extract_text_from_pdf(self, file_path):
        try:
            pdf_file = open(file_path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            text = ''
            for page in range(num_pages):
                text += pdf_reader.pages[page].extract_text()
            pdf_file.close()
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def perform_ocr(self, text):
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            ocr_text = text
            return ocr_text
        except Exception as e:
            print(f"Error performing OCR: {e}")
            return ""

    def text_to_speech(self, text, voice, speed):
        try:
            self.engine.setProperty('voice', voice)
            self.engine.setProperty('rate', int(speed))
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error converting text to speech: {e}")

    def start_speaking(self):
        try:
            if not self.speaking:
                self.speaking = True
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                if self.file_path:
                    text = self.extract_text_from_pdf(self.file_path)
                    ocr_text = self.perform_ocr(text)
                    voice = self.voice_var.get()
                    speed = self.speed_var.get()
                    threading.Thread(target=self.text_to_speech, args=(ocr_text, voice, speed)).start()
        except Exception as e:
            print(f"Error starting speech: {e}")

    def stop_speaking(self):
        try:
            if self.speaking:
                self.speaking = False
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                self.engine.stop()
                self.engine.endLoop()  # Add this line
        except Exception as e:
            print(f"Error stopping speech: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PDFScanner()
    app.run()