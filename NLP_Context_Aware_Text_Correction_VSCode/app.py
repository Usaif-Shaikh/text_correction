import re
from typing import Any

import streamlit as st
from spellchecker import SpellChecker
import language_tool_python

st.set_page_config(page_title="NLP Text Correction System", page_icon="📝", layout="wide")
st.title("NLP-Based Context-Aware Text Error Detection and Correction System")
st.write("Enter English text to identify likely spelling errors and supported grammar/context issues.")

DEFAULT_TEXT = "I went too college yesterday. She have a new book. I recieved the assignment and it was very intresting."

with st.sidebar:
    st.header("Settings")
    check_spelling = st.checkbox("Check spelling", value=True)
    check_grammar = st.checkbox("Check grammar and context", value=True)
    st.info("Grammar/context checking uses LanguageTool and may require internet access or additional setup.")

input_text = st.text_area("Enter text to analyse", value=DEFAULT_TEXT, height=180)


def spelling_issues(text: str) -> list[dict[str, Any]]:
    checker = SpellChecker()
    issues = []
    for match in re.finditer(r"\b[A-Za-z']+\b", text):
        word = match.group(0)
        if word.isupper() and len(word) > 1:
            continue
        if word.lower() not in checker:
            suggestion = checker.correction(word.lower())
            if suggestion and suggestion.lower() != word.lower():
                if word[:1].isupper():
                    suggestion = suggestion.capitalize()
                issues.append({
                    "type": "Spelling", "original": word, "suggestion": suggestion,
                    "start": match.start(), "end": match.end(),
                    "message": f"'{word}' may be misspelled.", "engine": "PySpellChecker",
                })
    return issues


def grammar_issues(text: str) -> tuple[list[dict[str, Any]], str | None]:
    tool = None
    try:
        tool = language_tool_python.LanguageTool("en-US")
        issues = []
        for match in tool.check(text):
            replacements = getattr(match, "replacements", []) or []
            issues.append({
                "type": "Grammar / Context",
                "original": text[match.offset:match.offset + match.errorLength],
                "suggestion": replacements[0] if replacements else "",
                "start": match.offset, "end": match.offset + match.errorLength,
                "message": getattr(match, "message", "Possible grammar issue."),
                "engine": "LanguageTool",
            })
        return issues, None
    except Exception as exc:
        return [], "Grammar/context checking could not start. Check network and LanguageTool setup. Details: " + str(exc)
    finally:
        if tool is not None:
            try:
                tool.close()
            except Exception:
                pass


def apply_suggestions(text: str, issues: list[dict[str, Any]]) -> str:
    candidates = sorted([x for x in issues if x.get("suggestion")], key=lambda x: (x["start"], x["end"]))
    selected, last_end = [], -1
    for item in candidates:
        if item["start"] >= last_end:
            selected.append(item)
            last_end = item["end"]
    result = text
    for item in reversed(selected):
        result = result[:item["start"]] + item["suggestion"] + result[item["end"]:]
    return result


if st.button("Analyse text", type="primary"):
    if not input_text.strip():
        st.warning("Enter some text before analysing.")
    else:
        results, warnings = [], []
        if check_spelling:
            results.extend(spelling_issues(input_text))
        if check_grammar:
            grammar, warning = grammar_issues(input_text)
            results.extend(grammar)
            if warning:
                warnings.append(warning)
        results.sort(key=lambda x: x["start"])
        st.session_state["results"] = results
        st.session_state["analysed_text"] = input_text
        st.session_state["warnings"] = warnings

if "results" in st.session_state and st.session_state.get("analysed_text") == input_text:
    results = st.session_state["results"]
    for warning in st.session_state.get("warnings", []):
        st.warning(warning)
    st.subheader("Analysis summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total issues", len(results))
    c2.metric("Spelling issues", sum(x["type"] == "Spelling" for x in results))
    c3.metric("Grammar/context issues", sum(x["type"] == "Grammar / Context" for x in results))
    st.subheader("Detected issues and suggestions")
    if not results:
        st.success("No likely issues were found by the enabled checks.")
    for i, issue in enumerate(results, start=1):
        with st.expander(f"{i}. {issue['type']} — {issue['original'] or 'text structure'}", expanded=True):
            st.write("**Explanation:**", issue["message"])
            st.write("**Suggested correction:**", issue["suggestion"] or "No automatic suggestion available")
            st.caption("Detection engine: " + issue["engine"])
    corrected = apply_suggestions(st.session_state["analysed_text"], results)
    st.subheader("Original vs. suggested corrected text")
    left, right = st.columns(2)
    with left:
        st.text_area("Original text", value=st.session_state["analysed_text"], height=160, disabled=True)
    with right:
        st.text_area("Suggested corrected text", value=corrected, height=160, disabled=True)
        st.download_button("Download corrected text", data=corrected, file_name="corrected_text.txt", mime="text/plain")

st.divider()
st.caption("Academic prototype: suggestions may be inaccurate. Review corrections before accepting them.")
