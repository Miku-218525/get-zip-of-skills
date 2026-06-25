# Get ZIP of Skills

> Author: [miku](https://github.com/Miku-218525)  
> A Codex skill for downloading GitHub repos, saving as zip files, and maintaining a local skills catalog.

## 功能

Use this skill by telling Codex: "Use get-zip-of-skills to download owner/repo"

It will automatically:
1. Download the repo zip from GitHub
2. Save to Desktop/skills/{name}.zip
3. Parse README for description
4. Update the skills-catalog.html index page

## 目录结构

get-zip-of-skills/
├── SKILL.md
├── README.md
├── agents/openai.yaml
└── scripts/download_skill.py

## License: MIT
