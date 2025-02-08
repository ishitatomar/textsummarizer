import tkinter as tk
from tkinter import scrolledtext, messagebox
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import string
import nltk
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
SUMMARY_PERCENTAGE = 0.1
def summarize_text(text):
    sentences = sent_tokenize(text)
    total_sentences = len(sentences)
    num_summary_sentences = max(1, int(total_sentences * SUMMARY_PERCENTAGE))
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words and word not in string.punctuation]
    word_frequencies = Counter(words)
    sentence_scores = {}
    for sentence in sentences:
        sentence_score = 0
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                sentence_score += word_frequencies[word]
        sentence_scores[sentence] = sentence_score
    if not sentence_scores:
        return "No summary could be generated from the given text."
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_summary_sentences]
    return ' '.join(summarized_sentences)
def generate_summary():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Error", "Please enter text to summarize.")
        return
    try:
        summary = summarize_text(text)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, summary)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
def clear_summary():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
root = tk.Tk()
root.title("Text Summarizer")
heading_label = tk.Label(root, text="Text Summarizer", font=("Arial", 30, "bold"), fg="navy", bg="lightyellow", padx=20, pady=10, relief=tk.RAISED)
heading_label.pack(pady=(10, 0))
input_label = tk.Label(root, text="Enter Text to Summarize:", font=("Arial", 14))
input_label.pack(pady=(10, 5))
input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=200, height=20, font=("Arial", 16), bg="black", fg="white")
input_text.pack(pady=5)
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
summarize_button = tk.Button(button_frame, text="Summarize", font=("Arial", 14), command=generate_summary)
summarize_button.grid(row=0, column=0, padx=5)
clear_button = tk.Button(button_frame, text="Clear", font=("Arial", 14), command=clear_summary)
clear_button.grid(row=0, column=1, padx=5)
output_label = tk.Label(root, text="Summary:", font=("Arial", 14))
output_label.pack(pady=5)
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=200, height=20, font=("Arial", 16), bg="black")
output_text.pack(pady=5)
root.mainloop()
