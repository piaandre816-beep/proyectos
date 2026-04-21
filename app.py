import streamlit as st
import pandas as pd
import plotly.express as px
import kagglehub
import os

st.set_page_config(page_title="EduAI Dashboard", page_icon="🏫", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
<style>
/* Background */
[data-testid="stAppViewContainer"] {
    background-color: #0f172a;
}
[data-testid="stSidebar"] {
    background-color: #1e293b;
}

/* Cards for metrics */
div[data-testid="metric-container"] {
    background-color: #1e293b;
    border: 1px solid rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
    color: white;
}
/* Titles */
h1, h2, h3, p, span, label {
    color: #f8fafc !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Descarga de datos dinámicos usando Kagglehub y devuelve el DataFrame procesado."""
    dataset_id = "visionlangai/ai-tools-usage-analysis-in-education"
    try:
        path = kagglehub.dataset_download(dataset_id)
        archivos = os.listdir(path)
        csv_file = [f for f in archivos if f.endswith('.csv')][0]
        csv_path = os.path.join(path, csv_file)
        
        df = pd.read_csv(csv_path)
        # Limpieza básica: quitar espacios en nombres de columna
        df.columns = [col.strip() for col in df.columns]
        return df
    except Exception as e:
        st.error(f"Error cargando los datos desde Kaggle: {e}")
        return pd.DataFrame()

# Título y Cabecera
st.title("🎓 Análisis de Uso de Herramientas de IA en Educación")
st.markdown("Explora de forma interactiva el impacto de la inteligencia artificial basado en el dataset de Kaggle `visionlangai`.")

df = load_data()

if df.empty:
    st.warning("No se encontraron datos o aún están descargándose.")
    st.stop()

columnas_reales = list(df.columns)

st.sidebar.header("🔍 Opciones de Filtro")

# Buscar columnas comunes
def find_column(keywords, columns):
    for k in keywords:
        for c in columns:
            if k.lower() in c.lower():
                return c
    return None

col_gender = find_column(["gender", "sexo"], columnas_reales)
col_role = find_column(["role", "profession", "occupation", "estudiante"], columnas_reales)
col_tool = find_column(["tool", "herramienta", "platform", "ai_tool"], columnas_reales)

filtered_df = df.copy()

if col_gender:
    sexos = df[col_gender].dropna().unique().tolist()
    seleccion = st.sidebar.multiselect("Filtrar por Género", sexos, default=sexos)
    if seleccion:
        filtered_df = filtered_df[filtered_df[col_gender].isin(seleccion)]

if col_role:
    roles = df[col_role].dropna().unique().tolist()
    seleccion_roles = st.sidebar.multiselect("Filtrar por Rol", roles, default=roles)
    if seleccion_roles:
        filtered_df = filtered_df[filtered_df[col_role].isin(seleccion_roles)]

if col_tool:
    tools = df[col_tool].dropna().unique().tolist()
    top_tools = df[col_tool].value_counts().head(10).index.tolist()
    seleccion_tools = st.sidebar.multiselect("Filtrar por Herramienta IA", top_tools, default=top_tools)
    if seleccion_tools:
        filtered_df = filtered_df[filtered_df[col_tool].isin(seleccion_tools)]

# --- SECTION: KPIs (TARJETAS) ---
st.markdown("### 📊 Indicadores Clave (KPIs)")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric("Total de Registros", f"{len(filtered_df):,}")
    
with kpi2:
    if col_tool:
        herramientas_unicas = filtered_df[col_tool].nunique()
        st.metric("Herramientas Diferentes", f"{herramientas_unicas}")
    else:
        st.metric("Columnas Disponibles", f"{len(columnas_reales)}")

with kpi3:
    if col_role:
        roles_unicos = filtered_df[col_role].nunique()
        st.metric("Tipos de Roles", f"{roles_unicos}")
    else:
        st.metric("Datos Faltantes (NA)", f"{filtered_df.isna().sum().sum()}")

st.markdown("---")

# --- SECTION: GRAFICOS ---
st.markdown("### 📈 Visualizaciones Interactivas")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if col_tool:
        st.subheader("Top Herramientas IA")
        df_tool_counts = filtered_df[col_tool].value_counts().reset_index()
        df_tool_counts.columns = [col_tool, 'Count']
        fig1 = px.bar(
            df_tool_counts.head(10), 
            x='Count', 
            y=col_tool, 
            orientation='h', 
            color='Count',
            color_continuous_scale="Purples"
        )
        fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig1, use_container_width=True)
    elif col_role:
        st.subheader("Distribución de Roles")
        df_role_counts = filtered_df[col_role].value_counts().reset_index()
        df_role_counts.columns = [col_role, 'Count']
        fig1 = px.pie(df_role_counts.head(10), names=col_role, values='Count', color_discrete_sequence=px.colors.sequential.Purp)
        fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    if col_role and col_gender:
        st.subheader("Distribución de Género por Rol")
        df_grouped = filtered_df.groupby([col_role, col_gender]).size().reset_index(name='Count')
        fig2 = px.bar(
            df_grouped, 
            x=col_role, 
            y='Count', 
            color=col_gender, 
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig2, use_container_width=True)
    elif col_gender:
        st.subheader("Distribución de Género")
        df_gender_counts = filtered_df[col_gender].value_counts().reset_index()
        df_gender_counts.columns = [col_gender, 'Count']
        fig2 = px.pie(df_gender_counts, names=col_gender, values='Count', hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
        fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sin columnas demográficas para este gráfico.")

st.markdown("---")
with st.expander("📌 Expandir para ver la tabla estática de datos"):
    st.dataframe(filtered_df, use_container_width=True)
