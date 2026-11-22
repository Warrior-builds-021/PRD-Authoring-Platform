"""Utility functions for PRD Platform"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

DATA_DIR = Path.home() / ".prd_platform"
DATA_DIR.mkdir(exist_ok=True)

PRDS_FILE = DATA_DIR / "prds.json"
PIPELINE_FILE = DATA_DIR / "pipeline.json"
RESEARCH_FILE = DATA_DIR / "research_history.json"

def save_prds(prds: List[Dict]) -> None:
    """Save PRDs to local storage"""
    with open(PRDS_FILE, 'w') as f:
        json.dump(prds, f, indent=2, default=str)

def load_prds() -> List[Dict]:
    """Load PRDs from local storage"""
    if PRDS_FILE.exists():
        with open(PRDS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_pipeline(items: List[Dict]) -> None:
    """Save pipeline items to local storage"""
    with open(PIPELINE_FILE, 'w') as f:
        json.dump(items, f, indent=2, default=str)

def load_pipeline() -> List[Dict]:
    """Load pipeline items from local storage"""
    if PIPELINE_FILE.exists():
        with open(PIPELINE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_research_history(history: List[Dict]) -> None:
    """Save research history"""
    with open(RESEARCH_FILE, 'w') as f:
        json.dump(history, f, indent=2, default=str)

def load_research_history() -> List[Dict]:
    """Load research history"""
    if RESEARCH_FILE.exists():
        with open(RESEARCH_FILE, 'r') as f:
            return json.load(f)
    return []

def generate_prd_pdf(prd: Dict) -> str:
    """Generate markdown representation of PRD for export"""
    md = f"""# {prd.get('title', 'PRD Title')}

## Product Information
- **Product Name**: {prd.get('product_name', 'N/A')}
- **Owner**: {prd.get('owner', 'N/A')}
- **Priority**: {prd.get('priority', 'N/A')}
- **Created**: {prd.get('created', 'N/A')}
- **Updated**: {prd.get('updated', 'N/A')}
- **Target Launch**: {prd.get('target_launch', 'N/A')}

## Problem Statement

{prd.get('problem_statement', 'N/A')}

## Goals

{prd.get('goals', 'N/A')}

## Success Metrics

{prd.get('success_metrics', 'N/A')}

## User Stories

{prd.get('user_stories', 'N/A')}

## Requirements & Features

{prd.get('features', 'N/A')}

## Risks & Assumptions

{prd.get('risks', 'N/A')}
"""
    return md

def get_prd_template() -> Dict:
    """Return a PRD template with default structure"""
    return {
        "title": "",
        "product_name": "",
        "owner": "",
        "target_launch": datetime.now().strftime("%Y-%m-%d"),
        "priority": "P1 - High",
        "status": "draft",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "problem_statement": "",
        "goals": "",
        "success_metrics": "",
        "user_stories": "",
        "features": "",
        "risks": ""
    }

def get_research_template() -> Dict:
    """Return a research template structure"""
    return {
        "title": "",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "competitors_analyzed": [],
        "key_differences": [],
        "market_gaps": [],
        "feature_recommendations": [],
        "notes": ""
    }