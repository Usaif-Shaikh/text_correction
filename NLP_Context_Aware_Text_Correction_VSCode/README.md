# NLP-Based Context-Aware Text Error Detection and Correction System

A Python NLP mini-project for identifying likely spelling mistakes and selected grammar/context issues in English text.

## Features
- Spelling suggestions using PySpellChecker
- Grammar, punctuation, and selected context checks using LanguageTool
- Explanations and suggested corrections
- Original vs. suggested corrected text
- Download corrected text
- Browser interface built with Streamlit

## Requirements
- Python 3.10+ recommended
- Visual Studio Code recommended
- Internet access may be needed by LanguageTool depending on setup

## Run in VS Code on Windows
1. Extract this ZIP.
2. Open VS Code → **File → Open Folder** → select the extracted project folder.
3. Choose **Terminal → New Terminal**.
4. Run each command:

```powershell
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

5. Open the local URL shown in the terminal, usually `http://localhost:8501`.
6. Keep the terminal open during your demonstration. Press `Ctrl+C` to stop the server.

If `python` is not recognized, install Python from https://www.python.org/downloads/, select **Add Python to PATH**, then restart VS Code.

## Example
`I went too college yesterday. She have a new book. I recieved the assignment.`

Results can vary with library versions and LanguageTool availability. Review all suggestions.

## Upload to GitHub
Create an empty repository on GitHub. In the VS Code terminal, run:

```bash
git init
git add .
git commit -m "Initial NLP text correction project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the URL with your own repository URL. Do not upload `.venv/`, credentials, or personal information.

## Limitations
- English-only prototype.
- Suggestions are not guaranteed to be correct.
- LanguageTool may fail if its service/runtime or network is unavailable.
- Future scope: accept/reject controls, labelled evaluation data, precision/recall/F1 evaluation.
