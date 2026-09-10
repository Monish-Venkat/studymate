import asyncio
from app.services.faiss_store import store
from app.services.embeddings import embed_text
from app.services.llm_client import generate_text
from app.core.config import settings
from app.core.prompts import ask_prompt, socratic_prompt, summary_prompt, mock_prompt, pyq_prompt

def build_context(hits):
    return '\n\n'.join(f"[{i}] {h.get('source', 'unknown')}, page {h.get('page', '?')}: {h['text']}" for i, h in enumerate(hits, 1))

async def retrieve(question, subject, level, board, doc_types, top_k=None):
    if not store.index.ntotal:
        return []
    normalized_level = {'PUC1': '1st', 'PUC2': '2nd'}.get(level.upper(), level.lower())
    filters = {'subject': [subject.lower()], 'level': [normalized_level],
               'board': [board.lower()], 'doc_type': doc_types}
    vec = await asyncio.to_thread(embed_text, question)
    return await asyncio.to_thread(store.search, vec, top_k or settings.TOP_K, filters)

async def respond(query, subject, level, board, model, make_prompt, doc_types=None, persona_id=None, persona_result=None, dialogue_context=""):
    hits = await retrieve(query, subject, level, board, doc_types or ['textbook', 'syllabus'])
    hits = [h for h in hits if h['score'] >= settings.MIN_SIMILARITY]
    if not hits:
        if persona_result is not None and persona_id:
            persona_result.update(applied=False, reason='No course evidence was found, so persona styling was not used.')
        return 'I could not find supporting passages for this request in the selected course material. Check your subject and year, or ask for the relevant material to be indexed.'
    prefix = ''
    if persona_id:
        from app.services.persona import style_context
        prefix, metadata = await style_context(persona_id, subject, query)
        if persona_result is not None:
            persona_result.update(metadata)
    answer = await generate_text(model, prefix + dialogue_context + make_prompt(build_context(hits)))
    sources = '\n'.join(f"[{i}] {h['source']} | page {h.get('page', '?')}" for i, h in enumerate(hits, 1))
    return f'{answer}\n\nRetrieved sources\n{sources}'

async def run_ask(question, subject, level, board, chapter=None, persona_id=None, persona_result=None, dialogue_context=""):
    return await respond(f'{chapter or ""} {question}', subject, level, board, settings.LLM_MAIN_MODEL,
                         lambda ctx: ask_prompt(ctx, question, board, level, subject), persona_id=persona_id, persona_result=persona_result, dialogue_context=dialogue_context)

async def run_socratic(question, subject, level, board, chapter=None, persona_id=None, persona_result=None, dialogue_context=""):
    return await respond(f'{chapter or ""} {question}', subject, level, board, settings.LLM_SOCRATIC_MODEL,
                         lambda ctx: socratic_prompt(ctx, question, board, level, subject), persona_id=persona_id, persona_result=persona_result, dialogue_context=dialogue_context)

async def run_summary(chapter, subject, level, board, summary_type, persona_id=None, persona_result=None, dialogue_context=""):
    return await respond(chapter, subject, level, board, settings.LLM_SMALL_MODEL,
                         lambda ctx: summary_prompt(ctx, chapter, board, level, subject, summary_type), persona_id=persona_id, persona_result=persona_result, dialogue_context=dialogue_context)

async def run_pyq(subject, level, board):
    return await respond(subject, subject, level, board, settings.LLM_SMALL_MODEL,
                         lambda ctx: pyq_prompt(ctx, subject, board, level), ['question_paper'])

async def run_mock(subject, level, board, total_marks):
    return await respond(subject, subject, level, board, settings.LLM_MOCK_MODEL,
                         lambda ctx: mock_prompt(ctx, subject, board, level, total_marks))
