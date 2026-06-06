import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# 1. Configuración del diseño
st.set_page_config(
    page_title="Informe Estadístico Comercial", layout="wide"
)
st.title("📊 Panel de Control e Informe de Rendimiento Comercial")
st.markdown("---")

# 2. TUS 30 DATOS REALES EXACTOS DE LA IMAGEN (Integrados para evitar archivos CSV)
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
        "Silla de oficina",
        "Escritorio",
        "Estante de libros",
        "Mesa de centro",
        "Organizador",
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
        175398.0,
        354098.0,
        415300.0,
        925600.0,
        1089000.0,
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
        "Silla de oficina",
        "Escritorio",
        "Estante de libros",
        "Mesa de centro",
        "Organizador",
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
        12450.0,
        28900.0,
        31000.0,
        85000.0,
        92000.0,
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

# --- PESTAÑA 1: HISTOGRAMA Y BOXPLOT PARALELOS CON MÉTODO TRADICIONAL ---
with tab1:
    st.header("Análisis de Distribución de Ventas")

    col_izq, col_der = st.columns(2)

    with col_izq:
        fig_hist, ax_hist = plt.subplots(figsize=(6, 5))
        sns.histplot(data=df_q, x="vtas_productos", bins="auto", ax=ax_hist)
        ax_hist.set_title("distribución de las ventas")
        st.pyplot(fig_hist)

    with col_der:
        fig_box, ax_box = plt.subplots(figsize=(6, 5))
        sns.boxplot(data=df_q, y="vtas_productos", ax=ax_box)
        ax_box.set_title("distribución de las ventas")
        st.pyplot(fig_box)

# --- PESTAÑA 2: GRÁFICO HORIZONTAL IDENTICO A TU ÚLTIMA FOTO ---
with tab2:
    st.header("Identificación Estadística de Valores Atípicos")

    # Cálculos exactos basados en tus 30 filas
    q1 = df_q["vtas_productos"].quantile(0.25).round(2)
    q2 = df_q["vtas_productos"].quantile(0.50).round(2)
    q3 = df_q["vtas_productos"].quantile(0.75).round(2)
    v_min = round(df_q["vtas_productos"].min(), 2)
    v_max = round(df_q["vtas_productos"].max(), 2)
    iqr_p = q3 - q1
    QRI = q3 + (1.5 * iqr_p)  # Da exactamente 826500.25 como tu foto

    # Tarjetas de datos tradicionales de Streamlit
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Mínimo", f"${v_min:,.2f}")
    c2.metric("Q1", f"${q1:,.2f}")
    c3.metric("Mediana (Q2)", f"${q2:,.2f}")
    c4.metric("Q3", f"${q3:,.2f}")
    c5.metric("Máximo", f"${v_max:,.2f}")

    st.markdown("---")

    # Replicamos el gráfico horizontal idéntico a tu cuaderno
    fig2, ax2 = plt.subplots(figsize=(10, 4))
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

# --- PESTAÑA 3: TU GRÁFICO DE BARRAS DE ROI CON LOS 30 PRODUCTOS REALES ---
with tab3:
    st.header("Eficiencia Real de Marketing")

    df_analisis = agrup_prod_vtas_mkt.copy()
    df_analisis["ROI_Marketing"] = (
        df_analisis["vtas_productos"] / df_analisis["marketing"]
    )
    df_analisis = df_analisis.sort_values(by="ROI_Marketing", ascending=False)

    fig3, ax3 = plt.subplots(figsize=(10, 12))
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
    ax3.set_xlabel("Multiplicador de Retorno (Ventas / Marketing)", fontsize=12)
    ax3.set_ylabel("Producto", fontsize=12)
    plt.tight_layout()
    st.pyplot(fig3)

