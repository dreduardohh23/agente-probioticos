"""
DASHBOARD ESTRATEGICO - Agente Probioticos
Genomma Lab | Visualizacion interactiva del reporte estrategico
"""

import streamlit as st

st.set_page_config(
    page_title="Dashboard Estrategico | Genomma Lab",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Dark scientific CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .block-container { padding-top: 1rem; max-width: 1400px; }

    /* Dashboard Header */
    .dash-header {
        background: linear-gradient(135deg, #0A0E1A 0%, #111827 50%, #0D1B2A 100%);
        border: 1px solid rgba(0, 212, 170, 0.2);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .dash-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00D4AA, #00B4D8, #7C3AED, #00D4AA);
        background-size: 200% 100%;
        animation: shimmer 3s infinite;
    }
    @keyframes shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }
    .dash-header h1 {
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.03em;
    }
    .dash-header .subtitle {
        color: #00D4AA;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 0.3rem;
    }
    .dash-header .date {
        color: #64748B;
        font-size: 0.75rem;
        margin-top: 0.5rem;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(145deg, #111827, #0D1B2A);
        border: 1px solid rgba(0, 212, 170, 0.15);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        background: var(--accent, #00D4AA);
    }
    .kpi-value {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: var(--accent, #00D4AA);
        line-height: 1;
    }
    .kpi-label {
        color: #94A3B8;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.4rem;
    }
    .kpi-detail {
        color: #64748B;
        font-size: 0.7rem;
        margin-top: 0.2rem;
    }

    /* Section Headers */
    .section-header {
        background: linear-gradient(135deg, #111827, #0D1B2A);
        border-left: 3px solid #00D4AA;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1.2rem;
        margin: 1.5rem 0 1rem 0;
    }
    .section-header h3 {
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        margin: 0;
    }

    /* Data Table */
    .data-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: #111827;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .data-table th {
        background: linear-gradient(135deg, #0D2137, #132D46);
        color: #00D4AA;
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 0.8rem 1rem;
        text-align: left;
        border-bottom: 2px solid rgba(0, 212, 170, 0.3);
    }
    .data-table td {
        color: #CBD5E1;
        font-size: 0.8rem;
        padding: 0.7rem 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.03);
    }
    .data-table tr:hover td { background: rgba(0, 212, 170, 0.05); }

    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 700;
    }
    .badge-green { background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-blue { background: rgba(59, 130, 246, 0.15); color: #3B82F6; border: 1px solid rgba(59, 130, 246, 0.3); }
    .badge-amber { background: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-red { background: rgba(239, 68, 68, 0.15); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-purple { background: rgba(139, 92, 246, 0.15); color: #8B5CF6; border: 1px solid rgba(139, 92, 246, 0.3); }

    /* Progress bar */
    .progress-container {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin-top: 0.3rem;
    }
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #00D4AA, #00B4D8);
    }

    /* Chart card */
    .chart-card {
        background: #111827;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1.5rem;
    }
    .chart-title {
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* Bar chart CSS */
    .bar-row {
        display: flex;
        align-items: center;
        margin-bottom: 0.6rem;
    }
    .bar-label {
        color: #94A3B8;
        font-size: 0.75rem;
        width: 140px;
        flex-shrink: 0;
    }
    .bar-track {
        flex: 1;
        background: rgba(255,255,255,0.05);
        border-radius: 6px;
        height: 24px;
        overflow: hidden;
        position: relative;
    }
    .bar-fill {
        height: 100%;
        border-radius: 6px;
        display: flex;
        align-items: center;
        padding-left: 0.5rem;
        font-size: 0.7rem;
        font-weight: 700;
        color: white;
    }

    /* Alert box */
    .alert-box {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.25);
        border-left: 3px solid #EF4444;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
    }
    .alert-box .alert-title { color: #EF4444; font-weight: 700; font-size: 0.8rem; }
    .alert-box .alert-text { color: #CBD5E1; font-size: 0.78rem; margin-top: 0.3rem; }

    /* Opportunity box */
    .opp-box {
        background: rgba(0, 212, 170, 0.05);
        border: 1px solid rgba(0, 212, 170, 0.2);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .opp-box .opp-title { color: #00D4AA; font-weight: 700; font-size: 0.85rem; }
    .opp-box .opp-text { color: #CBD5E1; font-size: 0.78rem; margin-top: 0.3rem; }

    /* Timeline */
    .timeline-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1rem;
        padding-left: 1.5rem;
        border-left: 2px solid rgba(0, 212, 170, 0.3);
        position: relative;
    }
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -5px;
        top: 0.3rem;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #00D4AA;
    }
    .timeline-phase { color: #00D4AA; font-weight: 700; font-size: 0.8rem; width: 80px; flex-shrink: 0; }
    .timeline-content { color: #CBD5E1; font-size: 0.78rem; }
    .timeline-markets { color: #94A3B8; font-size: 0.7rem; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="dash-header">
    <h1>📊 Dashboard Estrategico — Agente Probioticos</h1>
    <div class="subtitle">Genomma Lab Internacional | Celula de Innovacion en Probioticos</div>
    <div class="date">Reporte generado: Marzo 2026 | CONFIDENCIAL</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# KPIs ROW
# ═══════════════════════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown("""
    <div class="kpi-card" style="--accent: #00D4AA;">
        <div class="kpi-value">3</div>
        <div class="kpi-label">Productos en Pipeline</div>
        <div class="kpi-detail">Prob+BBR | Prob+Vit | Gomita</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="kpi-card" style="--accent: #3B82F6;">
        <div class="kpi-value">$65-70B</div>
        <div class="kpi-label">Mercado Global</div>
        <div class="kpi-detail">Probioticos 2024 | CAGR 7-9%</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="kpi-card" style="--accent: #8B5CF6;">
        <div class="kpi-value">6</div>
        <div class="kpi-label">Cepas Nivel 1</div>
        <div class="kpi-detail">Evidencia clinica alta</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="kpi-card" style="--accent: #F59E0B;">
        <div class="kpi-value">8+</div>
        <div class="kpi-label">Mercados Target</div>
        <div class="kpi-detail">MX, USA, BR, CO, PE, CL, AR</div>
    </div>""", unsafe_allow_html=True)

with k5:
    st.markdown("""
    <div class="kpi-card" style="--accent: #EF4444;">
        <div class="kpi-value">0</div>
        <div class="kpi-label">Competidores BBR+Prob</div>
        <div class="kpi-detail">First-mover advantage</div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PORTAFOLIO DE PRODUCTOS
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header"><h3>🧬 PORTAFOLIO PROPUESTO</h3></div>
""", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)

with p1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">PRODUCTO 1: Probiotico + Berberina</div>
        <span class="badge badge-green">FIRST-TO-MARKET</span>
        <br><br>
        <table class="data-table">
            <tr><td style="color:#94A3B8;">Formula</td><td>6 cepas (3.3x10<sup>10</sup> UFC) + BBR 1000mg</td></tr>
            <tr><td style="color:#94A3B8;">Indicacion</td><td>SII + DM2 + Resistencia insulina</td></tr>
            <tr><td style="color:#94A3B8;">Forma</td><td>Sachet monodosis / DRcaps</td></tr>
            <tr><td style="color:#94A3B8;">Precio</td><td><span style="color:#00D4AA;font-weight:700;">$15-25 USD/mes</span></td></tr>
            <tr><td style="color:#94A3B8;">Mercados</td><td>MX, LATAM, USA</td></tr>
        </table>
        <br>
        <div style="color:#94A3B8;font-size:0.7rem;">EVIDENCIA CLAVE</div>
        <div style="color:#CBD5E1;font-size:0.75rem;margin-top:0.3rem;">PREMOTE (Nature Comms, 2020, n=409):<br>HbA1c <span style="color:#00D4AA;font-weight:700;">-1.04%</span> combinado vs -0.71% BBR sola</div>
    </div>""", unsafe_allow_html=True)

with p2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">PRODUCTO 2: Probiotico + Vitaminas</div>
        <span class="badge badge-blue">ALTO NIVEL EVIDENCIA</span>
        <br><br>
        <table class="data-table">
            <tr><td style="color:#94A3B8;">Formula</td><td>4 cepas (1.5x10<sup>10</sup> UFC) + VitD3 + Zinc</td></tr>
            <tr><td style="color:#94A3B8;">Indicacion</td><td>SII + Inmunidad + Bienestar</td></tr>
            <tr><td style="color:#94A3B8;">Forma</td><td>Capsula DRcaps (lib. retardada)</td></tr>
            <tr><td style="color:#94A3B8;">Precio</td><td><span style="color:#3B82F6;font-weight:700;">$18-28 USD/mes</span></td></tr>
            <tr><td style="color:#94A3B8;">Mercados</td><td>MX, LATAM, USA</td></tr>
        </table>
        <br>
        <div style="color:#94A3B8;font-size:0.7rem;">SINERGIA TRIPLE</div>
        <div style="color:#CBD5E1;font-size:0.75rem;margin-top:0.3rem;">VitD+Prob: PCR <span style="color:#3B82F6;font-weight:700;">-1.28 mg/L</span><br>Zinc+LGG: Restaura barrera intestinal<br>En SII: Mejora IBS-SSS a 12 semanas</div>
    </div>""", unsafe_allow_html=True)

with p3:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">PRODUCTO 3: Gomita Probiotica</div>
        <span class="badge badge-purple">LIFESTYLE / ACCESIBLE</span>
        <br><br>
        <table class="data-table">
            <tr><td style="color:#94A3B8;">Formula</td><td>B. coagulans GBI-30 (2x10<sup>9</sup> UFC)</td></tr>
            <tr><td style="color:#94A3B8;">Indicacion</td><td>Salud digestiva general</td></tr>
            <tr><td style="color:#94A3B8;">Forma</td><td>Gomita (gummy)</td></tr>
            <tr><td style="color:#94A3B8;">Precio</td><td><span style="color:#8B5CF6;font-weight:700;">$12-18 USD/mes</span></td></tr>
            <tr><td style="color:#94A3B8;">Mercados</td><td>USA, MX</td></tr>
        </table>
        <br>
        <div style="color:#94A3B8;font-size:0.7rem;">VENTAJA CLAVE</div>
        <div style="color:#CBD5E1;font-size:0.75rem;margin-top:0.3rem;">Cepa esporulada termoestable<br>Mayor crecimiento en formato gummy USA<br>Gap en farmacia LATAM</div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# EVIDENCIA CIENTIFICA + SINERGIA
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header"><h3>🔬 EVIDENCIA CIENTIFICA — CEPAS NIVEL 1</h3></div>
""", unsafe_allow_html=True)

st.markdown("""
<table class="data-table">
    <thead>
        <tr>
            <th>Cepa</th>
            <th>Indicacion</th>
            <th>Dosis UFC/dia</th>
            <th>Nivel</th>
            <th>Efecto demostrado</th>
            <th>Ref. clave</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="color:#00D4AA;font-weight:600;">B. longum 35624</td>
            <td>SII (todos)</td>
            <td>1 x 10<sup>9</sup></td>
            <td><span class="badge badge-green">Nivel 1</span></td>
            <td>Reduce IL-6, TNF-alfa, CRP. Gold standard SII</td>
            <td>Whorwell 2006</td>
        </tr>
        <tr>
            <td style="color:#00D4AA;font-weight:600;">L. plantarum 299v</td>
            <td>SII-D, SII-M</td>
            <td>1 x 10<sup>10</sup></td>
            <td><span class="badge badge-green">Nivel 1</span></td>
            <td>71% vs 11% placebo. FBG -12 mg/dL</td>
            <td>Ducrotte 2012</td>
        </tr>
        <tr>
            <td style="color:#00D4AA;font-weight:600;">L. rhamnosus GG</td>
            <td>SII-D + Metabolismo</td>
            <td>1-2 x 10<sup>10</sup></td>
            <td><span class="badge badge-green">Nivel 1</span></td>
            <td>HOMA-IR -15%. Restaura barrera intestinal</td>
            <td>Tonucci 2017</td>
        </tr>
        <tr>
            <td style="color:#00D4AA;font-weight:600;">B. lactis HN019</td>
            <td>Estrenimiento</td>
            <td>1.8 x 10<sup>10</sup></td>
            <td><span class="badge badge-green">Nivel 1</span></td>
            <td>Transito colonico -31 horas</td>
            <td>Waller 2011</td>
        </tr>
        <tr>
            <td style="color:#00D4AA;font-weight:600;">B. lactis BB-12</td>
            <td>Estrenimiento + DM2</td>
            <td>1-10 x 10<sup>9</sup></td>
            <td><span class="badge badge-green">Nivel 1</span></td>
            <td>HbA1c -0.29%. Mejora consistencia heces</td>
            <td>Ejtahed 2012</td>
        </tr>
        <tr>
            <td style="color:#00D4AA;font-weight:600;">L. acidophilus La-5</td>
            <td>DM2</td>
            <td>5 x 10<sup>9</sup></td>
            <td><span class="badge badge-green">Nivel 1</span></td>
            <td>HbA1c -0.53%. Convierte BBR en dhBBR (5x)</td>
            <td>Ejtahed 2012</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# MECANISMO DE SINERGIA BBR + PROBIOTICO
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header"><h3>⚡ MECANISMO DE SINERGIA — Berberina + Probiotico (5 Niveles)</h3></div>
""", unsafe_allow_html=True)

s1, s2 = st.columns(2)

with s1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Niveles de Sinergia</div>
        <div class="bar-row">
            <div class="bar-label">1. Farmacocinetico</div>
            <div class="bar-track"><div class="bar-fill" style="width:95%;background:linear-gradient(90deg,#00D4AA,#00B4D8);">5x biodisponibilidad</div></div>
        </div>
        <div class="bar-row">
            <div class="bar-label">2. AGCC / GLP-1</div>
            <div class="bar-track"><div class="bar-fill" style="width:85%;background:linear-gradient(90deg,#3B82F6,#8B5CF6);">Estimula insulina</div></div>
        </div>
        <div class="bar-row">
            <div class="bar-label">3. Barrera intestinal</div>
            <div class="bar-track"><div class="bar-fill" style="width:80%;background:linear-gradient(90deg,#10B981,#059669);">Reduce endotoxemia</div></div>
        </div>
        <div class="bar-row">
            <div class="bar-label">4. Eje intestino-higado</div>
            <div class="bar-track"><div class="bar-fill" style="width:75%;background:linear-gradient(90deg,#F59E0B,#EF4444);">Metabolismo hepatico</div></div>
        </div>
        <div class="bar-row">
            <div class="bar-label">5. Inmunomodulacion</div>
            <div class="bar-track"><div class="bar-fill" style="width:70%;background:linear-gradient(90deg,#8B5CF6,#EC4899);">Reduce inflamacion</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Resultados Estudio PREMOTE (n=409)</div>
        <table class="data-table">
            <thead>
                <tr><th>Variable</th><th>BBR sola</th><th>Prob solo</th><th>BBR + Prob</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td>Reduccion HbA1c</td>
                    <td>-0.71%</td>
                    <td>-0.42%</td>
                    <td style="color:#00D4AA;font-weight:700;">-1.04%</td>
                </tr>
                <tr>
                    <td>Reduccion FBG</td>
                    <td>-0.99 mmol/L</td>
                    <td>-0.58 mmol/L</td>
                    <td style="color:#00D4AA;font-weight:700;">-1.49 mmol/L</td>
                </tr>
                <tr>
                    <td>Bifidobacterium</td>
                    <td><span class="badge badge-red">Deplecion</span></td>
                    <td><span class="badge badge-blue">Aumento</span></td>
                    <td><span class="badge badge-green">Restauracion</span></td>
                </tr>
            </tbody>
        </table>
        <div style="color:#64748B;font-size:0.7rem;margin-top:0.8rem;">Zhang Y et al. Nature Communications. 2020;11:5015. RCT multicentrico, DM2 recien diagnosticada. p&lt;0.05 para todas las variables.</div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# ANALISIS COMPETITIVO
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header"><h3>📊 ANALISIS COMPETITIVO</h3></div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Competidores USA — Precio USD/mes</div>
        <div class="bar-row">
            <div class="bar-label">Seed</div>
            <div class="bar-track"><div class="bar-fill" style="width:100%;background:linear-gradient(90deg,#8B5CF6,#EC4899);">$49.99</div></div>
        </div>
        <div class="bar-row">
            <div class="bar-label">Align</div>
            <div class="bar-track"><div class="bar-fill" style="width:72%;background:linear-gradient(90deg,#3B82F6,#6366F1);">$25-45</div></div>
        </div>
        <div class="bar-row">
            <div class="bar-label">Culturelle</div>
            <div class="bar-track"><div class="bar-fill" style="width:50%;background:linear-gradient(90deg,#00D4AA,#00B4D8);">$18-30</div></div>
        </div>
        <div class="bar-row">
            <div class="bar-label">Florastor</div>
            <div class="bar-track"><div class="bar-fill" style="width:48%;background:linear-gradient(90deg,#10B981,#059669);">$20-28</div></div>
        </div>
        <div class="bar-row">
            <div class="bar-label" style="color:#00D4AA;font-weight:700;">Genomma (P1)</div>
            <div class="bar-track"><div class="bar-fill" style="width:42%;background:linear-gradient(90deg,#F59E0B,#EF4444);">$15-25</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Competidores Mexico</div>
        <table class="data-table">
            <thead><tr><th>Marca</th><th>Cepa</th><th>Posicionamiento</th></tr></thead>
            <tbody>
                <tr><td style="font-weight:600;">Floratil</td><td>S. boulardii</td><td>Lider farmacia, diarrea</td></tr>
                <tr><td style="font-weight:600;">Enterogermina</td><td>B. clausii</td><td>Pediatria, Sanofi</td></tr>
                <tr><td style="font-weight:600;">BioGaia</td><td>L. reuteri</td><td>Pediatria premium</td></tr>
                <tr><td style="font-weight:600;">Yakult</td><td>L. casei Shirota</td><td>Masivo, bebida</td></tr>
            </tbody>
        </table>
        <br>
        <div class="opp-box">
            <div class="opp-title">GAP IDENTIFICADO</div>
            <div class="opp-text">Mercado MX anclado en "probiotico = diarrea". Indicaciones metabolicas (glucosa, peso, colesterol) y bienestar integral estan VACIAS. Nadie tiene probiotico + berberina.</div>
        </div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# REGULACION
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header"><h3>📋 MARCO REGULATORIO</h3></div>
""", unsafe_allow_html=True)

st.markdown("""
<table class="data-table">
    <thead>
        <tr><th>Criterio</th><th>Mexico (COFEPRIS)</th><th>USA (FDA)</th><th>Brasil (ANVISA)</th><th>LATAM Promedio</th></tr>
    </thead>
    <tbody>
        <tr>
            <td>Clasificacion</td>
            <td>Suplemento alimenticio</td>
            <td>Dietary supplement</td>
            <td>Suplemento alimentar</td>
            <td>Suplemento dietario</td>
        </tr>
        <tr>
            <td>Tiempo registro</td>
            <td><span class="badge badge-green">2-4 meses</span></td>
            <td><span class="badge badge-blue">3-6 meses</span></td>
            <td><span class="badge badge-red">8-18 meses</span></td>
            <td><span class="badge badge-amber">3-18 meses</span></td>
        </tr>
        <tr>
            <td>Costo estimado</td>
            <td>$5-15K USD</td>
            <td>$20-50K USD</td>
            <td>$15-40K USD</td>
            <td>$5-40K USD</td>
        </tr>
        <tr>
            <td>Berberina</td>
            <td><span class="badge badge-amber">ZONA GRIS</span></td>
            <td><span class="badge badge-green">PERMITIDA</span></td>
            <td><span class="badge badge-amber">CONSULTAR</span></td>
            <td><span class="badge badge-amber">VARIA</span></td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

st.markdown("""
<div class="alert-box">
    <div class="alert-title">⚠️ ALERTA REGULATORIA: BERBERINA EN MEXICO</div>
    <div class="alert-text">COFEPRIS puede considerar la berberina como ingrediente farmacologicamente activo. Se requiere opinion tecnica previa antes de incluirla en suplemento alimenticio. En USA no hay problema (historial pre-DSHEA 1994).</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PROVEEDORES + TIMELINE
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header"><h3>🏭 PROVEEDORES CLAVE & TIMELINE DE LANZAMIENTO</h3></div>
""", unsafe_allow_html=True)

t1, t2 = st.columns(2)

with t1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Proveedores Principales</div>
        <table class="data-table">
            <thead><tr><th>Categoria</th><th>Proveedor</th><th>Origen</th><th>Especialidad</th></tr></thead>
            <tbody>
                <tr>
                    <td style="color:#00D4AA;">Cepas</td>
                    <td style="font-weight:600;">Novonesis (#1)</td>
                    <td>Dinamarca</td>
                    <td>BB-12, HN019, La-5</td>
                </tr>
                <tr>
                    <td style="color:#00D4AA;">Cepas</td>
                    <td style="font-weight:600;">IFF (#2)</td>
                    <td>USA</td>
                    <td>LGG, NCFM</td>
                </tr>
                <tr>
                    <td style="color:#00D4AA;">Cepas</td>
                    <td style="font-weight:600;">Probi</td>
                    <td>Suecia</td>
                    <td>L. plantarum 299v</td>
                </tr>
                <tr>
                    <td style="color:#F59E0B;">Berberina</td>
                    <td style="font-weight:600;">Sabinsa</td>
                    <td>India/USA</td>
                    <td>Phytosome (mayor biodis.)</td>
                </tr>
                <tr>
                    <td style="color:#8B5CF6;">CMO Mexico</td>
                    <td style="font-weight:600;">Liomont / Medix</td>
                    <td>Mexico</td>
                    <td>Manufactura local</td>
                </tr>
                <tr>
                    <td style="color:#8B5CF6;">CMO USA</td>
                    <td style="font-weight:600;">Catalent / Best Form.</td>
                    <td>USA</td>
                    <td>Capsulas, sachets</td>
                </tr>
            </tbody>
        </table>
    </div>""", unsafe_allow_html=True)

with t2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Timeline de Lanzamiento Escalonado</div>
        <br>
        <div class="timeline-item">
            <div class="timeline-phase">Fase 1</div>
            <div>
                <div class="timeline-content"><strong>USA + Mexico</strong> — Meses 1-6</div>
                <div class="timeline-markets">Dietary supplement (FDA) + Suplemento alimenticio (COFEPRIS)</div>
                <div class="progress-container" style="width:200px;margin-top:0.4rem;"><div class="progress-bar" style="width:100%;"></div></div>
            </div>
        </div>
        <div class="timeline-item">
            <div class="timeline-phase">Fase 2</div>
            <div>
                <div class="timeline-content"><strong>Peru, Chile, Colombia</strong> — Meses 4-12</div>
                <div class="timeline-markets">Suplemento dietario (DIGEMID, ISP, INVIMA)</div>
                <div class="progress-container" style="width:200px;margin-top:0.4rem;"><div class="progress-bar" style="width:60%;"></div></div>
            </div>
        </div>
        <div class="timeline-item">
            <div class="timeline-phase">Fase 3</div>
            <div>
                <div class="timeline-content"><strong>Argentina, Brasil</strong> — Meses 8-18</div>
                <div class="timeline-markets">ANMAT + ANVISA (mas exigente)</div>
                <div class="progress-container" style="width:200px;margin-top:0.4rem;"><div class="progress-bar" style="width:30%;"></div></div>
            </div>
        </div>
        <br>
        <div class="opp-box">
            <div class="opp-title">FORMAS FARMACEUTICAS</div>
            <div class="opp-text">
                <strong>TOP 1:</strong> DRcaps (supervivencia 80-90%)<br>
                <strong>TOP 2:</strong> Sachet monodosis (estable, aceptado LATAM)<br>
                <strong>TOP 3:</strong> Gomita esporulada (mayor crecimiento USA)<br>
                <span style="color:#EF4444;font-weight:600;">⚠️ BBR es antimicrobiana — requiere separacion fisica del probiotico</span>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# OPORTUNIDADES ESTRATEGICAS
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header"><h3>🎯 OPORTUNIDADES ESTRATEGICAS</h3></div>
""", unsafe_allow_html=True)

o1, o2, o3 = st.columns(3)

with o1:
    st.markdown("""
    <div class="opp-box">
        <div class="opp-title">🥇 OPORTUNIDAD #1</div>
        <div class="opp-text">Probiotico + Berberina es un espacio VACIO a nivel global. No existe producto combinado comercial. First-mover advantage para Genomma Lab con respaldo de Nature Communications.</div>
    </div>""", unsafe_allow_html=True)

with o2:
    st.markdown("""
    <div class="opp-box">
        <div class="opp-title">🥈 OPORTUNIDAD #2</div>
        <div class="opp-text">Mercado MX/LATAM anclado en "probiotico = diarrea". Las indicaciones metabolicas (glucosa, peso, colesterol) y bienestar integral estan practicamente vacias. Espacio azul para posicionar.</div>
    </div>""", unsafe_allow_html=True)

with o3:
    st.markdown("""
    <div class="opp-box">
        <div class="opp-title">🥉 OPORTUNIDAD #3</div>
        <div class="opp-text">Gomitas probioticas en farmacia LATAM estan vacias. B. coagulans (termoestable) permite formato gummy sin cadena de frio. Precio accesible $12-18 USD/mes para captura masiva.</div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:1.5rem;border-top:1px solid rgba(255,255,255,0.05);">
    <div style="color:#64748B;font-size:0.7rem;">GENOMMA LAB INTERNACIONAL | AGENTE PROBIOTICOS | CONFIDENCIAL</div>
    <div style="color:#475569;font-size:0.65rem;margin-top:0.3rem;">Dashboard generado automaticamente a partir del Reporte Estrategico | Marzo 2026</div>
</div>
""", unsafe_allow_html=True)
