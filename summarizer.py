from tkinter import *
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from deep_translator import GoogleTranslator
from gtts import gTTS
import playsound
import tempfile
import os
import threading
import sounddevice as sd
import wavio
from docx import Document
import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.kl import KLSummarizer
import time  # Import time for timestamps

# List of languages
languages = {
    'English': 'en',
    'Hindi': 'hi',
    'Bengali': 'bn',
    'Telugu': 'te',
    'Marathi': 'mr',
    'Tamil': 'ta',
    'Gujarati': 'gu',
    'Malayalam': 'ml',
    'Kannada': 'kn',
    'Punjabi': 'pa',
    'Urdu': 'ur',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Russian': 'ru',
    'Chinese (Simplified)': 'zh-CN',
    'Japanese': 'ja',
    'Korean': 'ko',
}

playback_thread = None
uploaded_content = ""  # Variable to store uploaded document content
recording = False  # To manage recording state
history = []  # List to store user interactions


# Function to play the welcome message
def play_welcome_message():
    welcome_text = "Welcome Nafees Shaikh"
    tts = gTTS(text=welcome_text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        tts.save(temp_file.name)
    play_audio(temp_file.name)


# Summarization functions
def summarize_text(method):
    count = text1.get()
    txt1 = textbox1.get("1.0", 'end-1c')
    if txt1 == "":
        messagebox.showinfo("Critical", "Please add or paste the content")
        textbox1.focus()
    elif count == "":
        messagebox.showinfo("Critical", "Please enter the number of sentences")
        text1.focus()
        text1["bg"] = "red"
    else:
        text1["bg"] = "yellow"
        parser = PlaintextParser.from_string(txt1, Tokenizer('english'))
        if method == 'lexrank':
            summarizer = LexRankSummarizer()
        elif method == 'lsa':
            summarizer = LsaSummarizer()
        elif method == 'luhn':
            summarizer = LuhnSummarizer()
        elif method == 'kl':
            summarizer = KLSummarizer()
        summary = summarizer(parser.document, sentences_count=int(count))
        textbox2.delete("1.0", END)  # Clear previous summaries
        for sentence in summary:
            textbox2.insert(END, sentence)

        # Append to history
        history.append(f"Summary Method: {method}, Sentences: {count}, Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")


def translate_text():
    text_to_translate = textbox1.get("1.0", 'end-1c').strip()
    target_language = languages[language_var.get()]
    if not text_to_translate:
        messagebox.showinfo("Critical", "Please add text to translate")
        return
    try:
        translated = GoogleTranslator(source='auto', target=target_language).translate(text_to_translate)
        textbox2.delete("1.0", END)
        textbox2.insert(END, translated)

        # Append to history
        history.append(f"Translated to: {language_var.get()}, Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        messagebox.showerror("Translation Error", f"An error occurred: {str(e)}")


def text_to_audio(text, lang='en'):
    if not text:
        messagebox.showinfo("Critical", "Please generate summary or enter text to convert to audio")
        return
    try:
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            tts.save(temp_file.name)
        play_audio(temp_file.name)
    except Exception as e:
        messagebox.showerror("Audio Error", str(e))


def play_audio(file_path):
    global playback_thread

    def play():
        playsound.playsound(file_path)

    if playback_thread is not None and playback_thread.is_alive():
        stop_audio()
    playback_thread = threading.Thread(target=play)
    playback_thread.start()


def stop_audio():
    global playback_thread
    if playback_thread is not None and playback_thread.is_alive():
        os._exit(0)


def upload_document():
    global uploaded_content
    file_path = filedialog.askopenfilename(filetypes=[
        ("Text Files", "*.txt"),
        ("Word Documents", "*.docx"),
        ("PDF Files", "*.pdf"),
        ("All Files", ".")
    ])
    if file_path:
        content = ""
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            content = "\n".join([para.text for para in doc.paragraphs])
        elif file_path.endswith('.pdf'):
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                content = "\n".join([page.extract_text() for page in reader.pages])
        uploaded_content = content  # Store uploaded content
        textbox1.delete("1.0", END)
        textbox1.insert(END, content)


def clear_textboxes(textboxes):
    for textbox in textboxes:
        textbox.delete("1.0", END)


# Function to open the history window
# Function to open the history window with clickable entries
def open_history_window():
    def load_history_text(event):
        selected_index = history_listbox.curselection()
        if selected_index:
            method_info, original_text, processed_text = history[selected_index[0]]
            textbox1.delete("1.0", END)
            textbox1.insert(END, original_text)
            textbox2.delete("1.0", END)
            textbox2.insert(END, processed_text)

    history_window = Toplevel()
    history_window.title("History")
    history_window.geometry("800x600")
    history_window.configure(bg='#f9f9f9')

    history_listbox = Listbox(history_window, width=1000, height=500, font=("Arial", 12))
    history_listbox.pack(pady=10)

    # Add both summarization and translation entries
    for entry in history:
        history_listbox.insert(END, entry[0])  # Display summary/translation info

    # Add a binding to load the corresponding text when an item is clicked
    history_listbox.bind('<<ListboxSelect>>', load_history_text)

    global textbox1, textbox2  # Use the global textboxes to allow them to be cleared/loaded


def summarize_text(method):
    count = text1.get()
    txt1 = textbox1.get("1.0", 'end-1c')
    if txt1 == "":
        messagebox.showinfo("Critical", "Please add or paste the content")
        textbox1.focus()
    elif count == "":
        messagebox.showinfo("Critical", "Please enter the number of sentences")
        text1.focus()
        text1["bg"] = "red"
    else:
        text1["bg"] = "yellow"
        parser = PlaintextParser.from_string(txt1, Tokenizer('english'))
        if method == 'lexrank':
            summarizer = LexRankSummarizer()
        elif method == 'lsa':
            summarizer = LsaSummarizer()
        elif method == 'luhn':
            summarizer = LuhnSummarizer()
        elif method == 'kl':
            summarizer = KLSummarizer()
        summary = summarizer(parser.document, sentences_count=int(count))
        processed_text = "\n".join(str(sentence) for sentence in summary)
        textbox2.delete("1.0", END)  # Clear previous summaries
        textbox2.insert(END, processed_text)

        # Append to history
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        history.append((f"Summary Method: {method}, Sentences: {count}, Time: {timestamp}", txt1, processed_text))


def open_history_window():
    def load_history_text(event):
        selected_index = history_listbox.curselection()
        if selected_index:
            method_info, original_text, processed_text = history[selected_index[0]]
            textbox1.delete("1.0", END)
            textbox1.insert(END, original_text)
            textbox2.delete("1.0", END)
            textbox2.insert(END, processed_text)

    history_window = Toplevel()
    history_window.title("History")
    history_window.geometry("800x600")
    history_window.configure(bg='#f9f9f9')

    history_listbox = Listbox(history_window, width=1000, height=500, font=("Arial", 12))
    history_listbox.pack(pady=10)

    for entry in history:
        history_listbox.insert(END, entry[0])  # Display the summary info

    # Add a binding to load the corresponding text when an item is clicked
    history_listbox.bind('<<ListboxSelect>>', load_history_text)

    # Set up the main textboxes for displaying the loaded content
    global textbox1, textbox2  # Use the global textboxes to allow them to be cleared/loaded

    # Now, clicking on a history entry will load the respective original and processed texts into the textboxes


# Main GUI window setup with welcome message
def open_tool_interface():
    main_window = tk.Tk()
    main_window.title("Tool Interface")
    main_window.geometry("800x600")
    main_window.configure(bg='#e6f2ff')

    title_label = Label(main_window, text="Text summarisation System", font=("Arial", 24, "bold"), bg='#e6f2ff',
                        fg='#333333')
    title_label.pack(pady=20)

    upload_button = Button(main_window, text="Upload Document", command=upload_document, bg="#4CAF50", fg="#ffffff",
                           font=("Arial", 12, "bold"))
    upload_button.pack(pady=10)

    tools = [
        ("Summarizer", "Summarize text", open_summarizer_window),
        ("Translator", "Unlock languages", open_translation_window),
        ("Stop Audio", "Stop playing audio", stop_audio)
    ]

    frame = tk.Frame(main_window, bg='#e6f2ff')
    frame.pack(pady=20)
    for index, (name, description, command) in enumerate(tools):
        button = tk.Button(
            frame,
            text=name,
            width=15,
            height=4,
            command=command,
            bg="#4CAF50",
            fg="#ffffff",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=2,
            activebackground="#cce7ff"
        )
        button.grid(row=index, column=0, padx=10, pady=10)
    history_button = Button(main_window, width=15,
                            height=4, text="View History", command=open_history_window, bg="#4CAF50", fg="#ffffff",
                            font=("Arial", 12, "bold"))
    history_button.pack(pady=20)

    # Play the welcome message when the interface opens
    play_welcome_message()

    main_window.mainloop()


def open_summarizer_window():
    global window, textbox1, textbox2, text1
    window = Toplevel()
    window.title("Laconic Summarizer")
    window.geometry("400x300")
    window.configure(bg='#f9f9f9')

    label1 = Label(window, text="Enter the number of sentences:", font=("Arial", 12), bg='#f9f9f9')
    label1.pack(pady=10)

    text1 = Entry(window, font=("Arial", 12))
    text1.pack(pady=5)

    label2 = Label(window, text="Paste your text or paragraph:", font=("Arial", 12), bg='#f9f9f9')
    label2.pack(pady=10)

    textbox1 = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=100, height=10, font=("Arial", 12))
    textbox1.pack(pady=5)
    textbox1.focus()

    textbox2 = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=100, height=10, font=("Arial", 12))
    textbox2.pack(pady=5)

    if uploaded_content:
        textbox1.insert(END, uploaded_content)

    audio_button = Button(window, text="Convert to Audio", command=lambda: text_to_audio(textbox2.get("1.0", 'end-1c')),
                          bg="#4CAF50", fg="#ffffff", font=("Arial", 12))
    audio_button.pack(side=LEFT, padx=5, pady=5)

    clear_button = Button(window, text="Clear Text", command=lambda: clear_textboxes([textbox1, textbox2]),
                          bg="#FF6347", fg="#ffffff", font=("Arial", 12, "bold"))
    clear_button.pack(side=LEFT, pady=5)

    menubar = Menu(window)
    file = Menu(menubar, tearoff=0)
    file.add_command(label="Summary by number of sentences", command=lambda: summarize_text('lexrank'))
    file.add_command(label="Summary by number of sentences in simple words", command=lambda: summarize_text('lsa'))
    file.add_command(label="Summary by number of sentences from High Ranking words",
                     command=lambda: summarize_text('luhn'))
    file.add_command(label="Summary by number of sentences from keywords", command=lambda: summarize_text('kl'))
    file.add_separator()
    file.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="Summary", menu=file)
    window.config(menu=menubar)

    for index, (name, method) in enumerate(Button):
        button = Button(window, text=name, command=lambda m=method: summarize_text(m), bg="#4CAF50", fg="#ffffff",
                        font=("Arial", 12, "bold"))
        button.pack(padx=5, pady=5)

    clear_button = Button(window, text="Clear Text", command=lambda: clear_textboxes([textbox1, textbox2]),
                          bg="#FF6347", fg="#ffffff", font=("Arial", 12, "bold"))
    clear_button.pack(padx=5, pady=5)


def open_translation_window():
    global textbox1, textbox2, language_var
    window = Toplevel()
    window.title("Translate Text")
    window.geometry("400x300")
    window.configure(bg='#f9f9f9')

    label1 = Label(window, text="Select target language:", font=("Arial", 12), bg='#f9f9f9')
    label1.pack(pady=10)

    language_var = StringVar(window)
    language_var.set('English')

    language_menu = OptionMenu(window, language_var, *languages.keys())
    language_menu.pack(pady=5)

    label2 = Label(window, text="Paste your text or paragraph:", font=("Arial", 12), bg='#f9f9f9')
    label2.pack(pady=10)

    textbox1 = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=100, height=10, font=("Arial", 12))
    textbox1.pack(pady=5)
    textbox1.focus()

    textbox2 = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=100, height=10, font=("Arial", 12))
    textbox2.pack(pady=5)

    if uploaded_content:
        textbox1.insert(END, uploaded_content)

    translate_button = Button(window, text="Translate", command=translate_text, bg="#4CAF50", fg="#ffffff",
                              font=("Arial", 12))
    translate_button.pack(pady=10)

    audio_button = Button(window, text="Convert to Audio", command=lambda: text_to_audio(textbox2.get("1.0", 'end-1c')),
                          bg="#4CAF50", fg="#ffffff", font=("Arial", 12))
    audio_button.pack(padx=5, pady=7)

    clear_button = Button(window, text="Clear Text", command=lambda: clear_textboxes([textbox1, textbox2]),
                          bg="#FF6347", fg="#ffffff", font=("Arial", 12, "bold"))
    clear_button.pack(pady=5)


# Run the main interface
open_tool_interface()