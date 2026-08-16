# Topic Modelling GUI Desktop Application — System Prompt

## Project Overview

Building a **desktop GUI application** that democratizes topic modelling for social scientists who lack deep programming knowledge. Eliminates the programming layer and provides intuitive access to various topic modelling algorithms.

**Core Goal:** Make topic modelling accessible to non-technical social scientists (sociologists, political scientists, media studies researchers) without requiring Python skills.

**Architecture:** MVC pattern with algorithm-agnostic design for easy scaling to LDA, NMF, and other algorithms.

---

## Technical Stack

### GUI Framework: ttkbootstrap
- Lightweight Tkinter wrapper with Bootstrap themes
- 60-90 MB bundle size (ideal for GitHub distribution)
- Excellent Claude code generation accuracy
- MVP development: 4-5 weeks

### Core Libraries
- **BERTopic** (MVP focus; LDA, NMF as future algorithms)
- **pandas/numpy** — Data handling
- **matplotlib/seaborn** — Static visualization export
- **plotly** — Interactive visualization export (browser)
- **scikit-learn** — Utilities for algorithms
- **gensim** — LDA support (future)

### Distribution
- **PyInstaller** — Standalone .exe/.app/.AppImage
- Bundle size: 70-90 MB
- GitHub Releases for academic users

---

## Key Design Decisions

### Why ttkbootstrap (not Bootstack or PyQt6)?
- Strong Claude knowledge (Bootstack too new, undocumented)
- Fast MVP (4-5 weeks vs 6-8 weeks with friction)
- Lightweight (60-90 MB vs 150+ MB with PyQt6)

### Why browser export (not embedded viz)?
- Lightweight app (no browser embedding libraries)
- Leverages BERTopic's native Plotly visualizations
- Familiar to researchers (R Studio model)

### Why desktop (not web/cloud)?
- **Privacy:** Data stays local
- **Trust:** Researchers handle sensitive data (interviews, surveys)
- **Offline:** No internet required
- **No liability:** No data storage responsibility

### Why algorithm-agnostic design?
- Start with BERTopic, expand to LDA/NMF without refactoring
- Centralized AppState + BaseAlgorithm abstraction
- Same UI for all algorithms (parameter forms auto-generate)

---

## User Experience for Social Scientists

### What Users See After Analysis
1. **Summary** — "Analysis complete • X docs • Y topics"
2. **Key metrics** — Topic count, avg docs/topic, model quality, outliers
3. **Top topics** (5-10) — Each with top terms and prevalence %
4. **Action buttons** — Export, view charts, try new parameters
5. **Model config** — Algorithm name, parameters used (for reproducibility)

### Design Philosophy
- **Clarity over aesthetics** — Plain language, no jargon
- **Interpretability first** — Show top terms, not embeddings
- **Actionability** — Every result screen has 3-4 next steps
- **Reproducibility** — Always show model configuration

---

## MVC Architecture

Three layers (detailed in ARCHITECTURE.md):

**MODEL** (no UI)
- AppState (centralized state management)
- TopicResult (standardized algorithm output)
- Algorithms (BaseAlgorithm abstraction + implementations)
- Services (DataLoader, Processor, Exporter, Visualizer)

**VIEW** (display only)
- ttkbootstrap panels (InputPanel, SettingsPanel, ProcessingPanel, ResultsPanel)
- Subscribe to AppState changes
- Never call algorithms or file I/O

**CONTROLLER** (orchestration)
- AppController (handles file selection, algorithm switching)
- AnalysisController (manages training pipeline)
- Updates AppState on user actions
- Notifies views to re-render

---

## Development Timeline (4-5 weeks)

**Week 1:** Project setup + MVP core (BaseAlgorithm, BERTopic, AppState)
**Week 2:** UI foundation (ttkbootstrap main window, panels)
**Week 3:** Results & export (tables, stats, CSV/JSON, Plotly export)
**Week 4:** Polish & testing (error handling, documentation, unit tests)
**Week 5 (optional):** PyInstaller packaging & GitHub setup

---

## For AI Coding Partner (Claude)

### How to Work with This Project
1. **Provide context upfront** — Paste relevant section from ARCHITECTURE.md or API.md
2. **Ask for specific modules** — "Generate `models/algorithms/bertopic.py` following BaseAlgorithm contract"
3. **Validate against contracts** — Check generated code against interfaces in API.md
4. **Test early** — Unit test each module as generated

### When to Ask Claude
- UI boilerplate (ttkbootstrap has great docs)
- Algorithm abstraction patterns
- Data processing logic
- Export functionality

### When to Write Code Yourself
- Visualization pipeline (understand BERTopic API first)
- Error handling & edge cases (domain expertise)
- PyInstaller configuration
- Threading/performance tuning

---

## Target Audience

**Primary Users:** Social scientists with research data but limited programming skills

**Characteristics:**
- Know research methods well
- Familiar with R, SPSS, NVivo
- Need reproducible, citable methods
- Handle sensitive data (privacy-conscious)
- Value interpretability over accuracy

**What they value:**
- Clear, understandable output
- Methodological transparency
- Export-friendly formats (CSV, JSON)
- Minimal setup (download, run, analyze)
- Documentation & tutorials

---

## Success Criteria

**MVP (Week 4)**
- User uploads CSV/TXT file ✓
- BERTopic trains successfully ✓
- Results display with topics, stats, config ✓
- Export to CSV/JSON ✓
- Interactive Plotly viz in browser ✓
- Zero crashes on happy path ✓

**Post-MVP** (if traction)
- LDA/NMF algorithms ✓
- Embedded matplotlib charts ✓
- Document search/filter ✓
- Batch processing ✓

---

## Related Documentation

- **ARCHITECTURE.md** — MVC structure, data flows, code patterns
- **API.md** — Component contracts (BaseAlgorithm, AppState, TopicResult)
- **DEVELOPMENT.md** — Setup, testing, deployment
- **README.md** — Installation, quick start, usage

---

## Important Files

- `claude.md` ← You are here (high-level context)
- `ARCHITECTURE.md` ← For development (patterns & data flows)
- `API.md` ← For component interfaces
- `DEVELOPMENT.md` ← For setup & testing

When starting a coding session, paste relevant sections from the appropriate doc.
