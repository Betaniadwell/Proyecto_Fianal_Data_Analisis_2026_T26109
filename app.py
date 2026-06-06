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

# 2. TUS DATOS REALES INTEGRADOS (Sin depender de archivos externos)
data_ventas = {
    "producto": [
        "Lámpara de mesa",
        "Auriculares",
        "Microondas",
        "Cafetera",
        "Smartphone",
        "Freidora eléctrica",
        "Batidora",
        "Aspiradora",
        "Adorno de pared",
        "Horno eléctrico",
        "Espejo decorativo",
        "Consola de videojuegos",
        "Rincón de plantas",
        "Smartwatch",
        "Laptop",
        "Lavadora",
        "Cuadro decorativo",
        "Jarrón decorativo",
        "Alfombra",
        "Proyector",
        "Televisor",
        "Cortinas",
        "Secadora",
        "Plancha de vapor",
        "Parlantes bluetooth",
    ],
    "vtas_productos": [
        1279883.0,
        109112.0,
        1068876.0,
        92484.0,
        82212.0,
        78251.0,
        77537.0,
        77447.0,
        76097.0,
        75688.0,
        75663.0,
        75583.0,
        75572.0,
        75535.0,
        75326.0,
        74953.0,
        74578.0,
        74534.0,
        74098.0,
        73933.0,
        73815.0,
        73649.0,
        73338.0,
        73039.0,
        72111.0,
    ],
}

data_mkt = {
    "producto": [
        "Lámpara de mesa",
        "Auriculares",
        "Microondas",
        "Cafetera",
        "Smartphone",
        "Freidora eléctrica",
        "Batidora",
        "Aspiradora",
        "Adorno de pared",
        "Horno eléctrico",
        "Espejo decorativo",
        "Consola de videojuegos",
        "Rincón de plantas",
        "Smartwatch",
        "Laptop",
        "Lavadora",
        "Cuadro decorativo",
        "Jarrón decorativo",
        "Alfombra",
        "Proyector",
        "Televisor",
        "Cortinas",
        "Secadora",
        "Plancha de vapor",
        "Parlantes bluetooth",
    ],
    "marketing": [
        11262.5,
        9585.0,
        126917.0,
        76544.0,
        65552.5,
        7217.0,
        4138.0,
        4106.0,
        5868.5,
        7743.5,
        5577.0,
        3395.0,
        4905.5,
        6041.0,
        3350.5,
        3250.5,
        5021.5,
        6833.5,
        455.0,
        4497.5,
        4788.0,
        3393.5,
        4957.0,
        3331.5,
        4905.5,
    ],
}

df_q = pd.DataFrame(data_ventas)
agrup_prod_vtas_mkt = pd.DataFrame(data_mkt)
agrup_prod_vtas_mkt["vtas_productos"] = df_q["vtas_productos"]

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

    fig1, ax1 = plt.subplots(1, 2, figsize=(12, 6))

    # Subplot 1: Histograma original tal cual tu cuaderno
    sns.histplot(data=df_q, x="vtas_productos", bins="auto", ax=ax1[0])
    ax1[0].set_title("distribución de las ventas")

    # Subplot 2: Boxplot original tal cual tu cuaderno
    sns.boxplot(data=df_q, y="vtas_productos", ax=ax1[1])
    ax1[1].set_title("distribución de las ventas")

    plt.tight_layout()
    st.pyplot(fig1)

# --- PESTAÑA 2: GRÁFICO DE BIGOTES HORIZONTAL CON LÍNEA QRI ---
with tab2:
    st.header("Identificación Estadística de Valores Atípicos")

    # Cálculos estadísticos exactos de tu cuaderno
    q1 = df_q["vtas_productos"].quantile(0.25).round(2)
    q2 = df_q["vtas_productos"].quantile(0.50).round(2)
    q3 = df_q["vtas_productos"].quantile(0.75).round(2)
    v_min = round(df_q["vtas_productos"].min(), 2)
    v_max = round(df_q["vtas_productos"].max(), 2)

    q1_p, q3_p = df_q["vtas_productos"].quantile([0.25, 0.75]).round(2)
    iqr_p = q3_p - q1_p
    QRI = q3_p + (1.5 * iqr_p)

    # Tarjetas de métricas
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

# --- PESTAÑA 3: TU BLOQUE DE ROI SIN ERRORES ---
with tab3:
    st.header("Eficiencia Real de Marketing")

    df_analisis = agrup_prod_vtas_mkt.copy()
    df_analisis["ROI_Marketing"] = (
        df_analisis["vtas_productos"] / df_analisis["marketing"]
    )
    df_analisis = df_analisis.sort_values(
        by="ROI_Marketing", ascending=False
    )

    fig3, ax3 = plt.subplots(figsize=(10, 12))
    sns.set_theme(style="whitegrid")

    sns.barplot(
        data=df_analisis,
        x="ROI_Marketing",
        y="producto",
        palette="viridis",
        ax=ax3,
    )

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

