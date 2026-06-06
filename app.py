import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="Informe de Ventas y Marketing", layout="wide"
)

st.title("📋 Panel de Control de Datos y Análisis Visual")
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

# 4. CREACIÓN DE LAS PESTAÑAS (Se agregaron las nuevas pestañas visuales)
tab1, tab2, tab3 = st.tabs(
    [
        "📋 Tablas de Datos",
        "📊 Distribución de Ventas",
        "🎯 Eficiencia de Marketing",
    ]
)

# --- PESTAÑA 1: TABLAS DE DATOS ---
with tab1:
    st.header("Matrices de Datos Consolidados")
    st.subheader("📋 Datos de Ventas y Distribución (df_q)")
    st.dataframe(df_q_filtrado, use_container_width=True)
    st.subheader("📋 Datos de Marketing (df_mkt)")
    st.dataframe(df_mkt_filtrado, use_container_width=True)

# --- PESTAÑA 2: GRÁFICOS DE DISTRIBUCIÓN (Tus gráficos 1 y 2 integrados) ---
with tab2:
    st.header("Análisis de Distribución de Ventas")

    # Cálculos estadísticos basados en los datos filtrados
    if not df_q_filtrado.empty:
        q1 = df_q_filtrado["vtas_productos"].quantile(0.25).round(2)
        q2 = df_q_filtrado["vtas_productos"].quantile(0.50).round(2)
        q3 = df_q_filtrado["vtas_productos"].quantile(0.75).round(2)
        v_min = round(df_q_filtrado["vtas_productos"].min(), 2)
        v_max = round(df_q_filtrado["vtas_productos"].max(), 2)
        iqr_p = q3 - q1
        QRI = q3 + (1.5 * iqr_p)

        # Mostrar métricas en texto tipo Markdown legible
        st.markdown(f"""
        ### **Límites de los intervalos:**
        * **Mínimo:** {v_min:,.2f} | **Primer Cuartil (Q1):** {q1:,.2f} | **Mediana (Q2):** {q2:,.2f} | **Tercer Cuartil (Q3):** {q3:,.2f} | **Máximo:** {v_max:,.2f}
        """)

        # Gráfico Combinado 1: Histograma + Boxplot Vertical
        st.subheader("📊 Histograma y Diagrama de Caja General")
        fig1, ax1 = plt.subplots(1, 2, figsize=(12, 5))
        sns.histplot(
            data=df_q_filtrado,
            x="vtas_productos",
            bins="auto",
            ax=ax1[0],
            color="steelblue",
        )
        ax1[0].set_title("Distribución de las Ventas")

        sns.boxplot(
            data=df_q_filtrado, y="vtas_productos", ax=ax1[1], color="skyblue"
        )
        ax1[1].set_title("Distribución de las Ventas")
        plt.tight_layout()
        st.pyplot(fig1)

        # Gráfico 2: Boxplot Horizontal con Línea de Atípicos (QRI)
        st.subheader("🎯 Identificación de Valores Atípicos")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        sns.set_theme(style="whitegrid")
        sns.boxplot(
            x=df_q_filtrado["vtas_productos"],
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
            "Distribución de Ventas (Gráfico de Cajas y Bigotes)", fontsize=12
        )
        ax2.set_xlabel("vtas_productos")
        ax2.legend()
        st.pyplot(fig2)

# --- PESTAÑA 3: RETORNO DE INVERSIÓN (Tu gráfico 3 integrado) ---
with tab3:
    st.header("Eficiencia Real de Marketing")

    if not df_mkt_filtrado.empty:
        # Ordenamos los productos filtrados según su ROI de mayor a menor
        df_analisis = df_mkt_filtrado.sort_values(
            by="ROI_Marketing", ascending=False
        )

        # Gráfico 3: Gráfico de barras de ROI
        fig3, ax3 = plt.subplots(figsize=(10, 10))
        sns.set_theme(style="whitegrid")
        sns.barplot(
            data=df_analisis,
            x="ROI_Marketing",
            y="producto",
            hue="producto",
            palette="viridis",
            legend=False,
            ax=ax3,
        )

        ax3.set_title(
            "Ventas generadas por cada Peso invertido en Marketing",
            fontsize=12,
            fontweight="bold",
        )
        ax3.set_xlabel("Multiplicador de Retorno (Ventas / Marketing)")
        ax3.set_ylabel("Producto")
        plt.tight_layout()
        st.pyplot(fig3)
