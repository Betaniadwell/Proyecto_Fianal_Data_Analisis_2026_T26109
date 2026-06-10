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
    archivo_mkt = "datos_agrupados_marketing.csv"  # El nuevo archivo independiente

    def buscar_y_leer(nombre_archivo):
        if os.path.exists(nombre_archivo):
            return pd.read_csv(nombre_archivo)
        b = glob.glob("**/" + nombre_archivo, recursive=True)
        if b:
            return pd.read_csv(b[0])  # Toma la primera coincidencia encontrada en la lista
        return pd.DataFrame()

    df_q = buscar_y_leer(archivo_ventas)
    agrup_mkt = buscar_y_leer(archivo_mkt)
    return df_q, agrup_mkt

df_q, agrup_prod_vtas_mkt = cargar_datos_csv()

# 3. Creación de las 4 Pestañas de Navegación
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Distribución y Análisis Estadístico",
    "🎯 Detección de Atípicos (QRI)",
    "📈 Eficiencia de Marketing (ROI)",
    "🌌 Gráfico de Dispersión Comercial"
])

# --- PESTAÑA 1: DISTRIBUCIÓN Y BOXPLOT ---
with tab1:
    st.header("Análisis de Distribución de Ventas")
    
    if not df_q.empty:
        col_izq, col_der = st.columns(2)
        col_vta = 'vtas_productos' if 'vtas_productos' in df_q.columns else df_q.columns[0]
        
        with col_izq:
            fig_hist, ax_hist = plt.subplots(figsize=(6, 5))
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


# --- NUEVA PESTAÑA 2: DETECCIÓN DE ATÍPICOS (QRI) ---
with tab2:
    st.header("🎯 Detección de Atípicos (Rango Intercuartílico)")
    
    if not df_q.empty:
        col_vta = 'vtas_productos' if 'vtas_productos' in df_q.columns else df_q.columns[0]
        
        # 1. Cálculos estadísticos en tiempo real
        q1 = df_q[col_vta].quantile(0.25).round(2)
        q2 = df_q[col_vta].quantile(0.50).round(2)
        q3 = df_q[col_vta].quantile(0.75).round(2)
        v_min = round(df_q[col_vta].min(), 2)
        v_max = round(df_q[col_vta].max(), 2)
        
        iqr_p = q3 - q1
        QRI = q3 + (1.5 * iqr_p)
        
        # Filtrado de registros que superan el límite QRI
        atipicos = df_q[df_q[col_vta] > QRI].copy()

        # Diseño de dos columnas: Datos a la izquierda, Gráfico a la derecha
        col_datos, col_grafico = st.columns(2)
        
        with col_datos:
            st.subheader("📋 Resumen de Intervalos")
            st.markdown(f"""
            * **Mínimo:** ${v_min:,.2f}
            * **Primer Cuartil (q1):** ${q1:,.2f}
            * **Mediana (q2):** ${q2:,.2f}
            * **Tercer Cuartil (q3):** ${q3:,.2f}
            * **Máximo:** ${v_max:,.2f}
            """)
            st.info(f"**Línea Límite de Atípicos (QRI):** ${QRI:,.2f}")
            
            # Muestra cuántos registros superan el límite
            if not atipicos.empty:
                st.error(f"⚠️ Se detectaron **{len(atipicos)}** registros atípicos por encima del límite.")
            else:
                st.success("✅ No se detectaron valores atípicos superiores.")

        with col_grafico:
            # 2. Renderizado del Gráfico de Cajas personalizado
            fig_qri, ax_qri = plt.subplots(figsize=(10, 4.5))
            sns.set_theme(style="whitegrid")
            
            sns.boxplot(
                x=df_q[col_vta], 
                color="skyblue", 
                flierprops={"markerfacecolor": "red", "marker": "o", "markersize": 8},
                ax=ax_qri
            )
            
            # Línea roja de corte
            ax_qri.axvline(QRI, color='red', linestyle='--', linewidth=2, label=f'Límite QRI: {QRI:,.2f}')
            
            ax_qri.set_title('Distribución de Ventas con Límite de Atípicos', fontsize=14, pad=15)
            ax_qri.set_xlabel('Ventas de Productos ($)', fontsize=12)
            ax_qri.legend()
            
            st.pyplot(fig_qri)
            
        # --- NUEVA SECCIÓN: TABLA DE PRODUCTOS ATÍPICOS ---
        st.markdown("---")
        st.subheader("🔍 Listado Detallado de Ventas Atípicas")
        
        if not atipicos.empty:
            st.markdown("Los siguientes registros representan transacciones o productos con un volumen de ventas excepcionalmente alto:")
            
            # Ordenamos de mayor a menor venta para destacar los más importantes
            atipicos_ordenados = atipicos.sort_values(by=col_vta, ascending=False)
            
            # Mostramos la tabla formateada con Streamlit
            st.dataframe(
                atipicos_ordenados, 
                use_container_width=True,
                column_config={
                    col_vta: st.column_config.NumberColumn(
                        "Ventas de Productos",
                        format="$%,.2f"
                    )
                }
            )
        else:
            st.info(f"No hay filas para mostrar ya que ningún registro supera el límite estadístico de {QRI:,.2f}.")
            
    else:
        st.warning("⚠️ No hay datos disponibles para el análisis QRI.")


# --- PESTAÑA 3: EFICIENCIA DE MARKETING (ROI) CON GRÁFICO NUEVO ---
with tab3:
    st.header("📈 Eficiencia de Marketing (ROI)")
    
    if not agrup_prod_vtas_mkt.empty:
        st.subheader("Análisis de Inversión: Ventas vs Marketing (Top 5 Productos)")
        
        # Preparación de datos basándose en tu DataFrame agrupado de Colab
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

        # Diseño Final del Layout para Web
        fig.update_layout(
            barmode='overlay',
            template="plotly_white",
            xaxis=dict(tickangle=0, title="Productos"),
            yaxis=dict(tickformat="$,.0s", title="Monto ($)"),
            legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
            margin=dict(l=40, r=40, t=40, b=40),
            height=500
        )

        # Ajuste de grosores
        fig.update_traces(width=0.6, selector=dict(name='Ventas Totales'))
        fig.update_traces(width=0.45, selector=dict(name='Marketing (Impacto x50)'))

        # Despliegue responsivo de Plotly en Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
        # Despliegue de la nueva tabla agregada abajo del gráfico
        with st.expander("🔍 Ver Tabla de Datos de Marketing y Ventas (Subida desde Git)"):
            st.dataframe(agrup_prod_vtas_mkt, use_container_width=True)
    else:
        st.warning("⚠️ No se encontró el archivo 'datos_agrupados_marketing.csv'. Verifica haberlo subido desde Colab.")


# --- PESTAÑA 4: GRÁFICO DE DISPERSIÓN ---
with tab4:
    st.header("🌌 Gráfico de Dispersión Comercial")
    st.markdown("Sección reservada para el análisis relacional de variables comerciales.")
