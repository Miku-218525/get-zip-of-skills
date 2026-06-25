---
name: get-zip-of-skills
description: Download GitHub repos as zip files, save to Desktop/skills/, and update the skills catalog HTML. Use when user asks to download, save, or archive a GitHub repo as a skill, or to add entries to the skills catalog.
---

# Get ZIP of Skills

Downloads a GitHub repository as a zip file to Desktop/skills/, extracts its README description, and updates the local skills-catalog.html index file.

## Workflow

1. User provides a GitHub repo in format owner/repo, e.g. user/skill-name
2. **Download**: Fetch the repo archive from GitHub (try main branch first, fallback to master)
3. **Read**: Parse the README.md to extract a description
4. **Index**: Update skills-catalog.html with the new entry
5. **Report**: Tell the user the saved file path and size

## Script

Use `scripts/download_skill.py <owner/repo>`.
This single command handles download, README parsing, and catalog update.

## Example

`
Use -zip-of-skills to download user/skill-name
`

The script outputs JSON with status, file size, and description.
