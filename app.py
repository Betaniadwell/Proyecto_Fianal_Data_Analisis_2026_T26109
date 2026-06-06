import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# 1. Configuración del diseño de la página
st.set_page_config(
    page_title="Informe Estadístico Comercial", layout="wide"
)
st.title("📊 Panel de Control e Informe de Rendimiento Comercial")
st.markdown("---")


# 2. Carga limpia de tus archivos reales
@st.cache_data
def cargar_datos_csv():
    df_q = (
        pd.read_csv("datos_ventas_reales.csv")
        if os.path.exists("datos_ventas_reales.csv")
        else pd.DataFrame()
    )
    agrup_mkt = (
        pd.read_csv("datos_marketing_reales.csv")
        if os.path.exists("datos_marketing_reales.csv")
        else pd.DataFrame()
    )
    return df_q, agrup_mkt


df_q, agrup_prod_vtas_mkt = cargar_datos_csv()

# 3. Creación de las Pestañas de Navegación
tab1, tab2, tab3 = st.tabs(
    [
        "📊 Distribución de Ventas",
        "🎯 Detección de Atípicos (QRI)",
        "📈 Eficiencia de Marketing (ROI)",
    ]
)

# --- PESTAÑA 1: HISTOGRAMA Y BOXPLOT PARALELOS ---
with tab1:
    st.header("Análisis de Distribución de Ventas")

    if not df_q.empty:
        fig1, ax1 = plt.subplots(1, 2, figsize=(12, 6))

        # Subplot 1: Histograma original
        sns.histplot(
            data=df_q, x="vtas_productos", bins="auto", ax=ax1[0]
        )
        ax1[0].set_title("distribución de las ventas")

        # Subplot 2: Boxplot original
        sns.boxplot(data=df_q, y="vtas_productos", ax=ax1[1])
        ax1[1].set_title("distribución de las ventas")

        plt.tight_layout()
        st.pyplot(fig1)
    else:
        st.warning("⚠️ Falta el archivo 'datos_ventas_reales.csv'")

# --- PESTAÑA 2: GRÁFICO DE BIGOTES HORIZONTAL CON LÍNEA QRI ---
with tab2:
    st.header("Identificación Estadística de Valores Atípicos")

    if not df_q.empty:
        # Cálculos matemáticos idénticos a tu cuaderno
        q1 = df_q["vtas_productos"].quantile(0.25).round(2)
        q2 = df_q["vtas_productos"].quantile(0.50).round(2)
        q3 = df_q["vtas_productos"].quantile(0.75).round(2)
        v_min = round(df_q["vtas_productos"].min(), 2)
        v_max = round(df_q["vtas_productos"].max(), 2)

        q1_p, q3_p = (
            df_q["vtas_productos"].quantile([0.25, 0.75]).round(2)
        )
        iqr_p = q3_p - q1_p
        QRI = q3_p + (1.5 * iqr_p)

        # Render de métricas en columnas limpias
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Mínimo", f"${v_min:,.2f}")
        col2.metric("Cuartil 1 (Q1)", f"${q1:,.2f}")
        col3.metric("Mediana (Q2)", f"${q2:,.2f}")
        col4.metric("Cuartil 3 (Q3)", f"${q3:,.2f}")
        col5.metric("Máximo", f"${v_max:,.2f}")

        st.markdown("---")

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        sns.set_theme(style="whitegrid")

        sns.boxplot(
            x=df_q["vtas_productos"],
            color="skyblue",
            flierprops={"markerfacecolor": "red", "marker": "o"},
            ax=ax2,
        )
        ax2.axvline(
            QRI,
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Límite Atípicos (QRI): {QRI:.2f}",
        )

        ax2.set_title(
            "Distribución de Ventas (Gráfico de Cajas y Bigotes)",
            fontsize=14,
            pad=15,
        )
        ax2.set_xlabel("vtas_productos", fontsize=12)
        ax2.legend()

        st.pyplot(fig2)

# --- PESTAÑA 3: TU BLOQUE CORREGIDO SIN EL ERROR DE HUE ---
with tab3:
    st.header("Eficiencia Real de Marketing")

    if not agrup_prod_vtas_mkt.empty:
        # 1. Copia de trabajo idéntica a tu cuaderno original
        df_analisis = agrup_prod_vtas_mkt.copy()

        # 2. Cálculo real de ROI
        df_analisis["ROI_Marketing"] = (
            df_analisis["vtas_productos"] / df_analisis["marketing"]
        )

        # 3. Ordenamiento estricto
        df_analisis = df_analisis.sort_values(
            by="ROI_Marketing", ascending=False
        )

        # 4. Configuración del contenedor gráfico
        fig3, ax3 = plt.subplots(figsize=(10, 12))
        sns.set_theme(style="whitegrid")

        # Barras sin la propiedad 'hue' para evitar que desaparezca
        sns.barplot(
            data=df_analisis,
            x="ROI_Marketing",
            y="producto",
            palette="viridis",
            ax=ax3,
        )

        # 5. Etiquetas del gráfico original
        ax3.set_title(
            "Eficiencia Real: Ventas generadas por cada Peso invertido en Marketing",
            fontsize=14,
            fontweight="bold",
        )
        ax3.set_xlabel(
            "Multiplicador de Retorno (Ventas / Marketing)", fontsize=12
        )
        ax3.set_ylabel("Producto", fontsize=12)

        plt.tight_layout()
        st.pyplot(fig3)
    else:
        st.warning(
            "⚠️ No se encontraron datos comerciales para calcular el ROI."
        )
