# PRD Creator Platform

A comprehensive web application for writing Product Requirement Documents (PRDs) and managing the end-to-end product development pipeline.

## Features

### PRD Studio
- Structured PRD templates with all required sections
- Problem statement, goals, user stories, technical requirements
- Success metrics and KPI tracking
- Save as draft or create as active PRD

### Creator Research Hub
- Competitor product database (Notion, Coda, Airtable, Monday.com, ClickUp)
- Feature comparison matrix
- AI-powered research insights generation
- Category-based analysis

### Product Development Pipeline
- Visual Kanban-style board with 7 stages: Backlog → Research → PRD → Design → Dev → QA → Launched
- Pipeline items visibly linked to their PRDs
- Quick stage progression with arrow buttons
- PRD linking capability keeps the pipeline connected to your documents

### Dashboard
- Real-time metrics and KPIs in card layout
- Pipeline status overview
- Recent activity feed

## Quick Start

```bash
cd prd_platform
python run.py
```

Then open http://localhost:8501 in your browser.

## Alternative: Direct Streamlit Run

```bash
streamlit run app.py
```

## Installation

Required packages:
- streamlit>=1.62.0
- pandas>=2.1.0
- openpyxl>=3.1.0
- python-docx>=0.8.11
- markdown>=3.5.0
- jinja2>=3.1.0
- pyyaml>=6.0.1
- python-dateutil>=2.8.2

Install with:
```bash
pip install -r requirements.txt
```

## Project Structure

```
prd_platform/
├── app.py              # Main application (modern UI)
├── utils.py            # Data persistence layer
├── run.py              # Entry point with auto-install
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml     # Theme configuration
```

## Usage

1. **Dashboard**: Overview of your PRD portfolio and pipeline metrics
2. **Create PRD**: Build structured requirement documents
3. **My PRDs**: View, edit, and manage all PRDs
4. **Creator Research**: Research competitors and generate insights
5. **Pipeline**: Manage product development across all stages with visual PRD links
6. **Compare PRDs**: Compare two PRDs side-by-side
7. **Settings**: Data export and management

## Design

The platform uses a modern, professional design with:
- Native Streamlit theming via `config.toml`
- Material Symbols icons for clean UI
- Card-based layouts with bordered containers
- Sentence-cased labels and headings
- Interactive badges for status indicators
- Visual pipeline connections showing which PRD each item links to