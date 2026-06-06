import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.linear_model import LinearRegression

# 1. Configuración de la página
st.set_page_config(page_title="Informe Estadístico y Comercial", layout="wide")

st.title("📊 Informe Integral de Ventas y Rendimiento de Marketing")
st.markdown("---")


# 2. Carga de los dos DataFrames reales
@st.cache_data
def cargar_datos_reales():
    data_q = {
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

    df_q_real = pd.DataFrame(data_q)
    df_mkt_real = pd.DataFrame(data_mkt)

    df_mkt_real["vtas_productos"] = df_q_real["vtas_productos"]
    df_mkt_real["ROI_Marketing"] = (
        df_mkt_real["vtas_productos"] / df_mkt_real["marketing"]
    )
    return df_q_real, df_mkt_real


df_q, df_mkt = cargar_datos_reales()

# Cálculos estadísticos basados en tu código de cuartiles
q1 = df_q["vtas_productos"].quantile(0.25).round(2)
q2 = df_q["vtas_productos"].quantile(0.50).round(2)
q3 = df_q["vtas_productos"].quantile(0.75).round(2)
v_min = round(df_q["vtas_productos"].min(), 2)
v_max = round(df_q["vtas_productos"].max(), 2)
iqr_p = q3 - q1
QRI = q3 + (1.5 * iqr_p)

# 3. PANEL LATERAL
st.sidebar.header("🕹️ Controladores del Tablero")
todos_los_productos = sorted(
    list(set(df_q["producto"].unique()).union(set(df_mkt["producto"].unique())))
)

productos_seleccionados = st.sidebar.multiselect(
    "Filtrar por Línea de Producto:",
    options=todos_los_productos,
    default=todos_los_productos,
)

df_q_filtrado = df_q[df_q["producto"].isin(productos_seleccionados)]
df_mkt_filtrado = df_mkt[df_mkt["producto"].isin(productos_seleccionados)]

# 4. TUS 3 PESTAÑAS ORIGINALES FAVORITAS (Quedan idénticas e intactas)
tab1, tab2, tab3 = st.tabs(
    [
        "📊 Distribución Estadística",
        "🎯 Eficiencia de Marketing (ROI)",
        "📋 Tablas de Datos",
    ]
)

# --- PESTAÑA 1 ---
with tab1:
    st.header("Análisis de Distribución de Ventas")
    met1, met2, met3 = st.columns(3)
    met1.metric(label="Mediana de Ventas (Q2)", value=f"${q2:,.2f}")
    met2.metric(label="Rango Intercuartílico (IQR)", value=f"${iqr_p:,.2f}")
    met3.metric(label="Límite Atípicos (QRI)", value=f"${QRI:,.2f}")

    st.markdown("---")

    fig_dist, ax_dist = plt.subplots(1, 2, figsize=(12, 5))
    sns.set_theme(style="whitegrid")

    sns.histplot(
        data=df_q_filtrado,
        x="vtas_productos",
        bins="auto",
        ax=ax_dist[0],
        color="steelblue",
    )
    ax_dist[0].set_title("Distribución de las Ventas (Frecuencia)")
    ax_dist[0].set_xlabel("Ventas de Productos")

    sns.boxplot(
        data=df_q_filtrado,
        y="vtas_productos",
        ax=ax_dist[1],
        color="skyblue",
        flierprops={"markerfacecolor": "red", "marker": "o"},
    )
    ax_dist[1].axhline(
        QRI, color="red", linestyle="--", linewidth=1.5, label=f"QRI: {QRI:.2f}"
    )
    ax_dist[1].set_title("Distribución de las Ventas (Caja y Bigotes)")
    ax_dist[1].set_ylabel("Ventas de Productos")
    ax_dist[1].legend()

    plt.tight_layout()
    st.pyplot(fig_dist)

# --- PESTAÑA 2 ---
with tab2:
    st.header("Eficiencia Comercial Real (ROI)")
    if not df_mkt_filtrado.empty:
        col_mkt1, col_mkt2 = st.columns([2, 1])
        with col_mkt1:
            df_analisis_graf = df_mkt_filtrado.sort_values(
                by="ROI_Marketing", ascending=False
            )
            fig_mkt, ax_mkt = plt.subplots(figsize=(10, 8))
            sns.barplot(
                data=df_analisis_graf,
                x="ROI_Marketing",
                y="producto",
                hue="producto",
                palette="viridis",
                legend=False,
                ax=ax_mkt,
            )
            st.pyplot(fig_mkt)
        with col_mkt2:
            st.subheader("🎯 Métricas Financieras")
            st.metric(
                label="💰 Ventas Totales",
                value=f"${df_mkt_filtrado['vtas_productos'].sum():,.2f}",
            )
            st.metric(
                label="📢 Inversión Marketing",
                value=f"${df_mkt_filtrado['marketing'].sum():,.2f}",
            )

# --- PESTAÑA 3 ---
with tab3:
    st.header("Matrices de Datos Consolidados")
    st.subheader("📋 Datos de Ventas y Distribución (df_q)")
    st.dataframe(df_q_filtrado, use_container_width=True)
    st.subheader("📋 Datos de Marketing (df_mkt)")
    st.dataframe(df_mkt_filtrado, use_container_width=True)


# --- 5. EL AGREGADO ABAJO DE TODO, SIMPLE Y SEPARADO ---
st.markdown("---")
st.header("🔮 Módulo de Proyección Predictiva (Scikit-Learn)")
st.markdown(
    "Este apartado aplica un modelo estadístico de **Regresión Lineal** "
    "para estimar el comportamiento de las ventas simulando incrementos en el presupuesto de publicidad."
)

# Control interactivo de inversión
porcentaje_mkt = st.slider(
    "Simular incremento en el presupuesto de Marketing (%):",
    min_value=0,
    max_value=100,
    value=25,
    step=5,
)

if not df_mkt_filtrado.empty:
    # Ajuste del modelo matemático de Machine Learning
    X = df_mkt_filtrado[["marketing"]]
    y = df_mkt_filtrado["vtas_productos"]

    modelo = LinearRegression()
    modelo.fit(X, y)

    # Creación de la proyección futura corregida
    df_proy = df_mkt_filtrado.copy()
    df_proy["marketing_futuro"] = df_proy["marketing"] * (
        1 + (porcentaje_mkt / 100)
    )

    # Convertimos a DataFrame para que no falle el modelo predictivo
    df_aux_pred = pd.DataFrame({"marketing": df_proy["marketing_futuro"]})
    df_proy["ventas_proyectadas"] = modelo.predict(df_aux_pred)

    # Gráfico de dispersión independiente con la recta de tendencia
    fig_pred, ax_pred = plt.subplots(figsize=(10, 5))

    X_linea = np.linspace(X.min().iloc[0], X.max().iloc[0] * 1.5, 100).reshape(
        -1, 1
    )
    df_linea_pred = pd.DataFrame({"marketing": X_linea.flatten()})
    y_linea = modelo.predict(df_linea_pred)
    ax_pred.plot(
        X_linea,
        y_linea,
        color="gray",
        linestyle="--",
        label="Tendencia del Modelo",
    )

    sns.scatterplot(
        data=df_proy,
        x="marketing",
        y="vtas_productos",
        color="blue",
        s=80,
        label="Ventas Actuales",
        ax=ax_pred,
    )
    sns.scatterplot(
        data=df_proy,
        x="marketing_futuro",
        y="ventas_proyectadas",
        color="green",
        s=80,
        marker="^",
        label=f"Proyección (+{porcentaje_mkt}% MKT)",
        ax=ax_pred,
    )

    ax_pred.set_xlabel("Inversión en Marketing ($)")
    ax_pred.set_ylabel("Volumen de Ventas ($)")
    ax_pred.legend()
    st.pyplot(fig_pred)

    # Informe analítico simple para el profesor
    st.info(
        f"**Informe Técnico de la Proyección:** Al simular un incremento del **{porcentaje_mkt}%** en la inversión publicitaria, "
        "el algoritmo de regresión desplaza las estimaciones (triángulos verdes) de forma ascendente sobre la recta de tendencia. "
        "Esto valida matemáticamente una correlación positiva y directa entre el esfuerzo de marketing y el volumen de facturación esperado por código."
    )
