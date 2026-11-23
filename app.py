"""PRD Creator Platform — Product Development Pipeline"""
import streamlit as st
from pathlib import Path
from datetime import datetime
from typing import Any

from utils import (
    save_prds, load_prds, save_pipeline, load_pipeline,
    generate_prd_pdf, get_prd_template, get_research_template,
    save_research_history, load_research_history
)

st.set_page_config(
    page_title="PRD Platform",
    page_icon=":material/description:",
    layout="wide",
)

logo_path = Path(__file__).parent / "assets" / "logo.png"
if logo_path.exists():
    st.logo(str(logo_path), size="large")
else:
    st.sidebar.title("PRD Platform")

# ── Sample product database ──────────────────────────────────────────────────
PRODUCT_DATABASE = {
    "competitor_analysis": {
        "apps": [
            {"name": "Notion", "category": "Productivity", "features": ["docs", "databases", "collaboration", "templates"], "pricing": "Free–$16", "mvp_date": "2016"},
            {"name": "Coda", "category": "Productivity", "features": ["docs", "pipelines", "forms", "automation"], "pricing": "Free–$40", "mvp_date": "2019"},
            {"name": "Airtable", "category": "Database", "features": ["spreadsheets", "bases", "automation", "interfaces"], "pricing": "Free–$60", "mvp_date": "2012"},
            {"name": "Monday.com", "category": "Project Mgmt", "features": ["boards", "timeline", "gantt", "workflows"], "pricing": "$10–$18", "mvp_date": "2014"},
            {"name": "ClickUp", "category": "Project Mgmt", "features": ["tasks", "goals", "docs", "time tracking"], "pricing": "Free–$19", "mvp_date": "2017"},
        ]
    },
    "categories": ["Productivity", "Database", "Project Mgmt", "Design", "Development", "Communication"]
}

STAGES = ["Backlog", "Research", "PRD", "Design", "Dev", "QA", "Launched"]
STAGE_ICONS = {
    "Backlog": ":material/inventory_2:",
    "Research": ":material/manufacturing:",
    "PRD": ":material/description:",
    "Design": ":material/design_services:",
    "Dev": ":material/code:",
    "QA": ":material/bug_report:",
    "Launched": ":material/rocket_launch:",
}
STAGE_BADGE_COLORS = {
    "Backlog": "gray",
    "Research": "yellow",
    "PRD": "blue",
    "Design": "violet",
    "Dev": "green",
    "QA": "orange",
    "Launched": "green",
}
PRIORITY_OPTIONS = ["P0 — Critical", "P1 — High", "P2 — Medium", "P3 — Low"]

# ── Session state ────────────────────────────────────────────────────────────
def _init_state() -> None:
    st.session_state.setdefault("current_view", "dashboard")
    st.session_state.setdefault("prds", load_prds())
    st.session_state.setdefault("pipeline_items", load_pipeline())
    st.session_state.setdefault("editing_prd", None)

_init_state()


# ── Sidebar navigation ───────────────────────────────────────────────────────
NAV_ITEMS = [
    ("dashboard",    ":material/dashboard:",         "Dashboard"),
    ("create_prd",   ":material/edit_note:",          "Create PRD"),
    ("my_prds",      ":material/description:",       "My PRDs"),
    ("research",     ":material/science:",            "Creator research"),
    ("pipeline",     ":material/account_tree:",       "Pipeline"),
    ("compare_prds", ":material/compare_arrows:",     "Compare PRDs"),
    ("settings",     ":material/settings:",          "Settings"),
]

with st.sidebar:
    # Title handled by logo logic or sidebar fallback
    st.space("small")
    for view_id, icon, label in NAV_ITEMS:
        if st.button(label, key=f"nav_{view_id}", icon=icon, width="stretch"):
            st.session_state.current_view = view_id
            st.rerun()

# ── Helpers ───────────────────────────────────────────────────────────────────
def set_view(view: str) -> None:
    st.session_state.current_view = view


def _linked_prd(pr_id: str | None) -> dict | None:
    if not pr_id:
        return None
    return next((p for p in st.session_state.prds if p.get("title") == pr_id), None)


# ── Dashboard ─────────────────────────────────────────────────────────────────
def render_dashboard() -> None:
    st.title("Dashboard")

    prds = st.session_state.prds
    items = st.session_state.pipeline_items
    in_research = [i for i in items if i.get("stage") == "research"]
    in_progress = [i for i in items if i.get("stage") in {"dev", "qa"}]

    cols = st.columns(4)
    with cols[0]:
        with st.container(border=True):
            st.metric("Active PRDs", len(prds), icon=":material/description:")
    with cols[1]:
        with st.container(border=True):
            st.metric("Pipeline items", len(items), icon=":material/account_tree:")
    with cols[2]:
        with st.container(border=True):
            st.metric("In research", len(in_research), icon=":material/science:")
    with cols[3]:
        with st.container(border=True):
            st.metric("In progress", len(in_progress), icon=":material/code:")

    st.space("small")

    # Recent pipeline activity
    st.subheader("Recent pipeline items")
    if items:
        for item in items[-5:]:
            stage = item.get("stage", "backlog")
            badge_color = STAGE_BADGE_COLORS.get(stage.title(), "gray")
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{item.get('title', 'Untitled')}**")
                    if item.get("pr_id"):
                        st.caption(f":material/link: Linked to PRD: {item['pr_id']}")
                with c2:
                    st.badge(stage.title(), color=badge_color, icon=STAGE_ICONS.get(stage.title(), ":material/circle:"))
    else:
        st.caption("No pipeline items yet. Head to the pipeline tab to add some.")

    st.space("small")

    # Recent PRDs
    st.subheader("Recent PRDs")
    if prds:
        for prd in reversed(prds[-3:]):
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{prd.get('title', 'Untitled')}**")
                    st.caption(f"Updated {prd.get('updated', '—')}")
                with c2:
                    priority = prd.get("priority", "P2 — Medium")
                    st.badge(priority.split(" — ")[0] if " — " in priority else priority, color="violet")
    else:
        st.info("No PRDs yet. Start creating one!", icon=":material/lightbulb:")


# ── Create PRD ─────────────────────────────────────────────────────────────────
def render_create_prd() -> None:
    st.title("Create a PRD")

    prd = st.session_state.get("editing_prd") or get_prd_template()

    with st.form("prd_form", border=False):
        st.subheader("Overview")
        c1, c2 = st.columns(2)
        with c1:
            prd["title"] = st.text_input("Title", value=prd.get("title", ""), placeholder="e.g., Dark mode for editor")
            prd["product_name"] = st.text_input("Product name", value=prd.get("product_name", ""))
            prd["owner"] = st.text_input("Owner / product manager", value=prd.get("owner", ""))
        with c2:
            prd["priority"] = st.selectbox("Priority", PRIORITY_OPTIONS, index=PRIORITY_OPTIONS.index(prd.get("priority", "P1 — High")))
            launch_val = prd.get("target_launch", datetime.now().strftime("%Y-%m-%d"))
            try:
                launch_date = datetime.strptime(str(launch_val)[:10], "%Y-%m-%d").date()
            except (ValueError, TypeError):
                launch_date = datetime.now().date()
            prd["target_launch"] = str(st.date_input("Target launch", value=launch_date))

        st.subheader("Problem statement")
        prd["problem_statement"] = st.text_area("What problem are we solving?", height=100, value=prd.get("problem_statement", ""), placeholder="Describe the user pain point...", label_visibility="collapsed")

        st.subheader("Goals & success metrics")
        g1, g2 = st.columns(2)
        with g1:
            prd["goals"] = st.text_area("Goals", height=80, value=prd.get("goals", ""), placeholder="List 2–3 key goals…", label_visibility="collapsed")
        with g2:
            prd["success_metrics"] = st.text_area("Success metrics", height=80, value=prd.get("success_metrics", ""), placeholder="How will we measure success?", label_visibility="collapsed")

        st.subheader("User stories")
        prd["user_stories"] = st.text_area("Key user stories", height=100, value=prd.get("user_stories", ""), placeholder="As a [user], I want [goal] so that [benefit]…", label_visibility="collapsed")

        st.subheader("Features & requirements")
        prd["features"] = st.text_area("Features & requirements", height=150, value=prd.get("features", ""), placeholder="List features and technical requirements…", label_visibility="collapsed")

        st.subheader("Risks & assumptions")
        prd["risks"] = st.text_area("Potential risks and assumptions", height=100, value=prd.get("risks", ""), label_visibility="collapsed")

        st.subheader("Competitor notes")
        prd["competitor_notes"] = st.text_area("Competitor research notes", height=100, value=prd.get("competitor_notes", ""), label_visibility="collapsed")

        st.space("small")

        col_btn = st.columns([1, 1, 4])
        save_clicked = col_btn[0].form_submit_button("Save draft", icon=":material/save:", type="primary")
        create_clicked = col_btn[1].form_submit_button("Create PRD", icon=":material/check_circle:")

    if save_clicked or create_clicked:
        prd["updated"] = datetime.now().strftime("%Y-%m-%d")
        if save_clicked:
            prd["status"] = "draft"
        else:
            prd["status"] = "active"
            if not prd.get("created"):
                prd["created"] = datetime.now().strftime("%Y-%m-%d")
        st.session_state.prds.append(prd.copy())
        save_prds(st.session_state.prds)
        st.session_state.editing_prd = None
        set_view("my_prds")
        st.toast(f"PRD '{prd.get('title', 'Untitled')}' saved", icon=":material/check_circle:")
        st.rerun()


# ── My PRDs ───────────────────────────────────────────────────────────────────
def render_my_prds() -> None:
    st.title("My PRDs")

    if not st.session_state.prds:
        st.info("No PRDs yet. Start with \"Create PRD\"!", icon=":material/description:")
        return

    for i, prd in enumerate(reversed(st.session_state.prds)):
        real_idx = len(st.session_state.prds) - 1 - i
        title = prd.get("title", "Untitled")
        with st.container(border=True):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"#### {title}")
                priority = prd.get("priority", "P2 — Medium")
                st.badge(priority.split(" — ")[0] if " — " in priority else priority, color="violet")
                st.badge(prd.get("status", "draft"), color="gray")
            with c2:
                st.caption(f"Updated {prd.get('updated', '—')}")

            with st.expander("Details", expanded=False, icon=":material/visibility:"):
                st.markdown(f"**Owner** · {prd.get('owner', 'N/A')}")
                st.markdown(f"**Target launch** · {prd.get('target_launch', 'N/A')}")
                st.markdown(f"**Priority** · {prd.get('priority', 'N/A')}")
                st.markdown("---")
                st.markdown("**Problem statement**")
                st.write(prd.get("problem_statement", "N/A"))
                st.markdown("**Goals**")
                st.write(prd.get("goals", "N/A"))
                st.markdown("**Success metrics**")
                st.write(prd.get("success_metrics", "N/A"))
                st.markdown("**User stories**")
                st.write(prd.get("user_stories", "N/A"))
                st.markdown("**Features**")
                st.write(prd.get("features", "N/A"))

            c_edit, c_export, c_del = st.columns([1, 1, 1])
            if c_edit.button("Edit", key=f"edit_{real_idx}", icon=":material/edit:", width="stretch"):
                st.session_state.editing_prd = st.session_state.prds[real_idx].copy()
                set_view("create_prd")
                st.rerun()
            if c_export.button("Export", key=f"export_{real_idx}", icon=":material/download:", width="stretch"):
                md = generate_prd_pdf(st.session_state.prds[real_idx])
                st.download_button(
                    "Download Markdown",
                    md,
                    file_name=f"prd_{title.replace(' ', '_')}.md",
                    key=f"dl_{real_idx}",
                )
            if c_del.button("Delete", key=f"del_{real_idx}", icon=":material/delete:", width="stretch"):
                st.session_state.prds.pop(real_idx)
                save_prds(st.session_state.prds)
                st.toast("PRD deleted", icon=":material/delete:")
                st.rerun()

        st.space("small")


# ── Research hub ───────────────────────────────────────────────────────────────
def render_research() -> None:
    st.title("Creator research hub")
    st.caption("Research competitor products, analyze features, and generate insights.")

    with st.form("research_search", border=False):
        search_query = st.text_input("Search for similar products", placeholder="e.g., Notion, Airtable, Monday.com", label_visibility="collapsed")
        submitted = st.form_submit_button("Search", icon=":material/search:", type="primary")

    if submitted and search_query:
        st.session_state["research_query"] = search_query
    else:
        search_query = st.session_state.get("research_query", "")

    if search_query:
        matching = [a for a in PRODUCT_DATABASE["competitor_analysis"]["apps"]
                    if search_query.lower() in a["name"].lower()]
    else:
        matching = PRODUCT_DATABASE["competitor_analysis"]["apps"][:3]

    c_left, c_right = st.columns(2)

    with c_left:
        st.subheader("Competitive analysis")
        for app in matching:
            with st.container(border=True):
                st.markdown(f"**{app['name']}** · {app['category']}")
                st.caption(f"Features: {', '.join(app['features'])}")
                st.caption(f"Pricing: {app['pricing']}  ·  MVP: {app['mvp_date']}")

    with c_right:
        st.subheader("Feature matrix")
        if matching:
            import pandas as pd
            rows = []
            for app in matching:
                row: dict[str, Any] = {"Product": app["name"]}
                for cat in PRODUCT_DATABASE["categories"]:
                    row[cat] = "✓" if cat == app["category"] else ""
                rows.append(row)
            df = pd.DataFrame(rows).set_index("Product")
            st.dataframe(df, width="stretch")

        st.space("small")

        st.subheader("AI research assistant")
        with st.container(border=True):
            st.caption("Generate insights from your research in one click.")
            if st.button("Generate research summary", icon=":material/auto_awesome:", type="primary", key="gen_summary"):
                st.success("Research summary generated")
                st.write("Based on the products above, here are the key takeaways for your PRD.")
                st.balloons()


# ── Pipeline ───────────────────────────────────────────────────────────────────
def render_pipeline() -> None:
    st.title("Product development pipeline")
    st.caption("Track every item from backlog to launch. Link each item to its PRD to keep everything connected.")

    prds = st.session_state.prds
    items = st.session_state.pipeline_items

    # Stage columns — visual pipeline
    stage_cols = st.columns(len(STAGES))

    for idx, stage in enumerate(STAGES):
        stage_key = stage.lower()
        stage_items = [i for i in items if i.get("stage") == stage_key]
        icon = STAGE_ICONS[stage]
        color = STAGE_BADGE_COLORS[stage]

        with stage_cols[idx]:
            # Stage header
            st.markdown(f"**{icon} {stage}**")
            st.badge(str(len(stage_items)), color=color)

            st.space("small")

            # Items in this stage
            for item in stage_items:
                item_id = item.get("id")
                title = item.get("title", "Untitled")
                linked = _linked_prd(item.get("pr_id"))

                with st.container(border=True):
                    st.markdown(f"**{title}**")

                    # Linked PRD badge — visual connection
                    if linked:
                        st.caption(":material/link: " + linked.get("title", "Linked PRD"))
                        st.badge(linked.get("title", "PRD"), color="blue")
                    else:
                        st.caption(":material/link_off: Not linked to a PRD")

                    # Link / unlink
                    prd_titles = [""] + [p.get("title", "") for p in prds if p.get("title")]
                    current = item.get("pr_id") or ""
                    new_prd = st.selectbox(
                        "Link PRD",
                        prd_titles,
                        index=prd_titles.index(current) if current in prd_titles else 0,
                        key=f"link_{item_id}",
                        label_visibility="collapsed",
                    )
                    if new_prd != (item.get("pr_id") or ""):
                        item["pr_id"] = new_prd or None
                        save_pipeline(items)
                        st.toast("Link updated", icon=":material/link:")
                        st.rerun()

                    # Move buttons
                    stage_pos = STAGES.index(stage)
                    move_row = st.columns(2)
                    if move_row[0].button("←", key=f"back_{item_id}", icon=":material/arrow_back:", width="stretch"):
                        if stage_pos > 0:
                            item["stage"] = STAGES[stage_pos - 1].lower()
                            save_pipeline(items)
                            st.toast(f"Moved to {STAGES[stage_pos - 1]}", icon=":material/arrow_back:")
                            st.rerun()
                    if move_row[1].button("→", key=f"fwd_{item_id}", icon=":material/arrow_forward:", width="stretch"):
                        if stage_pos < len(STAGES) - 1:
                            item["stage"] = STAGES[stage_pos + 1].lower()
                            save_pipeline(items)
                            st.toast(f"Moved to {STAGES[stage_pos + 1]}", icon=":material/arrow_forward:")
                            st.rerun()

            st.space("small")

            # Add item button
            if st.button("Add item", key=f"add_{stage_key}", icon=":material/add:", width="stretch"):
                new_id = max([i.get("id", 0) for i in items], default=0) + 1
                items.append({"id": new_id, "title": f"New item in {stage}", "stage": stage_key, "pr_id": None})
                save_pipeline(items)
                st.toast(f"Added to {stage}", icon=":material/add:")
                st.rerun()

    st.space("small")
    st.caption("Tip: Use the arrow buttons on each card to move items between stages. Link a PRD so the pipeline stays connected to your documents.")


# ── Compare PRDs ────────────────────────────────────────────────────────────────
def render_compare_prds() -> None:
    st.title("Compare PRDs")
    st.caption("Compare two PRDs side by side to spot gaps and opportunities.")

    prds = st.session_state.prds
    if not prds:
        st.info("No PRDs to compare. Create some first!", icon=":material/description:")
        return

    prd_titles = [p.get("title", "Untitled") for p in prds]
    c1, c2 = st.columns(2)
    with c1:
        prd1_title = st.selectbox("First PRD", prd_titles, key="cmp_prd1")
    with c2:
        prd2_title = st.selectbox("Second PRD", prd_titles, key="cmp_prd2")

    prd1 = next((p for p in prds if p.get("title") == prd1_title), None)
    prd2 = next((p for p in prds if p.get("title") == prd2_title), None)

    if not prd1 or not prd2:
        st.info("Select two PRDs to compare.")
        return

    def _prd_card(prd: dict) -> None:
        with st.container(border=True):
            st.markdown(f"#### {prd.get('title', 'Untitled')}")
            st.markdown(f"- **Priority:** {prd.get('priority', 'N/A')}")
            st.markdown(f"- **Owner:** {prd.get('owner', 'N/A')}")
            st.markdown(f"- **Target launch:** {prd.get('target_launch', 'N/A')}")
            st.markdown(f"- **Problem:** {prd.get('problem_statement', 'N/A')[:200]}…")
            feat_count = len([l for l in prd.get("features", "").splitlines() if l.strip()])
            st.markdown(f"- **Features listed:** {feat_count}")

    c1, c2 = st.columns(2)
    with c1:
        _prd_card(prd1)
    with c2:
        _prd_card(prd2)

    st.space("small")
    st.subheader("Gap analysis")
    with st.container(border=True):
        p1_feats = set(l.strip().lower() for l in prd1.get("features", "").splitlines() if l.strip())
        p2_feats = set(l.strip().lower() for l in prd2.get("features", "").splitlines() if l.strip())
        only1 = p1_feats - p2_feats
        only2 = p2_feats - p1_feats
        if only1:
            st.markdown(f"**Only in {prd1_title}:**")
            for f in sorted(only1):
                st.markdown(f"- {f}")
        if only2:
            st.markdown(f"**Only in {prd2_title}:**")
            for f in sorted(only2):
                st.markdown(f"- {f}")
        if not only1 and not only2:
            st.caption("Both PRDs list the same features.")


# ── Settings ────────────────────────────────────────────────────────────────────
def render_settings() -> None:
    st.title("Settings")

    st.subheader("Data management")
    with st.container(border=True):
        import json
        if st.button("Export all data", icon=":material/download:", type="primary", width="stretch"):
            data = {
                "prds": st.session_state.prds,
                "pipeline": st.session_state.pipeline_items,
                "export_date": datetime.now().isoformat(),
            }
            st.download_button(
                "Download JSON",
                json.dumps(data, indent=2),
                file_name="prd_export.json",
                mime="application/json",
            )

    st.space("small")

    with st.container(border=True):
        confirm = st.checkbox("I confirm I want to delete all data")
        if st.button("Clear all data", icon=":material/delete:", type="secondary", width="stretch"):
            if confirm:
                st.session_state.prds = []
                st.session_state.pipeline_items = []
                save_prds([])
                save_pipeline([])
                st.toast("All data cleared", icon=":material/delete:")
            else:
                st.warning("Confirm the checkbox before clearing data.", icon=":material/warning:")

    st.space("small")

    st.subheader("Research templates")
    with st.container(border=True):
        st.caption("Quick templates for market analysis, competitor research, and user interviews.")
        if st.button("Open research template", icon=":material/description:", width="stretch"):
            tpl = get_research_template()
            st.session_state["research_template"] = tpl
            st.json(tpl, expanded=False)


# ── Router ────────────────────────────────────────────────────────────────────
VIEWS: dict[str, Any] = {
    "dashboard": render_dashboard,
    "create_prd": render_create_prd,
    "my_prds": render_my_prds,
    "research": render_research,
    "pipeline": render_pipeline,
    "compare_prds": render_compare_prds,
    "settings": render_settings,
}

view = st.session_state.get("current_view", "dashboard")
VIEWS.get(view, render_dashboard)()


if __name__ == "__main__":
    pass