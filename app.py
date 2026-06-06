import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Markdown

# 1. Tus cálculos de cuartiles y límites
q1 = df_q['vtas_productos'].quantile(0.25).round(2)
q2 = df_q ['vtas_productos'].quantile(0.50).round(2)
q3 = df_q ['vtas_productos'].quantile(0.75).round(2)
v_min = round(df_q['vtas_productos'].min(), 2)
v_max = round(df_q['vtas_productos'].max(), 2)
limites = (v_min, q1, q2, q3, v_max)

display(Markdown(f"""
### **Límites de los intervalos:**
* **Mínimo (v_min):** {v_min}
* **Primer Cuartil (q1):** {q1}
* **Mediana (q2):** {q2}
* **Tercer Cuartil (q3):** {q3}
* **Máximo (v_max):** {v_max}
"""))

# Cálculos del IQR y límite superior de atípicos (QRI)
q1_p, q3_p = df_q["vtas_productos"].quantile([0.25, 0.75]).round(2)
iqr_p = q3_p - q1_p
QRI = q3_p + (1.5 * iqr_p)

# Aca comienza el codigo para visualizar grafico( lo anterior es solo para referenciar al lector)

# 2. Configuración y creación del gráfico de bigotes
plt.figure(figsize=(10, 4))
sns.set_theme(style="whitegrid")

# Dibujamos el boxplot
sns.boxplot(x=df_q['vtas_productos'], color="skyblue", flierprops={"markerfacecolor": "red", "marker": "o"})

# Dibujamos una línea roja punteada en el límite QRI para identificar atípicos
plt.axvline(QRI, color='red', linestyle='--', linewidth=2, label=f'Límite Atípicos (QRI): {QRI:.2f}')

# Títulos y etiquetas
plt.title('Distribución de Ventas (Gráfico de Cajas y Bigotes)', fontsize=14, pad=15)
plt.xlabel('vtas_productos', fontsize=12)
plt.legend()

# Mostramos el gráfico
plt.show()
