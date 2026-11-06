import random
import re
from CHS_for_theory import EMERGENCY_DATA


def _dangers(text: str) -> list:
    paragraph, inside = [], False
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("⚠"):
            inside = True
            continue
        if inside:
            if not s or s[0] in "🔎🚨":
                break
            paragraph.append(s)
    joined = " ".join(paragraph)
    return [p.strip(" .;") for p in joined.split(",") if len(p.strip(" .;")) > 8]


def _premons(text: str) -> list:
    out, inside = [], False
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("🔎"):
            inside = True
            continue
        if inside:
            if s.startswith("•"):
                out.append(s[1:].strip(" .;"))
            elif not s:
                break
    return out


def _steps(text: str) -> list:
    steps, cur, inside = [], None, False
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("🚨"):
            inside = True
            continue
        if inside:
            m = re.match(r"^(\d+)\.\s*(.*)", s)
            if m:
                if cur:
                    steps.append(" ".join(cur))
                cur = [m.group(2)]
            elif cur and s:
                cur.append(s)
    if cur:
        steps.append(" ".join(cur))
    return steps


def _make_question(question: str, correct: str, pool: list) -> dict:
    wrong = random.sample([p for p in pool if p != correct], 3)
    options = wrong + [correct]
    random.shuffle(options)
    return {"question": question, "options": options, "correct": options.index(correct)}


MAX_QUESTIONS = 15


def build_questions(data=EMERGENCY_DATA, target: int = MAX_QUESTIONS):
    questions = []
    for idx, (_, text, title) in enumerate(data):
        pools_d = [d for j, (_, t, _) in enumerate(data) if j != idx for d in _dangers(t)]
        pools_p = [p for j, (_, t, _) in enumerate(data) if j != idx for p in _premons(t)]
        pools_s = [s for j, (_, t, _) in enumerate(data) if j != idx for s in _steps(t)]

        dangers, premons, steps = _dangers(text), _premons(text), _steps(text)
        if dangers:
            questions.append(_make_question(
                f"ЧС «{title}»: что относится к ОПАСНОСТЯМ этой аварии?", dangers[0], pools_d))
        if premons:
            questions.append(_make_question(
                f"ЧС «{title}»: что является ПРЕДВЕСТНИКОМ аварии?", premons[0], pools_p))
        if steps:
            questions.append(_make_question(
                f"ЧС «{title}»: какое ДЕЙСТВИЕ необходимо выполнить персоналу первостепенно?", steps[0], pools_s))
    random.shuffle(questions)
    return questions[:target]
