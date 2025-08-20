from PyPDF2 import PdfReader

def read_file(uploaded_file):
    """
    Reads content from a txt or pdf file and returns extracted text.
    Falls back to pdfplumber if PyPDF2 fails or returns empty.
    """
    if uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    elif uploaded_file.name.endswith(".pdf"):
        text = ""
        try:
            # Try PyPDF2 first
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception:
            text = ""

        # If PyPDF2 gave nothing, try pdfplumber
        if not text.strip():
            try:
                import pdfplumber
                uploaded_file.seek(0)  # reset pointer
                with pdfplumber.open(uploaded_file) as pdf:
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
            except Exception as e:
                return f"Error reading PDF: {e}"

        if not text.strip():
            return "Error: Could not extract any text from this PDF."

        return text

    else:
        return "Unsupported file format. Please upload a .txt or .pdf file."


def get_table_data(quiz_data):
    """
    Converts quiz JSON into a table-friendly format (list of dicts).
    Handles both dict-style options {a:..,b:..} and list-style ["..","..","..",".."].
    """
    table = []

    if isinstance(quiz_data, dict):
        quiz_data = [quiz_data]

    for idx, item in enumerate(quiz_data, start=1):
        mcq = item.get("question") or item.get("mcq", "")
        options = item.get("options", [])
        correct = item.get("answer") or item.get("correct", "")

        # Normalize options
        if isinstance(options, dict):
            opts = [
                options.get("a", ""),
                options.get("b", ""),
                options.get("c", ""),
                options.get("d", "")
            ]
        elif isinstance(options, list):
            opts = options + [""] * (4 - len(options))  # pad to 4
        else:
            opts = ["", "", "", ""]

        row = {
            "Q.No": idx,
            "Question": mcq,
            "A": opts[0],
            "B": opts[1],
            "C": opts[2],
            "D": opts[3],
            "Correct Answer": correct
        }
        table.append(row)

    return table
