"""
generate_pdf_report.py - Generates a professional PDF Masterclass Report
for the ShieldDOCS Format-Preserving PII Redaction Engine.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)

def build_pdf(filename="ShieldDOCS_PII_Redactor_Masterclass.pdf"):
    pdf_path = os.path.join(os.path.dirname(__file__), filename)
    desktop_pdf_path = os.path.join("/Users/kunalkumar/Desktop", filename)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    COLOR_PRIMARY = colors.HexColor("#0f172a")     # Slate 900
    COLOR_ACCENT = colors.HexColor("#2563eb")      # Blue 600
    COLOR_SECONDARY = colors.HexColor("#475569")   # Slate 600
    COLOR_BG_LIGHT = colors.HexColor("#f8fafc")    # Slate 50
    COLOR_BORDER = colors.HexColor("#e2e8f0")      # Slate 200

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=COLOR_PRIMARY,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=COLOR_SECONDARY,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=COLOR_ACCENT,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=COLOR_PRIMARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=15,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=COLOR_BORDER,
        borderWidth=1,
        borderPadding=6,
        spaceAfter=8,
        borderRadius=4
    )

    story = []

    # -------------------------------------------------------------------------
    # HEADER / COVER TITLE
    # -------------------------------------------------------------------------
    story.append(Paragraph("ShieldDOCS - Format-Preserving PII Redaction Engine", title_style))
    story.append(Paragraph("<b>Complete Masterclass Report: Assignment Problem, Technical Architecture & Line-by-Line Code Explanation</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceBefore=0, spaceAfter=10))

    meta_data = [
        [Paragraph("<b>Author:</b> Engineering & AI Systems Group", body_style), Paragraph("<b>Target Repository:</b> Singhkunall/pii-doc-redactor", body_style)],
        [Paragraph("<b>Date:</b> August 2026", body_style), Paragraph("<b>Live Production App:</b> pii-doc-redactor.onrender.com", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[3.5*inch, 4.0*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # PART 1: THE ASSIGNMENT PROBLEM STATEMENT
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part 1: Assignment Statement & Core Engineering Problem", h1_style))
    story.append(Paragraph(
        "The objective of this assignment was to build an enterprise-grade document processing system capable of automatically detecting "
        "and redacting Personally Identifiable Information (PII) from legal, corporate, and financial Word documents (e.g., Red Herring Prospectuses, "
        "Corporate NDAs, HR agreements) and text files, substituting sensitive data with realistic, consistent fake replacements.", body_style))
    
    story.append(Paragraph("<b>The Fundamental Challenge with Naive Redaction:</b>", h2_style))
    story.append(Paragraph(
        "In Microsoft Word XML (`.docx`), character formatting (bold, italic, font family, font size, text color, highlight) is stored inside child node elements "
        "called <b>Runs (`&lt;w:r&gt;`)</b>. Standard python-docx scripts perform text replacement by overwriting <code>paragraph.text = new_text</code>. "
        "This naive approach <b>erases all child Run XML elements</b>, stripping bold headers, italic legal notes, and table layouts into plain unstyled text. "
        "ShieldDOCS solves this by introducing <b>run-aware XML character mapping</b>.", body_style))
    
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------------------
    # PART 2: TECHNICAL ARCHITECTURE & SYSTEM DESIGN
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part 2: Technical Architecture & Design Principles", h1_style))
    
    arch_summary = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technology / Implementation</b>", body_style), Paragraph("<b>Key Design Purpose</b>", body_style)],
        [Paragraph("<b>PII Engine</b>", body_style), Paragraph("Python 3.11, Regex, Custom Legal Heuristics", body_style), Paragraph("High precision detection without heavy NLP model overhead", body_style)],
        [Paragraph("<b>Format Preserver</b>", body_style), Paragraph("OpenXML Run-Aware Character Offset Mapper", body_style), Paragraph("Retains 100% of bold/italic/colors & table structures", body_style)],
        [Paragraph("<b>Fake Generator</b>", body_style), Paragraph("Stateless MD5 Hash Seeding (`FakeMapper`)", body_style), Paragraph("Guarantees 100% entity consistency across 50+ page documents", body_style)],
        [Paragraph("<b>Backend API</b>", body_style), Paragraph("FastAPI, CORSMiddleware, 1-Shot Response", body_style), Paragraph("Single HTTP round-trip for instant <1s UI rendering", body_style)],
        [Paragraph("<b>Web Frontend</b>", body_style), Paragraph("Vanilla JS, Glassmorphic CSS, Blob Download", body_style), Paragraph("Interactive live preview, category filters, 1-click download", body_style)],
        [Paragraph("<b>Cloud Host</b>", body_style), Paragraph("Gunicorn + Multi-Worker Uvicorn on Docker/Render", body_style), Paragraph("Production concurrency and dynamic PORT env binding", body_style)]
    ]
    t_arch = Table(arch_summary, colWidths=[1.8*inch, 2.7*inch, 3.0*inch])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # PART 3: EXHAUSTIVE LINE-BY-LINE CODE EXPLANATION
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part 3: Exhaustive Code Walkthrough & Explanation", h1_style))

    # 3.1 pii_engine.py
    story.append(Paragraph("3.1 `pii_engine.py` - Core Detection & Run-Level Manipulation", h2_style))
    story.append(Paragraph("<b>A. Structured Regex Detectors:</b>", body_style))
    story.append(Paragraph("• <code>EMAIL_RE</code>: Uses word boundaries <code>\\b</code> to match emails without capturing surrounding text.", bullet_style))
    story.append(Paragraph("• <code>PHONE_RE</code>: Dual-pattern regex matching Indian <code>+91</code> numbers and US <code>(555) 019-2834</code> formats.", bullet_style))
    story.append(Paragraph("• <code>DOB_RE</code>: Employs contextual triggers (<code>Date of Birth:</code> or <code>DOB:</code>) before date parsing to avoid redacting standard contract execution dates.", bullet_style))
    
    story.append(Paragraph("<b>B. Unstructured Legal Heuristics & Stopword Filtering:</b>", body_style))
    story.append(Paragraph("• <code>COMPANY_SUFFIX_RE</code>: Matches capital-cased entity names preceding legal suffixes (<code>Private Limited</code>, <code>LLP</code>, <code>Inc</code>).", bullet_style))
    story.append(Paragraph("• <code>NAME_TRIGGER_RE</code>: Extracts names following executive titles (<i>Managing Director</i>, <i>Compliance Officer</i>, <i>Authorised Signatory</i>).", bullet_style))
    story.append(Paragraph("• <code>LEGAL_DEFINED_TERM_WORDS</code> & <code>_is_probable_person_name()</code>: Filters candidates against a 150+ legal prospectus stopword dictionary to prevent terms like <i>Book Running Lead Managers</i> from being misidentified as human names.", bullet_style))

    story.append(Paragraph("<b>C. Deterministic Hash Generator (`FakeMapper`):</b>", body_style))
    story.append(Paragraph("• Uses MD5 hash seeding: <code>seed = int(md5(salt + category + value).hexdigest(), 16)</code>.", bullet_style))
    story.append(Paragraph("• <b>Why:</b> Guarantees that 'Rahul Kapoor' is 100% consistently replaced by 'Kavya Reddy' across a 50-page document without requiring a database.", bullet_style))

    story.append(Paragraph("<b>D. Format-Preserving Run Redactor (`redact_paragraph_preserve_runs`):</b>", body_style))
    story.append(Paragraph(
        "1. Constructs a character-to-run offset map: <code>run_map = [(run_obj, char_offset_in_run)]</code>.<br/>"
        "2. Sorts PII spans from <b>right to left</b> (<code>reverse=True</code>) so replacements do not alter character indices of earlier spans.<br/>"
        "3. Modifies text inside individual <code>run.text</code> nodes, preserving parent <code>&lt;w:rPr&gt;</code> character styles (bold, italic, colors).", body_style))

    story.append(Spacer(1, 6))

    # 3.2 main.py
    story.append(Paragraph("3.2 `main.py` - FastAPI Server & 1-Shot Performance Optimization", h2_style))
    story.append(Paragraph("• <b>CORSMiddleware</b>: Exposes <code>Content-Disposition</code> headers so web browsers can extract stream filenames.", bullet_style))
    story.append(Paragraph("• <b>1-Shot Response (`/api/analyze`)</b>: Combines text extraction, PII scanning, entity table generation, AND HTML preview creation into 1 single HTTP request. Reduces UI load latency from 4s down to <1s.", bullet_style))
    story.append(Paragraph("• <b>Dynamic Port Binding</b>: Reads <code>os.environ.get('PORT', 10000)</code> dynamically to prevent 502 Bad Gateway errors on Render/Docker.", bullet_style))

    story.append(Spacer(1, 6))

    # 3.3 static/app.js
    story.append(Paragraph("3.3 `static/app.js` - Robust Frontend UI Logic", h2_style))
    story.append(Paragraph("• <b>JavaScript String `.endsWith()` Fix</b>: Replaced Python <code>.endswith</code> with JS <code>.endsWith()</code> to prevent frontend script crashes.", bullet_style))
    story.append(Paragraph("• <b>Safe Error Parsing</b>: Wraps <code>res.json()</code> in fallback try-catch blocks to handle non-JSON 502/500 proxy responses safely without throwing <code>Unexpected end of JSON input</code>.", bullet_style))
    story.append(Paragraph("• <b>Blob URL Download</b>: Converts binary stream into <code>window.URL.createObjectURL(blob)</code> and triggers programmatic browser download.", bullet_style))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # PART 4: TECHNICAL SUMMARY & COMPARISON MATRIX
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part 4: Technical Summary & Comparison Matrix", h1_style))
    
    comp_matrix = [
        [Paragraph("<b>Challenge</b>", body_style), Paragraph("<b>Implemented Solution</b>", body_style), Paragraph("<b>Why We Chose It</b>", body_style), Paragraph("<b>Alternative & Disadvantage</b>", body_style)],
        [
            Paragraph("<b>Style Loss</b>", body_style),
            Paragraph("Run-Level Offset Mapper", body_style),
            Paragraph("Modifies text inside `<w:t>` while preserving `<w:rPr>` formatting", body_style),
            Paragraph("Overwriting `paragraph.text` erases all bold/italic/color XML nodes", body_style)
        ],
        [
            Paragraph("<b>Entity Consistency</b>", body_style),
            Paragraph("MD5 Hash Seeding (`FakeMapper`)", body_style),
            Paragraph("Rahul Kapoor maps to Kavya Reddy 100% consistently everywhere", body_style),
            Paragraph("Random generators replace same person with different names across pages", body_style)
        ],
        [
            Paragraph("<b>False Positives</b>", body_style),
            Paragraph("Legal Stopword Filter Set", body_style),
            Paragraph("Prevents prospectus boilerplate from being flagged as human names", body_style),
            Paragraph("Heavy NLP models (spaCy) take 500MB+ RAM and slow down boot times", body_style)
        ],
        [
            Paragraph("<b>UI Latency</b>", body_style),
            Paragraph("Unified 1-Shot Endpoint", body_style),
            Paragraph("Returns metrics, table, and preview HTML in 1 single HTTP call", body_style),
            Paragraph("2 sequential network calls introduced 4s delay on free cloud servers", body_style)
        ],
        [
            Paragraph("<b>502 Bad Gateway</b>", body_style),
            Paragraph("Dynamic Port + Gunicorn", body_style),
            Paragraph("Binds `0.0.0.0:$PORT` and spawns 2 async Uvicorn worker threads", body_style),
            Paragraph("Hardcoded port 8000 causes proxy gateway routing failures on Render", body_style)
        ]
    ]
    t_comp = Table(comp_matrix, colWidths=[1.3*inch, 1.8*inch, 2.2*inch, 2.2*inch])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # PART 5: 2-MINUTE INTERVIEW PITCH
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part 5: 2-Minute Technical Pitch / Summary", h1_style))
    story.append(Paragraph(
        "<i>\"I built ShieldDOCS, an enterprise format-preserving PII redaction engine for Word documents and legal text files. "
        "The primary challenge was that standard redactors wipe out Word XML Run elements, destroying bold headers, italic notes, font colors, and table structures. "
        "I solved this by developing a Run-level XML manipulator in Python that maps string offsets to individual Word Run nodes, replacing sensitive text while preserving 100% of character styles.<br/><br/>"
        "For detection, I built a hybrid engine combining regexes for structured PII with contextual heuristics and legal dictionary filters for unstructured PII. "
        "For replacement, I designed a stateless MD5 hash-seeded generator that guarantees entity consistency across multi-page documents without needing a database. "
        "Finally, I wrapped this in an optimized 1-shot FastAPI backend paired with a Glassmorphic Web UI and deployed it using Gunicorn with Uvicorn workers on Docker and Render.\"</i>",
        code_style
    ))

    # Build Document
    doc.build(story)

    # Save copy to Desktop
    import shutil
    shutil.copy(pdf_path, desktop_pdf_path)

    print(f"PDF generated successfully at:\n 1. {pdf_path}\n 2. {desktop_pdf_path}")

if __name__ == "__main__":
    build_pdf()
