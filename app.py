import os
import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.graph_objects as go

# 1. Configuración del diseño de la página
st.set_page_config(page_title="Informe Estadístico Comercial", layout="wide")
st.title("📊 Panel de Control e Informe de Rendimiento Comercial")
st.markdown("---")

# 2. Carga de los DataFrames reales
@st.cache_data
def cargar_datos_csv():
    archivo_ventas = "datos_ventas_perfectos.csv"
    archivo_mkt = "datos_roi_perfectos.csv"

    def buscar_y_leer(nombre_archivo):
        if os.path.exists(nombre_archivo):
            return pd.read_csv(nombre_archivo)
        
        # Aquí corregimos la alineación (4 espacios para la función, 4 para el if)
        b = glob.glob("**/" + nombre_archivo, recursive=True)
        if b:
            return pd.read_csv(b[0]) # Agregamos [0] para leer el primer archivo encontrado
        return pd.DataFrame()

    df_q = buscar_y_leer(archivo_ventas)
    agrup_mkt = buscar_y_leer(archivo_mkt)
    return df_q, agrup_mkt


# 3. Creación de las 4 Pestañas de Navegación
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Distribución y Análisis Estadístico",
    "🎯 Detección de Atípicos (Vallas de Tukey)",
    "📈 Eficiencia de Marketing (ROI)",
    "🌌 Gráfico de Dispersión Comercial"
])

# --- PESTAÑA 1: DISTRIBUCIÓN Y BOXPLOT ---
with tab1:
    st.header("Análisis de Distribución de Ventas")
    
    if not df_q.empty:
        col_izq, col_der = st.columns(2)
        
        with col_izq:
            fig_hist, ax_hist = plt.subplots(figsize=(6, 5))
            # Se verifica si la columna es 'vtas_productos' o 'precio' según tus datos limpios
            col_vta = 'vtas_productos' if 'vtas_productos' in df_q.columns else df_q.columns[1]
            sns.histplot(data=df_q, x=col_vta, bins="auto", ax=ax_hist, color="steelblue")
            ax_hist.set_title("Distribución de las Ventas (Histograma)")
            st.pyplot(fig_hist)
            
        with col_der:
            fig_box, ax_box = plt.subplots(figsize=(6, 5.5))
            sns.boxplot(data=df_q, y=col_vta, ax=ax_box, color="skyblue")
            ax_box.set_title("Distribución de las Ventas (Caja y Bigotes)")
            st.pyplot(fig_box)
    else:
        st.warning("⚠️ No se pudieron cargar los datos de ventas para esta pestaña.")


# --- PESTAÑA 2: DETECCIÓN DE ATÍPICOS (VALLAS DE TUKEY) ---
with tab2:
    st.header("🎯 Detección de Atípicos (Método de Vallas de Tukey)")
    
    if not df_q.empty:
        col_vta = 'vtas_productos' if 'vtas_productos' in df_q.columns else df_q.columns[1]
        
        # 1. Cálculos estadísticos en tiempo real
        q1 = df_q[col_vta].quantile(0.25).round(2)
        q2 = df_q[col_vta].quantile(0.50).round(2)
        q3 = df_q[col_vta].quantile(0.75).round(2)
        v_min = round(df_q[col_vta].min(), 2)
        v_max = round(df_q[col_vta].max(), 2)
        
        qri_distancia = q3 - q1
        valla_tukey_sup = q3 + (1.5 * qri_distancia)
        atipicos = df_q[df_q[col_vta] > valla_tukey_sup].copy()

        col_datos, col_grafico = st.columns(2)
        
        with col_datos:
            st.subheader("📋 Resumen de Intervalos")
            st.markdown(f"""
            * **Mínimo:** ${v_min:,.2f}
            * **Primer Cuartil (Q1):** ${q1:,.2f}
            * **Mediana (Q2):** ${q2:,.2f}
            * **Tercer Cuartil (Q3 / Límite 75%):** ${q3:,.2f}
            * **Máximo:** ${v_max:,.2f}
            """)
            st.info(f"📐 **Rango Intercuartílico (QRI - Ancho de Caja):** ${qri_distancia:,.2f}")
            st.error(f"🛑 **Valla de Tukey (Límite Atípicos):** ${valla_tukey_sup:,.2f}")
            
            if not atipicos.empty:
                st.warning(f"⚠️ Se detectaron **{len(atipicos)}** registros atípicos por encima del límite.")
            else:
                st.success("✅ No se detectaron valores atípicos superiores.")

        with col_grafico:
            # 2. Renderizado del Gráfico de Cajas personalizado corregido
            fig_qri, ax_qri = plt.subplots(figsize=(10, 4.5))
            sns.set_theme(style="whitegrid")
            sns.boxplot(
                x=df_q[col_vta], 
                color="skyblue", 
                flierprops={"markerfacecolor": "red", "marker": "D"},
                ax=ax_qri
            )
            ax_qri.axvline(valla_tukey_sup, color="red", linestyle="--", label="Valla de Tukey")
            ax_qri.set_title("Identificación Visual de Valores Atípicos")
            ax_qri.legend()
            st.pyplot(fig_qri)


# --- PESTAÑA 3: EFICIENCIA DE MARKETING (GRÁFICO INTERACTIVO DE COLAB) ---
with tab3:
    st.header("📈 Eficiencia de Marketing (ROI)")
    
    if not agrup_prod_vtas_mkt.empty:
        # Se verifica la estructura del dataframe cargado desde el CSV
        st.subheader("Análisis de Inversión: Ventas vs Marketing (Top 5 Productos)")
        
        # Preparación de datos (Top 5 con el ajuste x50 de Colab)
        top_smart = agrup_prod_vtas_mkt.head(5).copy()
        top_smart['marketing_visual'] = top_smart['marketing'] * 50

        # Construcción del gráfico interactivo Plotly
        fig = go.Figure()

        # Barra de Ventas (Azul claro de fondo)
        fig.add_trace(go.Bar(
            x=top_smart['producto'],
            y=top_smart['vtas_productos'],
            name='Ventas Totales',
            marker_color='#3498db',
            opacity=0.3,
            text=top_smart['vtas_productos'],
            texttemplate='$%{text:,.2s}', 
            textposition='outside',
            textfont=dict(color='#2a3f5f', size=12)
        ))

        # Barra de Marketing (Rosado - Impacto x50)
        fig.add_trace(go.Bar(
            x=top_smart['producto'],
            y=top_smart['marketing_visual'],
            name='Marketing (Impacto x50)',
            marker_color='#FF2266',
            text=top_smart['marketing_visual'],
            texttemplate='<b>$ %{text:,.0f}</b>',
            textposition='inside',
            insidetextanchor='middle',
            insidetextfont=dict(color='white', size=11),
            customdata=top_smart['marketing'],
            hovertemplate='<b>Gasto Real:</b> $%{customdata:,.2f}<extra></extra>'
        ))

        # Diseño del Layout adaptado para la Web de Streamlit
        fig.update_layout(
            barmode='overlay',
            template="plotly_white",
            xaxis=dict(tickangle=0, title="Productos"),
            yaxis=dict(tickformat="$,.0s", title="Monto ($)"),
            legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
            margin=dict(l=40, r=40, t=40, b=40),
            height=500
        )

        # Ajuste de grosores de barra
        fig.update_traces(width=0.6, selector=dict(name='Ventas Totales'))
        fig.update_traces(width=0.45, selector=dict(name='Marketing (Impacto x50)'))

        # Despliegue responsivo de Plotly en Streamlit (Usa todo el ancho sin deformarse)
        st.plotly_chart(fig, use_container_width=True)
        
        # Opcional: Mostrar la tabla detallada abajo del gráfico
        with st.expander("🔍 Ver Tabla de Datos de Marketing y Ventas"):
            st.dataframe(agrup_prod_vtas_mkt, use_container_width=True)
    else:
        st.warning("⚠️ No se encontró el archivo 'datos_roi_perfectos.csv'. Súbelo desde Colab para calcular los gráficos.")


# --- PESTAÑA 4: GRÁFICO DE DISPERSIÓN ---
with tab4:
    st.header("🌌 Gráfico de Dispersión Comercial")
    st.markdown("Sección reservada para el análisis relacional de variables comerciales.")
