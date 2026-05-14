# 🎯 Professional Text Summarization Suite v3.0

A feature-rich desktop application for intelligent text summarization, translation, and analysis — built with Python and Tkinter.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)
![Version](https://img.shields.io/badge/Version-3.0-orange?style=flat-square)

---

## ✨ Features

- **4 Summarization Algorithms** — LexRank, LSA, Luhn, and KL-Divergence
- **Multi-format File Support** — Upload `.txt`, `.docx`, and `.pdf` files
- **Side-by-Side Method Comparison** — Compare all algorithms at once
- **Multi-language Translation** — 20+ languages via Google Translate
- **Text-to-Speech** — Listen to your summaries via gTTS
- **Text Analyzer** — Word count, readability scores, keyword extraction
- **History & Favorites** — Save and reload past summaries
- **Export Summaries** — Save as `.txt` or `.docx`
- **Professional UI** — Clean dark header, status bar, live clock

---

## 🧠 Summarization Methods

| Method | Algorithm | Best For |
|--------|-----------|----------|
| 🎯 Most Important Sentences | LexRank (Graph-based) | News articles, blogs, general text |
| 🔬 Main Topic Summary | LSA (Latent Semantic Analysis) | Scientific papers, technical documents |
| ⚡ Quick Key Points | Luhn (Keyword frequency) | Product descriptions, keyword-rich text |
| 📚 Detailed Important Summary | KL-Divergence | Legal documents, critical information |

---

## 📸 Screenshots

> _Add screenshots of the app here_

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/text-summarization-suite.git
cd text-summarization-suite

# Install dependencies
pip install -r requirements.txt

# Download required NLTK data
python -c "import nltk; nltk.download('punkt')"

# Run the application
python main.py
```

---

## 📦 Dependencies

```txt
deep-translator
gTTS
playsound
python-docx
PyPDF2
sumy
nltk
```

Install all at once:

```bash
pip install deep-translator gTTS playsound python-docx PyPDF2 sumy nltk
```

> **Note:** On some systems, `playsound` may require additional setup. See [playsound docs](https://github.com/TaylorSMarks/playsound) for platform-specific instructions.

---

## 🗂️ Project Structure

```
text-summarization-suite/
│
├── main.py               # Main application entry point
├── requirements.txt      # Python dependencies
├── history.json          # Auto-generated summary history (gitignored)
├── favorites.json        # Auto-generated favorites (gitignored)
├── settings.json         # Auto-generated user settings (gitignored)
└── README.md
```

---

## 🛠️ Usage

1. **Enter or upload text** — Paste directly, use clipboard, or upload a `.txt`, `.docx`, or `.pdf` file.
2. **Configure settings** — Set the number of sentences, summary style (Concise / Balanced / Detailed), and output language.
3. **Choose a method** — Click any of the four summarization buttons.
4. **Explore tools** — Use the **Compare All** button to see all methods side-by-side, or open the **Translator** / **Text Analyzer** from the Tools menu.
5. **Save your work** — Export to file, add to Favorites, or browse History.

---

## 🌐 Supported Languages

English, Hindi, Bengali, Telugu, Marathi, Tamil, Gujarati, Malayalam, Kannada, Punjabi, Urdu, Spanish, French, German, Italian, Russian, Chinese (Simplified), Japanese, Korean, Arabic, Portuguese, Dutch

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss changes, then submit a pull request.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin my-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Sumy](https://github.com/miso-belica/sumy) — Summarization library
- [gTTS](https://github.com/pndurette/gTTS) — Text-to-Speech
- [deep-translator](https://github.com/nidhaloff/deep-translator) — Translation
- [NLTK](https://www.nltk.org/) — Natural language processing
