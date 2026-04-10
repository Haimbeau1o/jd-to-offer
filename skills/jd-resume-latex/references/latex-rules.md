# LaTeX Rules

## Source of Truth

The final resume source lives outside this repo:

- `/Volumes/passport/简历/latex-resume`

Reference file:

- `/Volumes/passport/简历/滴滴/docs/resume_latex_reference.md`

## Files To Edit

- `profile.tex`
  Use for identity fields, role title, contact info, photo path, and mode selection.
- `content.tex`
  Use for education, internships, projects, skills, highlights, and ordering.
- `resume-*.tex`
  Use only for thin theme or mode entry points.

## Presentation Rules

- Prefer stronger information hierarchy over decorative widgets.
- Let the first screenful prove fit for the role.
- Keep left-column content compact and secondary to the main experience proof.
- Use metrics sparingly and only when they are real and defensible.
- Avoid maintaining duplicate resume bodies in this repo.

## Verification Rules

Compile from `/Volumes/passport/简历/latex-resume` with `latexmk`.

Then check:
- visual balance on page 1
- no accidental overflow that breaks readability
- `pdftotext -layout` still contains the important headers, role title, and main experience bullets
