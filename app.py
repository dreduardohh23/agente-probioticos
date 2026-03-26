"""
AGENTE PROBIOTICOS - Web Application
Genomma Lab | Celula de Innovacion en Probioticos
"""

import streamlit as st
import anthropic
import json
import os
import tempfile
from datetime import datetime

# ── Page config ──
st.set_page_config(
    page_title="Agente Probioticos | Genomma Lab",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1B3A5C 0%, #2E5E8E 50%, #3A7CA5 100%);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 { color: white; margin: 0; font-size: 1.8rem; }
    .main-header p { color: #B8D4E8; margin: 0.3rem 0 0 0; font-size: 0.95rem; }
    .status-badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-active { background: #10B981; color: white; }
    .badge-search { background: #F59E0B; color: white; }
    .stChatMessage { border-radius: 10px; }
    .sidebar-section {
        background: #F0F4F8;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    div[data-testid="stSidebarContent"] { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# ── System prompt with all agent knowledge ──
SYSTEM_PROMPT = """Eres el AGENTE PROBIOTICOS de Genomma Lab, una celula de trabajo dedicada al desarrollo e innovacion en la categoria de probioticos.

## Tu Proposito
Definir posicionamiento y portafolio de probioticos diferenciados, con formulas innovadoras y validacion con consumidor, para los mercados de Mexico, LATAM y USA.

## Conocimiento Base del Agente

### PRODUCTO 1: PROBIOTICO + BERBERINA (First-to-Market Global)
- Formula: 6 cepas (~3.3x10^10 UFC) + Berberina HCl 1000mg/dia
- Cepas: B. longum 35624 (1x10^9), B. lactis HN019 (1x10^10), L. acidophilus La-5/NCFM (5x10^9), L. plantarum 299v (1x10^10), L. rhamnosus GG (1x10^10), B. lactis BB-12 (1x10^9)
- Indicacion: SII + DM2 + Resistencia a insulina
- Estudio PREMOTE (Zhang Y et al., Nature Communications, 2020, n=409): BBR+Probiotico redujo HbA1c -1.04% vs -0.71% BBR sola
- 5 niveles de sinergia: farmacocinetico (dhBBR 5x biodisponibilidad), AGCC/GLP-1, barrera intestinal, eje intestino-higado, inmunomodulacion
- NO existe producto combinado comercial relevante a nivel global

### PRODUCTO 2: PROBIOTICO + VITAMINAS (SII + Bienestar)
- Formula: 4 cepas (~1.5x10^10 UFC) + Vitamina D3 2000 UI + Zinc bisglicinato 15mg
- Cepas: L. rhamnosus GG (5x10^9), L. plantarum 299v (5x10^9), B. lactis BB-12 (3x10^9), B. longum 35624 (2x10^9)
- Evidencia: Costanzo 2023 meta-analisis (VitD+probioticos), Akhtar 2022 (Zinc+LGG), Laliani 2023 (VitD+probioticos en SII)
- Alternativa: Psicobioticos + Complejo B (L. helveticus R0052 + B. longum R0175 + B6/B9/B12) para eje intestino-cerebro

### PRODUCTO 3: GOMITA PROBIOTICA
- B. coagulans GanedenBC30 (2x10^9 UFC) - cepa esporulada termoestable
- Formato accesible/lifestyle

### EVIDENCIA CIENTIFICA - CEPAS NIVEL 1
SII: B. longum 35624, L. plantarum 299v, L. rhamnosus GG, VSL#3
Estrenimiento: B. lactis BB-12, B. lactis HN019, B. lactis DN-173 010
Antiinflamatorio: VSL#3 (Nivel 1 AGA), E. coli Nissle 1917, B. longum 35624
Metabolismo glucosa: L. acidophilus La-5 (HbA1c -0.53%), L. rhamnosus GG (HOMA-IR -15%), Akkermansia muciniphila (HOMA-IR -28.6%)

### REGULACION
Mexico (COFEPRIS): Suplemento alimenticio (2-4 meses, $5-15K USD). ALERTA: Berberina en zona gris.
USA (FDA): Dietary supplement DSHEA (3-6 meses, $20-50K USD). Berberina permitida.
Brasil (ANVISA): Mas exigente, 8-18 meses. Colombia (INVIMA): 6-12 meses. Argentina (ANMAT): 6-12 meses.
Estrategia: Fase 1 USA+MX, Fase 2 Peru/Chile/Colombia, Fase 3 Argentina/Brasil.

### COMPETIDORES
USA: Culturelle (LGG, $18-30), Align (B.longum 35624, $25-45), Seed ($49.99 premium), Florastor (S.boulardii)
Mexico: Floratil (lider farmacia), Enterogermina (Sanofi, pediatria), BioGaia, Yakult
GAP: Nadie tiene probiotico+berberina. Mercado MX anclado en "diarrea". Gomitas vacias en farmacia LATAM.

### PROVEEDORES
Cepas: Novonesis (#1, Dinamarca), IFF (#2, USA), Kerry (termoestables), Probi (299v), BioGaia (L.reuteri)
Berberina: Sabinsa (Phytosome, mayor biodisponibilidad), China (>90% produccion global)
CMOs Mexico: Liomont, Medix, Neolpharma. USA: Best Formulations, Catalent. LATAM: Procaps

### FORMAS FARMACEUTICAS
TOP 1: Capsula DRcaps liberacion retardada (supervivencia 80-90%, claim diferenciador)
TOP 2: Sachet monodosis (alta estabilidad, culturalmente aceptado en LATAM)
TOP 3: Gomita con esporas (B. coagulans, mayor crecimiento en USA)
ALERTA: Berberina es antimicrobiana - requiere separacion fisica del probiotico

## Instrucciones de Comportamiento
1. Responde siempre en espanol
2. Basa tus respuestas en evidencia cientifica. Cita estudios cuando sea relevante
3. Cuando busques en la web, prioriza: PubMed, ClinicalTrials.gov, sitios de COFEPRIS/FDA/ANVISA, revistas indexadas
4. Para regulacion, siempre verifica la informacion mas reciente
5. Cuando el usuario suba archivos, analizalos en contexto del proyecto de probioticos
6. Si no estas seguro de algo, indicalo y sugiere donde buscar la informacion
7. Mantente enfocado en el proyecto de Genomma Lab
8. Puedes proponer mejoras, nuevas combinaciones, o alertar sobre riesgos
"""

# ── Helper functions ──

def extract_text_from_pdf(file_bytes):
    """Extract text from PDF file."""
    try:
        from PyPDF2 import PdfReader
        import io
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages[:50]:  # Limit to 50 pages
            text += page.extract_text() or ""
        return text[:50000]  # Limit text length
    except Exception as e:
        return f"Error leyendo PDF: {str(e)}"


def extract_text_from_docx(file_bytes):
    """Extract text from DOCX file."""
    try:
        from docx import Document
        import io
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([p.text for p in doc.paragraphs])
        return text[:50000]
    except Exception as e:
        return f"Error leyendo DOCX: {str(e)}"


def extract_text_from_xlsx(file_bytes):
    """Extract text from XLSX file."""
    try:
        import openpyxl
        import io
        wb = openpyxl.load_workbook(io.BytesIO(file_bytes), read_only=True)
        text = ""
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            text += f"\n=== Hoja: {sheet_name} ===\n"
            for row in ws.iter_rows(max_row=200, values_only=True):
                row_text = " | ".join([str(cell) if cell is not None else "" for cell in row])
                if row_text.strip(" |"):
                    text += row_text + "\n"
        return text[:50000]
    except Exception as e:
        return f"Error leyendo XLSX: {str(e)}"


def extract_file_content(uploaded_file):
    """Extract text content from uploaded file."""
    file_bytes = uploaded_file.read()
    name = uploaded_file.name.lower()

    if name.endswith('.pdf'):
        return extract_text_from_pdf(file_bytes)
    elif name.endswith('.docx'):
        return extract_text_from_docx(file_bytes)
    elif name.endswith(('.xlsx', '.xls')):
        return extract_text_from_xlsx(file_bytes)
    elif name.endswith(('.txt', '.md', '.csv', '.json')):
        return file_bytes.decode('utf-8', errors='ignore')[:50000]
    else:
        return f"Formato no soportado: {name}. Soportados: PDF, DOCX, XLSX, TXT, MD, CSV, JSON"


def search_web(query, max_results=5):
    """Search the web using DuckDuckGo."""
    try:
        from duckduckgo_search import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
        return results
    except Exception as e:
        return [{"title": "Error en busqueda", "url": "", "snippet": str(e)}]


def search_pubmed(query, max_results=5):
    """Search PubMed for scientific articles."""
    try:
        import requests
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        # Search
        search_url = f"{base_url}/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "sort": "relevance"
        }
        resp = requests.get(search_url, params=params, timeout=10)
        data = resp.json()
        ids = data.get("esearchresult", {}).get("idlist", [])

        if not ids:
            return []

        # Fetch details
        fetch_url = f"{base_url}/esummary.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "json"
        }
        resp = requests.get(fetch_url, params=fetch_params, timeout=10)
        fetch_data = resp.json()

        results = []
        for uid in ids:
            article = fetch_data.get("result", {}).get(uid, {})
            if article:
                authors = ", ".join([a.get("name", "") for a in article.get("authors", [])[:3]])
                results.append({
                    "title": article.get("title", "Sin titulo"),
                    "authors": authors,
                    "journal": article.get("source", ""),
                    "year": article.get("pubdate", "")[:4],
                    "pmid": uid,
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/"
                })
        return results
    except Exception as e:
        return [{"title": f"Error buscando PubMed: {str(e)}", "authors": "", "journal": "", "year": "", "pmid": "", "url": ""}]


def fetch_webpage(url):
    """Fetch and extract text from a webpage."""
    try:
        import requests
        from bs4 import BeautifulSoup
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Remove scripts and styles
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        text = soup.get_text(separator='\n', strip=True)
        return text[:30000]
    except Exception as e:
        return f"Error accediendo a {url}: {str(e)}"


def process_tool_call(tool_name, tool_input):
    """Process tool calls from Claude."""
    if tool_name == "web_search":
        results = search_web(tool_input.get("query", ""), tool_input.get("max_results", 5))
        return json.dumps(results, ensure_ascii=False)
    elif tool_name == "pubmed_search":
        results = search_pubmed(tool_input.get("query", ""), tool_input.get("max_results", 5))
        return json.dumps(results, ensure_ascii=False)
    elif tool_name == "fetch_url":
        text = fetch_webpage(tool_input.get("url", ""))
        return text
    return "Herramienta no reconocida"


# ── Tool definitions for Claude ──
TOOLS = [
    {
        "name": "web_search",
        "description": "Busca informacion en la web. Usa para buscar regulaciones, competidores, proveedores, noticias del mercado de probioticos, informacion de COFEPRIS, FDA, ANVISA, etc.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termino de busqueda. Ejemplo: 'COFEPRIS regulacion suplementos alimenticios probioticos 2025'"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Numero maximo de resultados (default 5)",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "pubmed_search",
        "description": "Busca articulos cientificos en PubMed/NCBI. Usa para encontrar estudios clinicos, meta-analisis, revisiones sistematicas sobre probioticos, berberina, vitaminas, etc.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termino de busqueda PubMed. Ejemplo: 'berberine probiotics type 2 diabetes randomized controlled trial'"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Numero maximo de resultados (default 5)",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "fetch_url",
        "description": "Accede a una pagina web y extrae su contenido. Usa para leer paginas de regulaciones, articulos completos, sitios de proveedores, etc.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL completa de la pagina a leer"
                }
            },
            "required": ["url"]
        }
    }
]


def get_ai_response(messages, api_key, modelo="claude-3-5-sonnet-20241022"):
    """Get response from Claude with tool use support."""
    client = anthropic.Anthropic(api_key=api_key)

    # Initial call
    response = client.messages.create(
        model=modelo,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        tools=TOOLS,
        messages=messages
    )

    # Handle tool use loop
    max_iterations = 5
    iteration = 0

    while response.stop_reason == "tool_use" and iteration < max_iterations:
        iteration += 1
        tool_results = []

        for block in response.content:
            if block.type == "tool_use":
                with st.status(f"🔍 Usando herramienta: **{block.name}**", expanded=True) as status:
                    if block.name == "web_search":
                        st.write(f"Buscando: *{block.input.get('query', '')}*")
                    elif block.name == "pubmed_search":
                        st.write(f"Buscando en PubMed: *{block.input.get('query', '')}*")
                    elif block.name == "fetch_url":
                        st.write(f"Accediendo: *{block.input.get('url', '')}*")

                    result = process_tool_call(block.name, block.input)

                    if block.name in ["web_search", "pubmed_search"]:
                        try:
                            parsed = json.loads(result)
                            for r in parsed[:3]:
                                title = r.get('title', '')
                                url = r.get('url', r.get('pmid', ''))
                                st.write(f"  - {title}")
                        except:
                            pass

                    status.update(label=f"✅ {block.name} completado", state="complete")

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        # Continue conversation with tool results
        messages = messages + [
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": tool_results}
        ]

        response = client.messages.create(
            model=modelo,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )

    # Extract final text
    final_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            final_text += block.text

    return final_text


# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚙️ Configuracion")

    # API Key
    api_key_raw = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Obtener en console.anthropic.com"
    )
    api_key = api_key_raw.strip() if api_key_raw else ""

    # Model selector
    modelo = st.selectbox(
        "Modelo Claude",
        ["claude-3-5-sonnet-20241022", "claude-sonnet-4-20250514", "claude-3-haiku-20240307"],
        index=0,
        help="Si un modelo da error, prueba otro"
    )

    if api_key:
        if st.button("🔌 Probar conexion"):
            try:
                test_client = anthropic.Anthropic(api_key=api_key)
                test_resp = test_client.messages.create(
                    model=modelo,
                    max_tokens=50,
                    messages=[{"role": "user", "content": "Di solo: Conexion exitosa"}]
                )
                st.success(f"✅ Conexion OK con {modelo}")
            except anthropic.AuthenticationError:
                st.error("❌ API Key invalida. Revisa que la copiaste completa desde console.anthropic.com")
            except anthropic.PermissionDeniedError:
                st.error("❌ Tu plan no tiene acceso a este modelo. Prueba otro modelo del selector.")
            except anthropic.NotFoundError:
                st.error("❌ Modelo no disponible. Selecciona otro modelo.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        st.success("✅ API Key configurada")
    else:
        st.warning("⚠️ Ingresa tu API Key para comenzar")

    st.markdown("---")

    # Report download
    st.markdown("### 📄 Reporte Estrategico")
    report_path = os.path.join(os.path.dirname(__file__), "Agente_Probioticos_Reporte_Estrategico.docx")
    if os.path.exists(report_path):
        with open(report_path, "rb") as f:
            st.download_button(
                label="⬇️ Descargar Reporte (.docx)",
                data=f.read(),
                file_name="Agente_Probioticos_Reporte_Estrategico.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        st.caption("Reporte compilado con toda la investigacion")
    else:
        st.info("Reporte no disponible")

    st.markdown("---")

    # File upload
    st.markdown("### 📎 Subir Archivos")
    uploaded_files = st.file_uploader(
        "Arrastra archivos aqui",
        accept_multiple_files=True,
        type=["pdf", "docx", "xlsx", "xls", "txt", "md", "csv", "json"],
        help="Soporta: PDF, DOCX, XLSX, TXT, MD, CSV, JSON"
    )

    if uploaded_files:
        st.markdown(f"**{len(uploaded_files)} archivo(s) cargado(s):**")
        for f in uploaded_files:
            size_kb = f.size / 1024
            st.markdown(f"- 📄 {f.name} ({size_kb:.0f} KB)")

    st.markdown("---")

    # Quick actions
    st.markdown("### 🚀 Acciones Rapidas")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔬 PubMed", use_container_width=True, help="Buscar en PubMed"):
            st.session_state.quick_action = "pubmed"
        if st.button("📋 Regulacion", use_container_width=True, help="Consultar regulacion"):
            st.session_state.quick_action = "regulacion"
    with col2:
        if st.button("🏭 Proveedores", use_container_width=True, help="Buscar proveedores"):
            st.session_state.quick_action = "proveedores"
        if st.button("📊 Competencia", use_container_width=True, help="Analizar competencia"):
            st.session_state.quick_action = "competencia"

    st.markdown("---")

    # Knowledge base summary
    with st.expander("📚 Base de Conocimiento", expanded=False):
        st.markdown("""
        **Productos definidos:**
        - P1: Probiotico + Berberina
        - P2: Probiotico + VitD + Zinc
        - P3: Gomita B. coagulans

        **Cepas clave:** B. longum 35624, L. plantarum 299v, L. rhamnosus GG, B. lactis HN019/BB-12

        **Mercados:** MX, LATAM, USA

        **Competidores:** Floratil, Enterogermina, Culturelle, Align, Seed
        """)

    # Clear chat
    st.markdown("---")
    if st.button("🗑️ Limpiar conversacion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ═══════════════════════════════════════════════════════════
# MAIN AREA
# ═══════════════════════════════════════════════════════════

# Header
st.markdown("""
<div class="main-header">
    <h1>🧬 Agente Probioticos</h1>
    <p>Celula de Innovacion | Genomma Lab | Desarrollo de Portafolio de Probioticos</p>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "file_contexts" not in st.session_state:
    st.session_state.file_contexts = {}

# Process uploaded files
if uploaded_files:
    for f in uploaded_files:
        if f.name not in st.session_state.file_contexts:
            with st.spinner(f"Procesando {f.name}..."):
                content = extract_file_content(f)
                st.session_state.file_contexts[f.name] = content

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["display_content"] if "display_content" in msg else msg["content"])
    else:
        with st.chat_message("assistant", avatar="🧬"):
            st.markdown(msg["content"])

# Handle quick actions
quick_prompts = {
    "pubmed": "Busca en PubMed los estudios mas recientes (2024-2026) sobre la combinacion de probioticos con berberina para diabetes tipo 2. Dame un resumen de los hallazgos mas relevantes.",
    "regulacion": "Busca la regulacion mas actualizada de COFEPRIS para suplementos alimenticios con probioticos en Mexico. Verifica si hay actualizaciones recientes sobre berberina.",
    "proveedores": "Busca proveedores actualizados de cepas probioticas (Novonesis, IFF, Kerry) y sus ultimas innovaciones en cepas para salud metabolica.",
    "competencia": "Busca los lanzamientos mas recientes de productos probioticos en Mexico y USA. Analiza las tendencias actuales del mercado."
}

if "quick_action" in st.session_state:
    action = st.session_state.quick_action
    if action in quick_prompts:
        prompt = quick_prompts[action]
        del st.session_state.quick_action
        st.session_state.pending_prompt = prompt
        st.rerun()

# Chat input
if prompt := st.chat_input("Pregunta al Agente Probioticos...") or st.session_state.get("pending_prompt"):
    if "pending_prompt" in st.session_state:
        prompt = st.session_state.pending_prompt
        del st.session_state.pending_prompt

    if not api_key:
        st.error("⚠️ Por favor ingresa tu Anthropic API Key en la barra lateral para comenzar.")
        st.stop()

    # Build user message with file context if any
    full_content = prompt
    display_content = prompt

    # Add file contexts if files are uploaded and this is the first message or files are new
    if st.session_state.file_contexts:
        file_context = "\n\n--- ARCHIVOS ADJUNTOS ---\n"
        for fname, content in st.session_state.file_contexts.items():
            file_context += f"\n### Archivo: {fname}\n{content[:15000]}\n"
        full_content = prompt + file_context
        display_content = prompt + f"\n\n📎 *{len(st.session_state.file_contexts)} archivo(s) adjunto(s)*"

    # Display user message
    with st.chat_message("user"):
        st.markdown(display_content)

    # Add to history
    st.session_state.messages.append({
        "role": "user",
        "content": full_content,
        "display_content": display_content
    })

    # Build messages for API (only send text content)
    api_messages = []
    for msg in st.session_state.messages:
        if isinstance(msg["content"], str):
            api_messages.append({"role": msg["role"], "content": msg["content"]})

    # Get AI response
    with st.chat_message("assistant", avatar="🧬"):
        with st.spinner("Pensando..."):
            try:
                response = get_ai_response(api_messages, api_key, modelo)
                st.markdown(response)

                # Add to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
            except anthropic.AuthenticationError as e:
                st.error(f"❌ API Key invalida. Verifica tu clave en console.anthropic.com\n\nDetalle: {str(e)}")
            except anthropic.PermissionDeniedError as e:
                st.error(f"❌ Permiso denegado. Tu API Key puede no tener acceso al modelo. Detalle: {str(e)}")
            except anthropic.NotFoundError as e:
                st.error(f"❌ Modelo no encontrado. Detalle: {str(e)}")
            except anthropic.RateLimitError:
                st.error("⏳ Limite de velocidad alcanzado. Espera un momento e intenta de nuevo.")
            except Exception as e:
                st.error(f"❌ Error: {type(e).__name__}: {str(e)}")


# ── Welcome message if no chat history ──
if not st.session_state.messages:
    st.markdown("---")
    st.markdown("### 👋 Bienvenido al Agente Probioticos")
    st.markdown("Soy tu asistente especializado en el desarrollo del portafolio de probioticos de Genomma Lab. Puedo ayudarte con:")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        **🔬 Evidencia Cientifica**
        - Buscar en PubMed
        - Analizar estudios clinicos
        - Validar combinaciones
        """)
    with col2:
        st.markdown("""
        **📋 Regulacion**
        - COFEPRIS, FDA, ANVISA
        - Claims permitidos
        - Clasificacion de producto
        """)
    with col3:
        st.markdown("""
        **🏭 Supply Chain**
        - Proveedores de cepas
        - Fabricantes berberina
        - Contract manufacturers
        """)
    with col4:
        st.markdown("""
        **📊 Mercado**
        - Analisis competitivo
        - Precios y tendencias
        - Oportunidades
        """)

    st.markdown("---")
    st.markdown("**Ejemplos de preguntas:**")
    examples = [
        "Busca los ultimos estudios sobre Lactobacillus plantarum 299v y sindrome de intestino irritable",
        "Cual es la regulacion actual de COFEPRIS para berberina en suplementos?",
        "Compara los precios de los principales probioticos en farmacias de Mexico",
        "Busca proveedores de Bacillus coagulans GanedenBC30 con capacidad de suministro a Mexico",
        "Que formas farmaceuticas innovadoras estan usando las marcas lideres de probioticos?",
    ]
    for ex in examples:
        st.markdown(f"- *{ex}*")
