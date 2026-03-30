"""
nlp_engine.py — CVR Chatbot NLP Engine
Strategy:
  1. Query normalisation via QUERY_MAP (casual → formal search terms)
  2. Stopword removal + keyword extraction
  3. Hard keyword filter (sentences with ≥1 keyword)
  4. Multi-factor sentence scoring (hit-ratio, names, numbers, length)
  5. TF-IDF cosine re-ranking on top candidates
  6. Deduplication → return best 3-4 sentences as answer
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from knowledge_base import CVR_KNOWLEDGE

# ── Query normalisation map ──────────────────────────────────────────────────
QUERY_MAP = {
    # People
    "who is the principal":     "principal dr bhaskara rao name",
    "who is principal":         "principal dr bhaskara rao name",
    "principal name":           "principal dr bhaskara rao",
    "principal of cvr":         "principal dr bhaskara rao",
    "who is the director":      "director governing board name",
    "who is director":          "director governing board name",
    "who is the chairman":      "chairman cherabuddi trust founder",
    "who is chairman":          "chairman cherabuddi trust founder",
    "who is the hod":           "head department hod professor",
    "who is hod":               "head department hod professor",
    "warden":                   "warden hostel boys girls",
    "founder":                  "founder cherabuddi venkata reddy established",

    # Admissions
    "how to join":              "admission procedure eligibility apply eamcet",
    "how to get admission":     "admission eamcet eligibility criteria",
    "how to apply":             "admission procedure application form",
    "admission process":        "admission procedure eligibility criteria eamcet",
    "admission procedure":      "admission procedure eligibility criteria eamcet",
    "eligibility":              "eligibility criteria qualification intermediate mathematics",
    "eamcet":                   "eamcet rank cutoff admission closing",
    "eamcet cutoff":            "eamcet cutoff rank closing branch",
    "cutoff rank":              "eamcet cutoff rank closing branch",
    "lateral entry":            "lateral entry diploma ecet second year",
    "management quota":         "management quota admission seats fee",
    "nri quota":                "nri quota admission seats",

    # Fees
    "fees":                     "fee tuition annual amount rupees",
    "how much fee":             "fee tuition annual amount rupees semester",
    "how much is the fee":      "fee tuition annual amount rupees",
    "fee structure":            "fee tuition annual semester amount rupees",
    "total fees":               "fee tuition annual total amount rupees",
    "yearly fees":              "fee tuition annual amount rupees",
    "cost":                     "fee tuition cost amount",
    "scholarship":              "scholarship merit financial aid fee waiver reimbursement",
    "free reimbursement":       "scholarship fee reimbursement sc st bc government",

    # Courses / Departments
    "courses offered":          "btech mtech mba mca programmes branches offered departments",
    "what courses":             "btech programmes branches departments offered",
    "available branches":       "btech branches cse ece eee mechanical civil it aiml",
    "which branches":           "btech branches cse ece eee mechanical civil it aiml",
    "all branches":             "btech branches cse ece eee mechanical civil it mba mca",
    "departments":              "departments branches cse ece eee mechanical civil it",
    "programs":                 "btech mtech mba mca programs offered",
    "how many seats":           "seats intake total branches programs",
    "total seats":              "seats intake total branches programs",
    "cse seats":                "cse computer science seats intake 240",

    # Placements
    "placement":                "placement campus recruitment companies package lpa offers",
    "placements":               "placement campus recruitment companies package lpa offers",
    "job":                      "placement job recruitment company offer",
    "jobs":                     "placement job recruitment company offer",
    "top companies":            "placement recruiter companies mnc tcs infosys",
    "salary":                   "placement package lpa salary ctc offer",
    "package":                  "placement package lpa ctc salary offer",
    "highest package":          "placement highest package lpa ctc",
    "average package":          "placement average package lpa salary",
    "how many companies":       "placement companies recruited visited campus 200",
    "placement percentage":     "placement percentage eligible students placed",
    "tpc":                      "training placement cell tpc officer",
    "internship":               "internship summer industry training mandatory",

    # Contact
    "contact":                  "contact phone email address",
    "contact details":          "contact phone email address location",
    "contact number":           "phone number contact helpline",
    "phone number":             "phone number contact helpline 9100100510",
    "email":                    "email contact admissions",
    "address":                  "address location ibrahimpatnam hyderabad rangareddy",
    "where is cvr":             "address location ibrahimpatnam hyderabad nh65",
    "how to reach":             "address location ibrahimpatnam route directions",
    "location":                 "address location ibrahimpatnam hyderabad telangana",
    "distance from hyderabad":  "distance hyderabad 25 km ibrahimpatnam",
    "website":                  "website www cvr ac in",

    # Campus / Facilities
    "hostel":                   "hostel accommodation boys girls room facility",
    "hostel fee":               "hostel fee charges accommodation rupees year",
    "any hostel":               "hostel accommodation available boys girls",
    "boys hostel":              "hostel boys accommodation room warden",
    "girls hostel":             "hostel girls accommodation room warden female",
    "library":                  "library books digital resources ieee reading",
    "labs":                     "laboratory labs facilities infrastructure",
    "canteen":                  "canteen food cafeteria mess",
    "bus":                      "transport bus routes shuttle facility",
    "transport":                "transport bus routes facility fee",
    "sports":                   "sports ground gymnasium facilities cricket football",
    "gym":                      "gymnasium sports facility fitness",
    "wifi":                     "wifi internet campus high-speed",
    "auditorium":               "auditorium seating capacity 1000 events",
    "campus size":              "campus area 25 acres",
    "facilities":               "infrastructure facilities campus labs library hostel",

    # About CVR
    "about cvr":                "cvr college established founded history vision mission",
    "tell me about cvr":        "cvr college established founded history overview",
    "when was cvr established": "established founded year 2001 cvr college",
    "established":              "established founded year 2001 cvr",
    "affiliation":              "affiliated jntuh jntu university",
    "accreditation":            "naac nba aicte iso accreditation grade approved",
    "ranking":                  "naac nba nirf ranking grade",
    "naac":                     "naac accreditation grade quality",
    "nba":                      "nba accreditation programmes approved",
    "vision":                   "vision mission goals objectives",
    "is cvr good":              "placement naac nba accreditation ranking quality",

    # Research
    "research":                 "research publications patents projects grants",
    "phd":                      "phd research program jntuh affiliated",
    "mous":                     "mou collaboration tcs infosys microsoft aws industry",
    "hackathon":                "hackathon smart india technova coding competition",
    "technova":                 "technova technical fest events competitions",

    # Academics
    "cgpa":                     "cgpa sgpa grade points percentage calculation",
    "sgpa":                     "sgpa cgpa grade points percentage",
    "percentage":               "cgpa percentage calculation 10-point grade",
    "attendance":               "attendance 75% mandatory detained semester",
    "jntuh":                    "jntuh university affiliated hyderabad regulation",
    "results":                  "jntuh results jntuhresults examination",
    "supplementary":            "supplementary examination backlog fail",
    "backlog":                  "backlog supplementary examination fail reappear",
    "regulation":               "regulation r22 r20 jntuh syllabus",
    "first year":               "first year orientation curriculum subjects labs",
    "syllabus":                 "curriculum syllabus subjects topics r22 jntuh",

    # Faculty
    "faculty":                  "faculty professors phd qualified teaching staff",
    "number of faculty":        "faculty 200 professors phd teaching staff",
}

STOPWORDS = {
    "the","a","an","is","are","was","were","be","been","being","have","has","had",
    "do","does","did","will","would","could","should","may","might","shall","can",
    "and","but","or","nor","for","yet","so","although","though","while","since",
    "as","if","when","where","which","who","whom","that","this","these","those",
    "it","its","of","in","on","at","to","from","by","with","about","into",
    "please","hi","hello","hey","sir","madam","tell","give","me","my","we","you",
    "your","what","how","why","any","some","all","each","every","both","i",
}

# ── Build sentence corpus ────────────────────────────────────────────────────
def build_corpus():
    """Split all knowledge entries into individual sentences with metadata."""
    corpus = []
    for entry in CVR_KNOWLEDGE:
        raw = re.split(r'(?<=[.!?])\s+', entry["content"])
        for sent in raw:
            sent = sent.strip()
            if len(sent) > 25 and len(sent.split()) >= 5:
                corpus.append({
                    "sentence": sent,
                    "title": entry["title"],
                    "category": entry["category"],
                })
    return corpus

CORPUS = build_corpus()
SENTENCES = [r["sentence"] for r in CORPUS]

# ── Query normalisation ──────────────────────────────────────────────────────
def normalise(query: str) -> str:
    q = query.lower().strip()
    for phrase in sorted(QUERY_MAP.keys(), key=len, reverse=True):
        if phrase in q:
            return q.replace(phrase, QUERY_MAP[phrase])
    return q

def get_keywords(q: str) -> list:
    tokens = re.findall(r"[a-zA-Z0-9]+", q.lower())
    return [t for t in tokens if len(t) >= 3 and t not in STOPWORDS]

# ── Sentence scoring ─────────────────────────────────────────────────────────
def score_sentence(sentence: str, keywords: list) -> float:
    sl = sentence.lower()
    words = sl.split()
    hits = sum(1 for kw in keywords if kw in sl)
    hit_ratio = hits / max(len(keywords), 1)
    score = hit_ratio * 2.0

    # Boost: has a name/title
    if re.search(r'\b(dr|prof|mr|mrs|ms)\.?\s', sl):
        score += 0.5
    # Boost: contains numbers (fees, years, percentages)
    if re.search(r'\b\d{4,}\b|\b\d+\.?\d*\s*(lpa|lakhs?|rs\.?|rupees|%|seats|km)', sl):
        score += 0.4
    # Length sweet-spot (15–70 words)
    if 15 <= len(words) <= 70:
        score += 0.3
    elif len(words) > 90:
        score -= 0.3
    # Penalty: looks like nav/menu
    cap_words = sum(1 for w in words if w and w[0].isupper())
    if len(words) <= 10 and cap_words / max(len(words), 1) > 0.6:
        score -= 1.0
    return score

def keyword_hits(sentence: str, keywords: list) -> int:
    sl = sentence.lower()
    return sum(1 for kw in keywords if kw in sl)

# ── Deduplication ────────────────────────────────────────────────────────────
def dedupe(sentences: list) -> list:
    seen_keys = []
    result = []
    for s in sentences:
        key = re.sub(r'\W+', '', s.lower())[:80]
        is_dup = any(
            sum(a == b for a, b in zip(key, k)) / max(len(key), len(k)) > 0.75
            for k in seen_keys
        )
        if not is_dup:
            seen_keys.append(key)
            result.append(s)
    return result

# ── Main answer function ─────────────────────────────────────────────────────
def get_answer(query: str) -> str:
    if not SENTENCES:
        return "Knowledge base is empty."

    # Step 1: Normalise
    q_norm = normalise(query)
    keywords = get_keywords(q_norm)
    if not keywords:
        keywords = get_keywords(query.lower())

    # Step 2: Hard keyword filter
    filtered = [s for s in SENTENCES if keyword_hits(s, keywords) >= 1]

    # Relax: partial keyword match
    if len(filtered) < 3:
        short_kws = [k[:5] for k in keywords if len(k) >= 4]
        filtered = [s for s in SENTENCES if any(sk in s.lower() for sk in short_kws)]

    if not filtered:
        return (
            "I couldn't find specific information about that. "
            "Try asking about: admissions, EAMCET cutoffs, fees, courses, placements, "
            "hostel, transport, faculty, research, labs, or contact details. "
            "You can also visit www.cvr.ac.in or call +91-9100100510."
        )

    # Step 3: Keyword scoring
    scored = sorted(filtered, key=lambda s: score_sentence(s, keywords), reverse=True)
    top30 = scored[:30]

    # Step 4: TF-IDF cosine re-ranking
    if len(top30) >= 3:
        try:
            vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
            mat = vec.fit_transform(top30 + [q_norm])
            sims = cosine_similarity(mat[-1], mat[:-1]).flatten()
            order = sims.argsort()[::-1]
            top30 = [top30[i] for i in order]
        except Exception:
            pass

    # Step 5: Deduplicate and pick top sentences
    final = dedupe(top30)[:4]

    answer = " ".join(final).strip()
    answer = re.sub(r'\s+', ' ', answer)
    if not answer.endswith(('.', '!', '?')):
        answer += '.'
    return answer
