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
            
        # --- NUEVA SECCIÓN: TABLA DE PRODUCTOS ATÍPICOS ---
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
            st.info("No hay filas para mostrar ya que ningún registro supera el límite estadístico de {QRI:,.2f}.")
            
    else:
        st.warning("⚠️ No hay datos disponibles para el análisis QRI.")
