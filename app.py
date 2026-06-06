%%writefile app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Configuración de la página (Estilo Reporte Avanzado)
st.set_page_config(page_title="Informe Estadístico y Comercial", layout="wide")

st.title("📊 Informe Integral de Ventas y Rendimiento de Marketing")
st.markdown("---")

# 2. Carga de los dos DataFrames reales desde tu entorno de Colab
@st.cache_data
def cargar_datos_reales():
    import __main__
    # Cargamos df_q para la parte estadística
    if hasattr(__main__, 'df_q'):
        df_q_real = __main__.df_q.copy()
    else:
        # Respaldo por si acaso
        df_q_real = pd.DataFrame({
            "producto": ["Lámpara de mesa", "Auriculares", "Microondas"],
            "vtas_productos": [1279883.0, 109112.0, 1068876.0]
        })
        
    # Cargamos agrup_prod_vtas_mkt para la parte de marketing y ROI
    if hasattr(__main__, 'agrup_prod_vtas_mkt'):
        df_mkt_real = __main__.agrup_prod_vtas_mkt.copy()
    else:
        # Respaldo por si acaso
        df_mkt_real = pd.DataFrame({
            "producto": ["Lámpara de mesa", "Auriculares", "Microondas"],
            "marketing": [11262.5, 9585.0, 126917.0],
            "vtas_productos": [1279883.0, 109112.0, 1068876.0]
        })
    
    # Nos aseguramos de que el nombre de la columna de ventas sea homogéneo para los cálculos
    if 'vtas.productos' in df_q_real.columns:
        df_q_real = df_q_real.rename(columns={'vtas.productos': 'vtas_productos'})
    if 'vtas.productos' in df_mkt_real.columns:
        df_mkt_real = df_mkt_real.rename(columns={'vtas.productos': 'vtas_productos'})
        
    # Calculamos el ROI real en la tabla de marketing
    df_mkt_real["ROI_Marketing"] = df_mkt_real["vtas_productos"] / df_mkt_real["marketing"]
    
    return df_q_real, df_mkt_real

df_q, df_mkt = cargar_datos_reales()

# Cálculos estadísticos basados exactamente en tu código de cuartiles (usando df_q)
q1 = df_q['vtas_productos'].quantile(0.25).round(2)
q2 = df_q['vtas_productos'].quantile(0.50).round(2)
q3 = df_q['vtas_productos'].quantile(0.75).round(2)
v_min = round(df_q['vtas_productos'].min(), 2)
v_max = round(df_q['vtas_productos'].max(), 2)
iqr_p = q3 - q1
QRI = q3 + (1.5 * iqr_p)

# 3. PANEL LATERAL: Filtro unificado por producto
st.sidebar.header("🕹️ Controladores del Tablero")
todos_los_productos = sorted(list(set(df_q["producto"].unique()).union(set(df_mkt["producto"].unique()))))

productos_seleccionados = st.sidebar.multiselect(
    "Filtrar por Línea de Producto:",
    options=todos_los_productos,
    default=todos_los_productos
)

# Aplicamos los filtros a ambos DataFrames
df_q_filtrado = df_q[df_q["producto"].isin(productos_seleccionados)]
df_mkt_filtrado = df_mkt[df_mkt["producto"].isin(productos_seleccionados)]

# 4. CREACIÓN DE PESTAÑAS (Aquí se junta todo de forma limpia)
tab1, tab2, tab3 = st.tabs(["📊 Distribución Estadística (df_q)", "🎯 Eficiencia de Marketing (ROI)", "📋 Tablas de Datos"])

# --- PESTAÑA 1: TUS DOS BLOQUES DE CÓDIGO DE CAJAS E HISTOGRAMAS ---
with tab1:
    st.header("Análisis de Distribución de Ventas")
    st.markdown("Esta sección evalúa el comportamiento de la dispersión de las ventas mediante cuartiles y frecuencias.")
    
    # Fila de tarjetas estadísticas rápidas basadas en tus cálculos
    met1, met2, met3 = st.columns(3)
    met1.metric(label="Mediana de Ventas (Q2)", value=f"${q2:,.2f}")
    met2.metric(label="Rango Intercuartílico (IQR)", value=f"${iqr_p:,.2f}")
    met3.metric(label="Límite Atípicos (QRI)", value=f"${QRI:,.2f}")
    
    st.markdown("---")
    
    # Renderizamos tus dos gráficos juntos (el histograma y el boxplot vertical que enviaste)
    fig_dist, ax_dist = plt.subplots(1, 2, figsize=(12, 5))
    sns.set_theme(style="whitegrid")
    
    # Subplot 1: Histograma
    sns.histplot(data=df_q_filtrado, x='vtas_productos', bins="auto", ax=ax_dist[0], color="steelblue")
    ax_dist[0].set_title("Distribución de las Ventas (Frecuencia)")
    ax_dist[0].set_xlabel("Ventas de Productos")
    
    # Subplot 2: Boxplot vertical
    sns.boxplot(data=df_q_filtrado, y='vtas_productos', ax=ax_dist[1], color="skyblue", flierprops={"markerfacecolor": "red", "marker": "o"})
    ax_dist[1].axhline(QRI, color='red', linestyle='--', linewidth=1.5, label=f'Límite QRI: {QRI:.2f}')
    ax_dist[1].set_title("Distribución de las Ventas (Caja y Bigotes)")
    ax_dist[1].set_ylabel("Ventas de Productos")
    ax_dist[1].legend()
    
    plt.tight_layout()
    st.pyplot(fig_dist)
    
    # Texto analítico detallado
    st.info(f"""
    **Anotaciones de Intervalos (Datos de df_q):**
    * **Valor Mínimo Registrado:** ${v_min:,.2f}
    * **Primer Cuartil (25% - Q1):** ${q1:,.2f}
    * **Tercer Cuartil (75% - Q3):** ${q3:,.2f}
    * **Valor Máximo Detectado:** ${v_max:,.2f}
    """)

# --- PESTAÑA 2: GRÁFICO DE BARRAS DE EFICIENCIA REAL (ROI) ---
with tab2:
    st.header("Eficiencia Real: Ventas generadas por cada Peso invertido en Marketing")
    st.markdown("Evaluación cruzada del retorno obtenido por cada peso asignado a campañas de marketing usando `agrup_prod_vtas_mkt`.")
    
    if not df_mkt_filtrado.empty:
        col_mkt1, col_mkt2 = st.columns([2, 1])
        
        with col_mkt1:
            # Tu código exacto de ordenamiento y gráfico de barras horizontales
            df_analisis_graf = df_mkt_filtrado.sort_values(by="ROI_Marketing", ascending=False)
            
            fig_mkt, ax_mkt = plt.subplots(figsize=(10, 8))
            sns.barplot(
                data=df_analisis_graf,
                x="ROI_Marketing",
                y="producto",
                hue="producto",
                palette="viridis",
                legend=False,
                ax=ax_mkt
            )
            ax_mkt.set_xlabel("Multiplicador de Retorno (Ventas / Marketing)", fontsize=12)
            ax_mkt.set_ylabel("Producto", fontsize=12)
            plt.tight_layout()
            st.pyplot(fig_mkt)
            
        with col_mkt2:
            st.subheader("🎯 Métricas Clave Financieras")
            st.metric(label="💰 Ventas Totales (Segmento)", value=f"${df_mkt_filtrado['vtas_productos'].sum():,.2f}")
            st.metric(label="📢 Gasto de Marketing Acumulado", value=f"${df_mkt_filtrado['marketing'].sum():,.2f}")
            st.metric(label="📈 Multiplicador Medio (ROI)", value=f"{df_mkt_filtrado['ROI_Marketing'].mean():.2f}x")
            
            st.markdown("""
            ### **Interpretación:**
            Los productos ubicados en la parte superior devuelven una mayor cantidad de ingresos por cada peso invertido en publicidad. Las barras amarillas/verdes representan las líneas de producto con un aprovechamiento óptimo del presupuesto comercial.
            """)
    else:
        st.warning("Selecciona al menos un producto en el panel lateral para calcular el ROI.")

# --- PESTAÑA 3: LAS TABLAS DE DATOS INTERACTIVAS ---
with tab3:
    st.header("Matrices de Datos Consolidados")
    st.markdown("Tablas interactivas para auditar los registros analizados en el reporte.")
    
    st.subheader("📋 Datos de Ventas y Distribución (df_q)")
    st.dataframe(df_q_filtrado, use_container_width=True)
    
    st.subheader("📋 Datos de Marketing y Retornos (agrup_prod_vtas_mkt)")
    st.dataframe(df_mkt_filtrado, use_container_width=True)

