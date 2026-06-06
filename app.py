import matplotlib.pyplot as plt
import seaborn as sns




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
