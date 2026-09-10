def ask_prompt(context, question, board, level, subject):
    return f'Explain clearly using only the context. Board={board}; Level={level}; Subject={subject}.\nCONTEXT:\n{context}\nQUESTION:{question}'

def socratic_prompt(context, question, board, level, subject):
    return f'You are a Socratic tutor. Ask guiding questions first, grounded in context. Board={board}; Level={level}; Subject={subject}.\nCONTEXT:\n{context}\nQUESTION:{question}'

def summary_prompt(context, chapter, board, level, subject, summary_type):
    return f'Summarize the retrieved material for {chapter} as {summary_type}. Do not imply this covers the entire chapter. Board={board}; Level={level}; Subject={subject}.\nCONTEXT:\n{context}'

def mock_prompt(context, subject, board, level, total_marks):
    return f'Generate a practice paper for {subject}, using only the context. Include recall/comprehension, application/analysis, and evaluation questions. Label Bloom level and marks for each question. Include internal choice with equal marks. Count only one alternative toward the exact total of {total_marks}. This is practice, not a verified official format. Board={board}; Level={level}.\nCONTEXT:\n{context}'

def pyq_prompt(context, subject, board, level):
    return f'Review these question-paper excerpts for {subject}. State that this is a limited excerpt review, not a complete five-year statistical trend analysis. Do not invent frequencies or year coverage. Board={board}; Level={level}.\nCONTEXT:\n{context}'
