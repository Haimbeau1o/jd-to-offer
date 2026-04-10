# JD Resume LaTeX Workflow

## Goal

Turn a target JD into a closed-loop resume adaptation flow:

1. understand the role deeply
2. map required proof to real candidate assets
3. package one experience professionally without overclaiming
4. sync the result into the LaTeX resume source of truth

## Operating Sequence

### Step 1: Gather the role context

Use one of:
- user-provided JD markdown
- existing case bundle under `cases/`
- existing role analysis under `docs/examples/` or `docs/plans/`

If the role is current or user asks for latest sources, browse and prefer official sources.

### Step 2: Produce the proof map

For each role, answer:
- what does this role optimize for
- what technical proof is mandatory
- what business proof is preferred
- what can be bridged from adjacent experience
- what must not be faked

### Step 3: Build the source pack for the target experience

For the selected internship or project, gather:
- user-confirmed tasks
- local repo artifacts
- official company/product signals
- official engineering or product docs

### Step 4: Write the packaging output

Produce:
- one dominant storyline
- one one-sentence summary
- up to three bullets
- one interview bridge sentence
- one forbidden claims list

### Step 5: Sync to LaTeX

Edit only the real resume project:
- `/Volumes/passport/简历/latex-resume/profile.tex`
- `/Volumes/passport/简历/latex-resume/content.tex`

### Step 6: Verify

Run:
- `latexmk -xelatex -interaction=nonstopmode -halt-on-error -output-directory=out <entry>.tex`
- `pdftotext -layout <pdf> -`

Inspect both visual hierarchy and text extraction.
