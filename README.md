# ShieldDOCS - Format-Preserving PII Redaction Engine

ShieldDOCS is a Python & FastAPI-based Word Document (`.docx`) and text file PII redaction engine. Unlike standard redactors that wipe Word formatting, ShieldDOCS performs run-aware replacement in Word XML, **preserving 100% of character styles (bold, italic, font colors, font sizes, highlight, and table formatting)** while replacing sensitive data with deterministic fake values.

## 🚀 Features

- **Format-Preserving DOCX Redaction**: Retains all Word styles, tables, font families, and colors.
- **Regex & Legal Heuristic Detectors**: Detects Emails, Phone numbers (+91 & International), SSN, Credit Cards, IP Addresses, Dates of Birth, Names, Company Suffixes, and Registered Addresses.
- **Deterministic Fake Mapping**: Hash-seeded fake data generation ensures consistency across documents.
- **Modern Web Interface**: Dark mode UI with drag-and-drop file upload, live entity summary cards, category toggles, interactive inspector table, side-by-side document comparison, and 1-click download.
- **REST API**: Built on FastAPI with clean endpoints for analysis, preview, and redaction.

## 🛠️ Installation & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Singhkunall/pii-doc-redactor.git
   cd pii-doc-redactor
   ```

2. Create virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   python main.py
   ```

4. Open your browser and navigate to:
   `http://127.0.0.1:8000/`

## 🐳 Docker Deployment

Build and run using Docker:
```bash
docker build -t pii-doc-redactor .
docker run -p 8000:8000 pii-doc-redactor
```

## 📄 License

MIT License
