# JD to Offer Workflow

## Goal

Turn a JD into a reusable preparation bundle that helps the user study efficiently, build one role-aligned flagship project, and speak convincingly in interviews.

## Operating Steps

1. Normalize the input JD into structured sections.
2. Map the JD to the competency taxonomy and rank the top capability areas.
3. Run `scaffold-research` to create a case-specific research template.
4. Browse for current resources. Prefer official docs, primary papers, and official repos.
5. Save the web-verified findings into a YAML override file.
6. Run `generate --resource-overrides ...` so the latest findings are merged into the resource pack.
7. Design one flagship project that spans the top competencies and matches the role's business context.
8. Write interview-ready assets: resume bullets, project storyline, and likely follow-up questions.
9. Validate the output bundle.

## Browsing Guidance

For software frameworks or libraries, use official documentation first. For methods or algorithms, use primary papers first. For business grounding, use official company resources or top-tier conference papers.

## Quality Bar

A strong bundle should let the user answer these questions without improvising:

- What exactly does this JD optimize for?
- Which foundations should I study, and in what order?
- What one project best proves fit for this role?
- What metrics, trade-offs, and failure cases should I discuss in interviews?
