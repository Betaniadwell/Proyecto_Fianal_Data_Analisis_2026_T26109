import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# 1. Configuración del diseño de la página
st.set_page_config(page_title="Informe Estadístico Comercial", layout="wide")
st.title("📊 Panel de Control e Informe de Rendimiento Comercial")
st.markdown("---")

# 2. Carga de los DataFrames reales
@st.cache_data
def cargar_datos_csv():
    archivo_ventas = "datos_ventas_perfectos.csv"
    archivo_mkt = "datos_roi_perfectos.csv"

    if os.path.exists(archivo_ventas):
        df_q = pd.read_csv(archivo_ventas)
    else:
        import glob
        b = glob.glob("**/" + archivo_ventas, recursive=True)
        df_q = pd.read_csv(b) if b else pd.DataFrame()

    if os.path.exists(archivo_mkt):
        agrup_mkt = pd.read_csv(archivo_mkt)
    else:
        import glob
        b = glob.glob("**/" + archivo_mkt, recursive=True)
        agrup_mkt = pd.read_csv(b) if b else pd.DataFrame()

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
        
        with col_izq:
            fig_hist, ax_hist = plt.subplots(figsize=(6, 5))
            sns.histplot(data=df_q, x='vtas_productos', bins="auto", ax=ax_hist, color="steelblue")
            ax_hist.set_title("Distribución de las Ventas (Histograma)")
            st.pyplot(fig_hist)
            
        with col_der:
            fig_box, ax_box = plt.subplots(figsize=(6, 5.5))
            sns.boxplot(data=df_q, y='vtas_productos', ax=ax_box, color="skyblue")
            ax_box.set_title("Distribución de las Ventas (Caja y Bigotes)")
            st.pyplot(fig_box)
    else:
        st.warning("⚠️ No se pudieron cargar los datos de ventas para esta pestaña.")


# --- PESTAÑA 2: DETECCIÓN DE ATÍPICOS (QRI) ---
with tab2:
    st.header("🎯 Detección de Atípicos (Rango Intercuartílico)")
    
    if not df_q.empty:
        # 1. Cálculos estadísticos en tiempo real
        q1 = df_q['vtas_productos'].quantile(0.25).round(2)
        q2 = df_q['vtas_productos'].quantile(0.50).round(2)
        q3 = df_q['vtas_productos'].quantile(0.75).round(2)
        v_min = round(df_q['vtas_productos'].min(), 2)
        v_max = round(df_q['vtas_productos'].max(), 2)
        
        iqr_p = q3 - q1
        QRI = q3 + (1.5 * iqr_p)
        
        # Filtrado de registros que superan el límite QRI
        atipicos = df_q[df_q['vtas_productos'] > QRI].copy()

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
                x=df_q['vtas_productos'], 
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
            
        # --- TABLA DE PRODUCTOS ATÍPICOS ---
        st.markdown("---")
        st.subheader("🔍 Listado Detallado de Ventas Atípicas")
        
        if not atipicos.empty:
            st.markdown("Los siguientes registros representan transacciones o productos con un volumen de ventas excepcionalmente alto:")
            
            # Ordenamos de mayor a menor venta para destacar los más importantes
            atipicos_ordenados = atipicos.sort_values(by='vtas_productos', ascending=False)
            
            # Mostramos la tabla formateada con Streamlit
            st.dataframe(
                atipicos_ordenados, 
                use_container_width=True,
                column_config={
                    "vtas_productos": st.column_config.NumberColumn(
                        "Ventas de Productos",
                        format="$%,.2f"
                    )
                }
            )
        else:
            st.info(f"No hay filas para mostrar ya que ningún registro supera el límite estadístico.")
            
    else:
        st.warning("⚠️ No hay datos disponibles para el análisis QRI.")


# --- PESTAÑA 3: EL GRÁFICO DE BARRAS DE ROI ---
with tab3:
    st.header("Eficiencia Real de Marketing")
    
    if not agrup_prod_vtas_mkt.empty:
        df_analisis = agrup_prod_vtas_mkt.copy()
        df_analisis["ROI_Marketing"] = df_analisis["vtas_productos"] / df_analisis["marketing"]
        df_analisis = df_analisis.sort_values(by="ROI_Marketing", ascending=False)
        
        fig_roi, ax_roi = plt.subplots(figsize=(10, 12))
        sns.set_theme(style="whitegrid")
        
        sns.barplot(data=df_analisis, x="ROI_Marketing", y="producto", palette="viridis", ax=ax_roi)
        
        plt.title("Eficiencia Real: Ventas generadas por cada Peso invertido en Marketing", fontsize=14, fontweight="bold")
        plt.xlabel("Multiplicador de Retorno (Ventas / Marketing)", fontsize=12)
        plt.ylabel("Producto", fontsize=12)
        plt.tight_layout()
        st.pyplot(fig_roi)
    else:
        st.warning("⚠️ No se encontraron datos para calcular el ROI.")


# --- PESTAÑA 4: GRÁFICO DE DISPERSIÓN COMERCIAL + CONCLUSIONES ---
with tab4:
    st.header("Análisis de Dispersión: Inversión vs. Ventas")
    st.markdown("Este gráfico permite visualizar qué productos tienen mayor tracción comercial en relación con su presupuesto asignado.")
    
    if not agrup_prod_vtas_mkt.empty:
        df_analisis = agrup_prod_vtas_mkt.copy()
        df_analisis["ROI_Marketing"] = df_analisis["vtas_productos"] / df_analisis["marketing"]
        
        if "marketing" in df_analisis.columns and "vtas_productos" in df_analisis.columns:
            fig_scat, ax_scat = plt.subplots(figsize=(10, 6))
            sns.set_theme(style="whitegrid")
            
            sns.scatterplot(
                data=df_analisis, 
                x="marketing", 
                y="vtas_productos", 
                hue="producto", 
                size="ROI_Marketing", 
                sizes=(40, 400), 
                palette="viridis", 
                legend=False,
                ax=ax_scat
            )
            
            ax_scat.set_title("Relación entre Inversión en Publicidad y Ventas Totales", fontsize=14, fontweight="bold")
            ax_scat.set_xlabel("Presupuesto de Marketing ($)", fontsize=12)
            ax_scat.set_ylabel("Ventas de Productos ($)", fontsize=12)
            plt.tight_layout()
            st.pyplot(fig_scat)
            
            st.markdown("---")
            st.subheader("💡 Conclusiones y Diagnóstico Estratégico")
            
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.success("""
                **🚀 Oportunidades de Crecimiento (Cuadrante Superior Izquierdo):**
                * Detectamos productos con **baja inversión en publicidad** que generan **ventas masivas** (cercanas a \$1.2M). 
                * *Acción recomendada:* Incrementar el presupuesto de marketing en estos artículos de alta tracción orgánica.
                """)
                st.info("""
                **📈 Motores de Caja Estables (Línea Central):**
                * Las burbujas verdes demuestran un rendimiento constante entre \$600K y \$800K. Responden bien a aumentos de presupuesto, pero muestran un efecto de saturación al llegar al límite de su mercado.
                """)
            with col_info2:
                st.error("""
                **⚠️ Alertas de Pérdida / Ineficiencia (Zona Inferior):**
                * Las burbujas amarillas y pequeñas representan productos que, a pesar de recibir inversión constante (\$5K+), devuelven muy pocas ventas (menos de \$400K).
                * *Acción recomendada:* Pausar o reestructurar de inmediato las campañas publicitarias de estos artículos.
                """)
        else:
            st.info("💡 El archivo debe contener las columnas 'marketing' y 'vtas_productos'.")
