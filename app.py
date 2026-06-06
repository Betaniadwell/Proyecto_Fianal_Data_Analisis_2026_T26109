import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# 1. Configuración del diseño de la página
st.set_page_config(page_title="Informe Estadístico Comercial", layout="wide")
st.title("📊 Panel de Control e Informe de Rendimiento Comercial")
st.markdown("---")

# 2. Creación de las Pestañas de Navegación Tradicionales
tab1, tab2, tab3 = st.tabs([
    "📊 Distribución y Análisis Estadístico",
    "🎯 Eficiencia de Marketing (ROI)",
    "🌌 Gráfico de Dispersión Comercial"
])

# --- PESTAÑA 1: DISTRIBUCIÓN Y BOXPLOT (DATOS REALES DE VENTAS) ---
with tab1:
    st.header("Análisis de Distribución de Ventas")
    
    if os.path.exists("datos_ventas_perfectos.csv"):
        df_q = pd.read_csv("datos_ventas_perfectos.csv")
        
        # Separamos el espacio en 2 columnas tradicionales para mantener el tamaño original
        col_izq, col_der = st.columns(2)
        
        with col_izq:
            fig_hist, ax_hist = plt.subplots(figsize=(6, 5))
            sns.histplot(data=df_q, x='vtas_productos', bins="auto", ax=ax_hist, color="steelblue")
            ax_hist.set_title("Distribución de las Ventas (Histograma)")
            st.pyplot(fig_hist)
            
        with col_der:
            fig_box, ax_box = plt.subplots(figsize=(6, 5))
            sns.boxplot(data=df_q, y='vtas_productos', ax=ax_box, color="skyblue")
            ax_box.set_title("Distribución de las Ventas (Caja y Bigotes)")
            st.pyplot(fig_box)
    else:
        st.warning("⚠️ Por favor, sube el archivo 'datos_ventas_perfectos.csv' a GitHub para activar esta pestaña.")

# --- PESTAÑA 2: EL GRÁFICO DE BARRAS DE ROI QUE YA QUEDÓ PERFECTO ---
with tab2:
    st.header("Eficiencia Real de Marketing")
    
    if os.path.exists("datos_roi_perfectos.csv"):
        df_analisis = pd.read_csv("datos_roi_perfectos.csv")
        
        fig_roi, ax_roi = plt.subplots(figsize=(10, 12))
        sns.set_theme(style="whitegrid")
        
        sns.barplot(data=df_analisis, x="ROI_Marketing", y="producto", palette="viridis", ax=ax_roi)
        
        plt.title("Eficiencia Real: Ventas generadas por cada Peso invertido en Marketing", fontsize=14, fontweight="bold")
        plt.xlabel("Multiplicador de Retorno (Ventas / Marketing)", fontsize=12)
        plt.ylabel("Producto", fontsize=12)
        plt.tight_layout()
        st.pyplot(fig_roi)
    else:
        st.warning("⚠️ Falta el archivo 'datos_roi_perfectos.csv' en tu GitHub.")

# --- PESTAÑA 3: TU GRÁFICO DE DISPERSIÓN COMERCIAL ---
with tab3:
    st.header("Análisis de Dispersión: Inversión vs. Ventas")
    st.markdown("Este gráfico permite visualizar qué productos tienen mayor tracción comercial en relación con su presupuesto asignado.")
    
    if os.path.exists("datos_roi_perfectos.csv"):
        df_analisis = pd.read_csv("datos_roi_perfectos.csv")
        
        # Si las columnas de tu dataframe de ROI contienen marketing y vtas_productos
        if "marketing" in df_analisis.columns and "vtas_productos" in df_analisis.columns:
            fig_scat, ax_scat = plt.subplots(figsize=(10, 6))
            sns.set_theme(style="whitegrid")
            
            # Dibujamos el scatter plot original
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
        else:
            st.info("💡 Para ver la dispersión, asegúrate de que el archivo exportado contenga las columnas 'marketing' y 'vtas_productos'.")
