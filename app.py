import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Configuración del diseño
st.set_page_config(
    page_title="Informe Estadístico Comercial", layout="wide"
)
st.title("📊 Panel de Control e Informe de Rendimiento Comercial")
st.markdown("---")

# Carga el CSV exacto que exportaste desde Colab
if os.path.exists("datos_roi_perfectos.csv"):
    df_analisis = pd.read_csv("datos_roi_perfectos.csv")

    # Forzamos a que mantenga el orden estricto en el que vino de Colab
    st.header("Eficiencia Real de Marketing")

    # Definimos el tamaño de la figura tradicional (cuadrada y alta para los productos)
    fig, ax = plt.subplots(figsize=(10, 12))
    sns.set_theme(style="whitegrid")

    # Graficamos directamente sin recalcular nada
    sns.barplot(
        data=df_analisis, x="ROI_Marketing", y="producto", palette="viridis"
    )

    plt.title(
        "Eficiencia Real: Ventas generadas por cada Peso invertido en Marketing",
        fontsize=14,
        fontweight="bold",
    )
    plt.xlabel("Multiplicador de Retorno (Ventas / Marketing)", fontsize=12)
    plt.ylabel("Producto", fontsize=12)
    plt.tight_layout()

    # Lo mostramos de forma limpia
    st.pyplot(fig)

else:
    st.warning(
        "⚠️ Por favor, sube el archivo 'datos_roi_perfectos.csv' a tu repositorio de GitHub para activar el gráfico."
    )

