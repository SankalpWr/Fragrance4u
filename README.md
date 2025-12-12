CMPE 255 Data Mining Project
# Fragrance4u – Bodywash to Perfume Recommendation System
## Course
**CMPE 255 – Data Mining**
San José State University

## Team Members
- Nikita Memane
- Katherine Le
- Sankalp Wahane

---

## Project Overview
Fragrance4u is an interpretable, data-mining–based recommendation system that
identifies perfumes with fragrance profiles similar to familiar scented products such as
bodywashes. The system uses structured fragrance-note analysis and hybrid similarity
scoring to recommend perfumes while providing transparent explanations for each
recommendation.

Unlike black-box recommendation models, Fragrance4u focuses on **explainability**,
**reproducibility**, and **end-to-end deployment**, making it suitable for real-world
consumer applications.

---

## Problem Statement
Consumers often struggle to choose perfumes because fragrance descriptions are
complex and unstructured. While people know which bodywashes or soaps they like,
mapping those preferences to perfumes is difficult. This project frames fragrance
matching as a **content-based similarity mining problem** and builds an interpretable
system to bridge that gap.

---

## Datasets

The project uses the following datasets:

- **Men’s Bodywash Dataset**
`Mens_Personal_Care_-_Keyword_Notes.xlsx`

- **Women’s Bodywash Dataset**
`womens_bodywash_top100_with_notes_only (1).csv`

- **Perfume Dataset**
`final_perfume_data (3).xlsx`

All datasets contain fragrance notes in free-text format and require preprocessing and
normalization.

---

## Methodology
The system follows a classical **data mining pipeline**:

1. **Text Normalization &amp; Tokenization**
- Lowercasing, punctuation cleanup, stopword removal
- Synonym/alias normalization (e.g., *orange blossom → neroli*)

2. **Candidate Pruning**

- Inverted indexing to reduce unnecessary comparisons

3. **Similarity Scoring**
- Hybrid scoring using:
- Jaccard similarity
- Token overlap
- TF-IDF cosine similarity (when available)
- Accord overlap
- Generic fragrance descriptors are down-weighted

4. **Recommendation &amp; Explanation**
- Top-K perfume recommendations
- Transparent matched-note explanations

---

## System Architecture
Input Datasets
↓

Preprocessing &amp; Normalization
↓
Similarity Scoring &amp; Ranking
↓
Evaluation &amp; Visualization
↓
CSV / Excel Outputs + Frontend Demo

## Project Structure
Fragrance4u/
├── README.md
├── report/
│ └── CMPE255_Final_Project_Report_Fragrance4u.pdf
├── presentation/
│ └── From_Shower_to_Scent_AI_Bodywash_Perfume_Matching.pptx
├── Demo Video/
│ └── project_demo.mp4
├── notebooks/
│ └── bodywash_to_perfume_recommender.ipynb
├── visuals/
│ ├── fig1_match_strength_distribution.png
│ ├── fig2_threshold_vs_coverage.png
│ └── fig3_generic_penalty_ablation.png
├── Python Files/
│ └── match_bodywash_to_perfume.py
├── datasets/
│ ├── Mens_Personal_Care_-_Keyword_Notes.xlsx
│ ├── womens_bodywash_top100_with_notes_only.csv
│ ├── final_perfume_data.xlsx
│ ├── bodywash_to_perfume_recommendations.csv
│ └── bodywash_to_perfume_recommendations_with_images.xlsx
├── public/
│ └── robots.txt
├── src/
│ ├── components/
│ │ ├── PerfumeDisplay.tsx
│ │ ├── ProductCard.tsx
│ │ └── SearchBar.tsx
│ ├── data/
│ │ └── products.ts
│ ├── hooks/
│ ├── lib/
│ └── pages/
│ ├── Index.tsx
│ └── NotFound.tsx
├── .gitignore
├── package.json
├── package-lock.json
├── vite.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── (other config files…)

---

## Evaluation &amp; Visualizations

The following plots are generated and discussed in the final report:

- `fig1_match_strength_distribution.png`  
  Distribution of normalized match-strength scores

- `fig2_threshold_vs_coverage.png`  
  Trade-off between confidence threshold and recommendation coverage

- `fig3_generic_penalty_ablation.png`  
  Ablation study comparing scoring with and without generic-accord penalization

---

## How to Run the Code

### Python Script

```bash
python match_bodywash_to_perfume.py \
  --men &quot;Mens_Personal_Care_-_Keyword_Notes.csv&quot; \
  --women &quot;womens_bodywash_top100_with_notes_only (1).csv&quot; \
  --perfumes &quot;final_perfume_data.csv&quot; \
  --out &quot;bodywash_to_perfume_recommendations.csv&quot; \
  --topk 5

Colab/Jupyter Notebook
Open:
notebooks/bodywash_to_perfume_recommender.ipynb
Run all cells to reproduce preprocessing, scoring, visualizations, and outputs.
CRISP-DM Methodology
This project follows the CRISP-DM framework:
• Business Understanding – fragrance discovery problem
• Data Understanding – unstructured fragrance notes
• Data Preparation – normalization and aliasing
• Modeling – similarity scoring
• Evaluation – metrics and ablation studies
• Deployment – frontend demo and reports
⸻

Deliverables
• Final Project Report (PDF)
• Documented Jupyter Notebook
• Python implementation
• Evaluation visualizations
• Frontend demo application
• Presentation slides
• Demo video

⸻
Notes
• All code is written from scratch.
• No pretrained recommendation models are used.
• The focus is on interpretability and data mining principles.
⸻
License
This project is submitted as part of an academic course and is intended for educational purposes
only.
