## Adding a New OMGN Meeting Session  

This document explains how to properly add a new session to the OMGN meetings archive.  
Two scenarios exist:

1. Adding a **recent meeting** (featured section)  
2. Archiving a meeting in the **old sessions list**

Please follow the workflow carefully to ensure consistency and long-term maintainability.

---

## 1️⃣ Adding a Recent Meeting  
_File:_ `_data/omgn-meetings.yml`

Recent meetings are displayed prominently on the website:
- Full title
- Location
- Year
- Link to the official meeting website
- Group picture
- Abstract book

Only **three** meetings are kept in this featured section (for performance reasons).

### Procedure

#### Step 1 — Insert the New Meeting

Add the new session at the **top** of `omgn-meetings.yml`.

Maintain the existing YAML structure and indentation.

Include:
- Title  
- Location  
- Dates  
- Website URL  
- Abstract book (PDF path)  
- Group picture (image path)

---

#### Step 2 — Maintain the “Three Meetings” Rule

After inserting the new meeting:

- The current meeting positioned as **#3** must be removed from this file.
- That meeting must then be transferred to `_data/old-omgn-meetings.yml` (see Section 2).

This guarantees that only the three most recent meetings remain featured.

---

## 2️⃣ Moving a Meeting to the Archive  
_File:_ `_data/old-omgn-meetings.yml`

Archived meetings are condensed entries:
- No external website link
- No displayed group picture
- Abstract book remains available

### Important

- The **group picture file must still be kept internally** in the repository.
- It is simply no longer displayed on the website (we may change that in the future).

### Procedure

1. Copy the meeting data.
2. Remove:
   - Website field
   - Group picture display field
3. Keep:
   - Title
   - Location
   - Year
   - Abstract book

Ensure chronological order is preserved.

---

## Abstract Book Preparation (Mandatory)

Before uploading any abstract book:

### A. Remove All Annotations

Many PDFs contain:
- Personal comments
- Track changes
- Hidden notes

These must be completely removed before publication.

**Do not upload annotated PDFs.**

If necessary:
- Open in a PDF editor.
- Remove all comments.
- Re-export a clean version.

---

### B. Use Controlled Compression

All abstract books must be compressed using:

👉 https://www.ilovepdf.com/compress_pdf

Compression setting:
- **Low compression**

Rationale:
- Preserves figure and text quality
- Avoids unnecessary disk usage
- Maintains professional archive standards

Do **not** use extreme compression.

---

## Final Checklist Before Commit

- [ ] YAML syntax validated  
- [ ] Only 3 meetings in `omgn-meetings.yml`  
- [ ] Older meeting transferred correctly  
- [ ] Abstract book cleaned from annotations  
- [ ] Abstract book compressed (low compression)  
- [ ] Group picture stored (even if archived)  
- [ ] Paths tested locally  

---

Maintaining clarity and structural discipline ensures that the OMGN archive 
remains sustainable, lightweight, and professionally curated for future meetings.

