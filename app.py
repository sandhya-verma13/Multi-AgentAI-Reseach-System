import os
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
import streamlit as st
from pipeline import run_research_pipeline

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Import fonts */
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap');

  /* Global */
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0c0f1a;
    color: #e2e8f0;
  }

  /* Hide Streamlit branding */
  #MainMenu, footer, header { visibility: hidden; }

  /* Main container */
  .main .block-container {
    max-width: 900px;
    padding: 2.5rem 2rem;
  }

  /* Hero header */
  .hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
  }

  .hero-subtitle {
    color: #64748b;
    font-size: 1rem;
    margin-bottom: 2.5rem;
    letter-spacing: 0.01em;
  }

  /* Input box */
  .stTextInput > div > div > input {
    background: #131929 !important;
    border: 1.5px solid #1e2d45 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
  }
  .stTextInput > div > div > input:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,0.15) !important;
  }

  /* Run button */
  .stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.65rem 2rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    letter-spacing: 0.01em;
  }
  .stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
  }
  .stButton > button:active {
    transform: translateY(0) !important;
  }

  /* Step cards */
  .step-card {
    background: #131929;
    border: 1px solid #1e2d45;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.25rem;
    transition: border-color 0.3s;
  }
  .step-card.active {
    border-color: #6366f1;
    box-shadow: 0 0 0 1px rgba(99,102,241,0.2);
  }
  .step-card.done {
    border-color: #10b981;
    box-shadow: 0 0 0 1px rgba(16,185,129,0.12);
  }

  .step-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
  }
  .step-badge {
    background: #1e2d45;
    color: #818cf8;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    text-transform: uppercase;
  }
  .step-badge.done {
    background: rgba(16,185,129,0.15);
    color: #10b981;
  }
  .step-badge.active {
    background: rgba(99,102,241,0.15);
    color: #818cf8;
  }

  .step-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #cbd5e1;
  }

  .step-content {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.7;
    color: #94a3b8;
    background: #0c0f1a;
    border-radius: 8px;
    padding: 1rem;
    max-height: 280px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
    border: 1px solid #1a2540;
  }

  /* Report card - special */
  .report-card {
    background: linear-gradient(145deg, #131929 0%, #0f1c2e 100%);
    border: 1.5px solid #6366f1;
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 0 30px rgba(99,102,241,0.08);
  }
  .report-body {
    color: #cbd5e1;
    font-size: 0.95rem;
    line-height: 1.85;
    white-space: pre-wrap;
  }

  /* Feedback card */
  .feedback-card {
    background: rgba(16,185,129,0.05);
    border: 1.5px solid #10b981;
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.25rem;
  }
  .feedback-body {
    color: #a7f3d0;
    font-size: 0.92rem;
    line-height: 1.85;
    white-space: pre-wrap;
  }

  /* Section labels */
  .section-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.9rem;
  }

  /* Divider */
  .divider {
    border: none;
    border-top: 1px solid #1e2d45;
    margin: 2rem 0;
  }

  /* Error box */
  .error-box {
    background: rgba(239,68,68,0.08);
    border: 1.5px solid #ef4444;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    color: #fca5a5;
    font-size: 0.9rem;
  }
</style>
""", unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🔬 Multi-Agent Research System</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Search → Scrape → Write → Critique — fully automated research pipeline</div>', unsafe_allow_html=True)

# ── Input Row ──────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_input(
        label="Research topic",
        placeholder="e.g. Advances in quantum error correction 2024",
        label_visibility="collapsed",
    )
with col_btn:
    run_clicked = st.button("Run →", use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Pipeline Execution ─────────────────────────────────────────────────────────
if run_clicked:
    if not topic.strip():
        st.markdown('<div class="error-box">⚠️ Please enter a research topic before running.</div>', unsafe_allow_html=True)
        st.stop()

    # Placeholders for live step cards
    ph_search   = st.empty()
    ph_reader   = st.empty()
    ph_writer   = st.empty()
    ph_critic   = st.empty()

    def render_step(placeholder, step_num, title, status, content=""):
        badge_cls  = "active" if status == "active" else ("done" if status == "done" else "")
        card_cls   = "active" if status == "active" else ("done" if status == "done" else "")
        badge_text = "Running…" if status == "active" else ("Complete" if status == "done" else "Pending")
        icon       = "⏳" if status == "active" else ("✅" if status == "done" else "○")
        content_html = f'<div class="step-content">{content}</div>' if content else ""
        placeholder.markdown(f"""
        <div class="step-card {card_cls}">
          <div class="step-header">
            <span class="step-badge {badge_cls}">{icon} Step {step_num} — {badge_text}</span>
            <span class="step-title">{title}</span>
          </div>
          {content_html}
        </div>
        """, unsafe_allow_html=True)

    # Mark all as pending
    render_step(ph_search, 1, "Search Agent — gathering sources",   "pending")
    render_step(ph_reader, 2, "Reader Agent — scraping top URL",    "pending")
    render_step(ph_writer, 3, "Writer Chain — drafting report",     "pending")
    render_step(ph_critic, 4, "Critic Chain — evaluating quality",  "pending")

    try:
        # ── Step 1: Search ─────────────────────────────────────────────────────
        render_step(ph_search, 1, "Search Agent — gathering sources", "active")

        from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

        search_agent  = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [{"role": "user", "content": f"Find recent and reliable information on the topic: {topic}"}]
        })
        search_text = search_result["messages"][-1].content
        render_step(ph_search, 1, "Search Agent — gathering sources", "done", search_text[:1200] + ("…" if len(search_text) > 1200 else ""))

        # ── Step 2: Reader ─────────────────────────────────────────────────────
        render_step(ph_reader, 2, "Reader Agent — scraping top URL", "active")

        reader_agent  = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [{"role": "user", "content": f"Based on the following search result about the '{topic}', Pick the most relevant URL and scrape it..."}]
        })
        scraped_text = reader_result["messages"][-1].content
        render_step(ph_reader, 2, "Reader Agent — scraping top URL", "done", scraped_text[:1200] + ("…" if len(scraped_text) > 1200 else ""))

        # ── Step 3: Writer ─────────────────────────────────────────────────────
        render_step(ph_writer, 3, "Writer Chain — drafting report", "active")

        research_combined = f"Search Result:\n{search_text}\n\nScraped Content:\n{scraped_text}"
        report = writer_chain.invoke({"topic": topic, "research": research_combined})
        render_step(ph_writer, 3, "Writer Chain — drafting report", "done", "Report generated — see below.")

        # ── Step 4: Critic ─────────────────────────────────────────────────────
        render_step(ph_critic, 4, "Critic Chain — evaluating quality", "active")

        feedback = critic_chain.invoke({"report": report})
        render_step(ph_critic, 4, "Critic Chain — evaluating quality", "done", "Feedback ready — see below.")

        # ── Results ────────────────────────────────────────────────────────────
        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        st.markdown('<div class="section-label">📄 Final Research Report</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="report-card"><div class="report-body">{report}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label">🧠 Critic Feedback</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="feedback-card"><div class="feedback-body">{feedback}</div></div>', unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="⬇ Download Report (.txt)",
            data=f"TOPIC: {topic}\n\n{'='*60}\nREPORT\n{'='*60}\n{report}\n\n{'='*60}\nCRITIC FEEDBACK\n{'='*60}\n{feedback}",
            file_name=f"research_{topic[:40].replace(' ','_')}.txt",
            mime="text/plain",
        )

    except Exception as e:
        st.markdown(f'<div class="error-box">❌ Pipeline error: <code>{e}</code></div>', unsafe_allow_html=True)

else:
    # Empty state
    st.markdown("""
    <div style="text-align:center; padding: 4rem 0; color: #2d3f5c;">
      <div style="font-size:3.5rem; margin-bottom:1rem;">🤖</div>
      <div style="font-family:'Space Grotesk',sans-serif; font-size:1.1rem; color:#334155;">
        Enter a topic above and hit <strong style="color:#818cf8;">Run →</strong> to start the pipeline.
      </div>
      <div style="margin-top:0.75rem; font-size:0.85rem; color:#1e3a5f;">
        Search Agent · Reader Agent · Writer Chain · Critic Chain
      </div>
    </div>
    """, unsafe_allow_html=True)