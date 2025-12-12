
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
match_bodywash_to_perfume.py
--------------------------------
Bodywash → Perfume recommender based on note/accord similarity.

Usage (CLI):
  python match_bodywash_to_perfume.py \
      --men "Mens_Personal_Care_-_Keyword_Notes.csv" \
      --women "womens_bodywash_top100_with_notes_only (1).csv" \
      --perfumes "final_perfume_data.csv" \
      --out "bodywash_to_perfume_recommendations.csv" \
      --topk 5
"""
import argparse, re, math
from dataclasses import dataclass
from typing import Iterable, List, Dict, Tuple, Optional
import numpy as np, pandas as pd

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False

PUNCT_RE = re.compile(r"[^\w\s'-]+", re.UNICODE)
WS_RE = re.compile(r"\s+")

SYNONYMS = {
    "agarwood": "oud", "oud wood": "oud", "oudh": "oud",
    "gaiac": "gaiac wood", "oak moss": "oakmoss", "mousse de chene": "oakmoss",
    "benzoin resin": "benzoin", "elemi resin": "elemi", "labdanum resin": "labdanum",
    "muguet": "lily-of-the-valley", "lily of the valley": "lily-of-the-valley",
    "rose damascena": "rose", "rose de mai": "rose", "bulgarian rose": "rose",
    "jasmin": "jasmine", "sambac jasmine": "jasmine", "ylang ylang": "ylang-ylang",
    "calabrian bergamot": "bergamot", "sicilian lemon": "lemon",
    "vanille": "vanilla", "tonka bean": "tonka", "tonka beans": "tonka",
    "cardamon": "cardamom", "cacao": "cocoa", "sugar": "sweet",
    "ambergris": "amber", "ambrox": "ambroxan",
    "sea water": "sea notes", "sea breeze": "sea notes",
    "herbal": "aromatic",
}
STOPWORDS = {"note","notes","accord","accords","and","with","of","the","a","an","essence","oil","absolute","extract","accorde"}

def normalize_text(s: str) -> str:
    s = s.strip().lower().replace("–","-").replace("—","-").replace("/", " ")
    s = PUNCT_RE.sub(" ", s); s = WS_RE.sub(" ", s)
    return s.strip()

def split_terms(s: str) -> List[str]:
    if not s: return []
    parts = re.split(r"[;,+|]", s)
    out = []
    for p in parts:
        p = normalize_text(p)
        if p: out.append(p.strip())
    return out

def canonical(term: str) -> str:
    t = term.strip().lower().replace("’","'").replace("`","'")
    t = re.sub(r"\s+", " ", t).strip(" -")
    t = SYNONYMS.get(t, t)
    if t in STOPWORDS: return ""
    return t

def to_token_set(s: str) -> List[str]:
    terms = split_terms(s); toks = []
    for t in terms:
        can = canonical(t)
        if not can: continue
        toks.append(can)
        if " " in can:
            head = can.split()[-1]
            if head not in STOPWORDS and len(head) > 2:
                toks.append(head)
    seen, out = set(), []
    for x in toks:
        if x and x not in seen:
            out.append(x); seen.add(x)
    return out

def jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    A, B = set(a), set(b)
    return 0.0 if not A and not B else len(A & B) / len(A | B)

def overlap_score(a: Iterable[str], b: Iterable[str]) -> float:
    A, B = set(a), set(b)
    if not A or not B: return 0.0
    return len(A & B) / max(1, min(len(A), len(B)))

def soft_match_terms(a: List[str], b: List[str]):
    A, B = set(a), set(b)
    common = sorted(A & B)
    a_words = {w for t in A for w in t.split() if len(w)>2 and w not in STOPWORDS}
    b_words = {w for t in B for w in t.split() if len(w)>2 and w not in STOPWORDS}
    extra = sorted((a_words & b_words) - set(" ".join(common).split()))
    return common, extra

@dataclass
class Weights:
    w_jaccard: float = 0.45
    w_overlap: float = 0.25
    w_tfidf: float = 0.20
    w_accords: float = 0.10

def build_tfidf_corpus(strings: List[str]):
    if not SKLEARN_AVAILABLE: return None, None
    vec = TfidfVectorizer(
        analyzer="word",
        token_pattern=r"(?u)\b\w[\w-]+\b",
        ngram_range=(1,2),
        min_df=1,
        lowercase=True
    )
    mat = vec.fit_transform(strings)
    return vec, mat

def cosine(vec, mat, s: str):
    if vec is None or mat is None: return np.zeros((mat.shape[0],), dtype=float) if mat is not None else np.zeros((0,), dtype=float)
    from sklearn.metrics.pairwise import cosine_similarity
    q = vec.transform([s])
    return cosine_similarity(q, mat)[0]

def score_bodywash_to_perfume(bw_notes, pf_notes_list, pf_accords_list=None, weights: Weights = Weights()):
    bw_tokens = to_token_set(bw_notes or "")
    pf_tokens_list = [to_token_set(x or "") for x in pf_notes_list]
    j_scores = np.array([jaccard(bw_tokens, t) for t in pf_tokens_list], dtype=float)
    o_scores = np.array([overlap_score(bw_tokens, t) for t in pf_tokens_list], dtype=float)

    tfidf_corpus = [normalize_text(x or "") for x in pf_notes_list]
    if SKLEARN_AVAILABLE:
        vec, mat = build_tfidf_corpus(tfidf_corpus)
        c_scores = cosine(vec, mat, normalize_text(bw_notes or ""))
    else:
        c_scores = np.zeros_like(j_scores)

    if pf_accords_list is not None and any(pf_accords_list):
        bw_acc = to_token_set(", ".join(split_terms(bw_notes)))
        pf_acc_tokens = [to_token_set(x or "") for x in pf_accords_list]
        a_scores = np.array([overlap_score(bw_acc, t) for t in pf_acc_tokens], dtype=float)
    else:
        a_scores = np.zeros_like(j_scores)

    final = (weights.w_jaccard*j_scores + weights.w_overlap*o_scores +
             weights.w_tfidf*c_scores + weights.w_accords*a_scores)

    diag = {}
    for idx, pf_toks in enumerate(pf_tokens_list):
        common, extra = soft_match_terms(bw_tokens, pf_toks)
        diag[idx] = {"match_terms": common, "word_overlap": extra}
    return final, diag

def first_col(df: pd.DataFrame, candidates):
    cols = {c.lower(): c for c in df.columns}
    for name in candidates:
        if name.lower() in cols: return cols[name.lower()]
    return None

def load_bodywash_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    notes_col = first_col(df, ["notes","note","fragrance_notes","scent notes","scent"])
    if not notes_col: raise ValueError(f"No 'Notes' column found in {path}")
    df["_bw_notes"] = df[notes_col].fillna("").astype(str)
    return df

def load_perfumes_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    notes_col = first_col(df, ["notes","key notes","Key Notes","note"])
    if not notes_col: raise ValueError(f"No 'Notes' column found in {path}")
    brand_col = first_col(df, ["brand"])
    name_col = first_col(df, ["name","fragrance","product"])
    accords_col = first_col(df, ["main accords","accords"])
    df["_pf_notes"] = df[notes_col].fillna("").astype(str)
    df["_pf_accords"] = df[accords_col].fillna("").astype(str) if accords_col else ""
    df["_pf_brand"] = df[brand_col].fillna("").astype(str) if brand_col else ""
    df["_pf_name"] = df[name_col].fillna("").astype(str) if name_col else ""
    return df

def recommend_for_df(bw_df: pd.DataFrame, pf_df: pd.DataFrame, topk: int = 5, weights: Weights = Weights()):
    pf_notes = pf_df["_pf_notes"].tolist()
    pf_accs = pf_df["_pf_accords"].tolist() if "_pf_accords" in pf_df.columns else None
    recs = []
    for i, row in bw_df.iterrows():
        bw_notes = row["_bw_notes"]
        scores, diag = score_bodywash_to_perfume(bw_notes, pf_notes, pf_accs, weights)
        top_idx = np.argsort(scores)[::-1][:topk]
        for rank, j in enumerate(top_idx, 1):
            recs.append({
                "bw_index": i,
                "bw_notes": bw_notes,
                "rank": rank,
                "score": round(float(scores[j]), 6),
                "perfume_brand": pf_df.loc[j, "_pf_brand"],
                "perfume_name": pf_df.loc[j, "_pf_name"],
                "perfume_notes": pf_df.loc[j, "_pf_notes"],
                "perfume_accords": pf_df.loc[j, "_pf_accords"] if "_pf_accords" in pf_df.columns else "",
                "matched_terms": ", ".join(diag[j]["match_terms"]),
                "word_overlap": ", ".join(diag[j]["word_overlap"]),
            })
    return pd.DataFrame(recs)

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--men", type=str, help="Men bodywash CSV")
    ap.add_argument("--women", type=str, help="Women bodywash CSV")
    ap.add_argument("--perfumes", type=str, required=True, help="Perfume CSV")
    ap.add_argument("--out", type=str, default="bodywash_to_perfume_recommendations.csv")
    ap.add_argument("--topk", type=int, default=5)
    ap.add_argument("--w", nargs=4, type=float, metavar=("W_JACC","W_OVER","W_TFIDF","W_ACCR"),
                    help="Weights for Jaccard, Overlap, TF-IDF, Accords")
    args = ap.parse_args()

    pf_df = load_perfumes_csv(args.perfumes)

    frames = []
    if args.men:
        men_df = load_bodywash_csv(args.men); men_df["_source"]="men"; frames.append(men_df)
    if args.women:
        wom_df = load_bodywash_csv(args.women); wom_df["_source"]="women"; frames.append(wom_df)
    if frames:
        bw_df = pd.concat(frames, ignore_index=True)
    else:
        raise SystemExit("Please provide at least one bodywash CSV via --men or --women")

    weights = Weights()
    if args.w: weights = Weights(*args.w)

    rec_df = recommend_for_df(bw_df, pf_df, topk=args.topk, weights=weights)

    keep_cols = [c for c in bw_df.columns if not c.startswith("_")]
    out = rec_df.merge(bw_df[keep_cols + ["_bw_notes"]], left_on="bw_index", right_index=True, how="left")
    out.to_csv(args.out, index=False)
    print(f"Saved recommendations to {args.out} (rows: {len(out)})")

if __name__ == "__main__":
    main()
