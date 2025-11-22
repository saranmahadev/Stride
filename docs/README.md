# Stride Documentation

This directory contains the source files for Stride's documentation site, built with [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Serve Locally

```bash
mkdocs serve
```

Then open http://127.0.0.1:8000 in your browser.

### Build Static Site

```bash
mkdocs build
```

Output will be in the `site/` directory.

## Structure

```
docs/
├── index.md                # Homepage
├── getting-started/        # Installation, quick start, concepts
├── user-guide/             # Complete CLI reference
├── ai-agents/              # AI tool integrations
├── tutorials/              # Step-by-step guides
├── api/                    # API reference
├── development/            # Contributing, architecture
├── about/                  # Roadmap, changelog, FAQ
├── stylesheets/            # Custom CSS (red theme)
├── javascripts/            # Custom JS
└── assets/                 # Images, logos
```

## Theme

Stride documentation uses a custom red color theme (`#d32f2f`) to match the brand identity.

- **Primary:** Material Red 700
- **Accent:** Red A200
- **Custom CSS:** `stylesheets/extra.css`
- **Custom JS:** `javascripts/extra.js`

## Deployment

Documentation is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the `main` branch.

### Manual Deployment

```bash
mkdocs gh-deploy
```

## Contributing

When adding new documentation:

1. Create markdown files in appropriate directories
2. Update navigation in `mkdocs.yml`
3. Follow existing style and formatting
4. Test locally with `mkdocs serve`
5. Submit pull request

## Style Guide

- Use ATX-style headers (`#` not `===`)
- Include code examples with proper syntax highlighting
- Add admonitions for tips, warnings, notes
- Use Mermaid diagrams for workflows
- Keep paragraphs concise (2-3 sentences)
- Link to related pages

## Requirements

- Python 3.11+
- MkDocs 1.5.3+
- Material for MkDocs 9.4.14+
- Various plugins (see requirements.txt)

## Support

- **Issues**: https://github.com/saranmahadev/Stride/issues
- **Discussions**: https://github.com/saranmahadev/Stride/discussions
