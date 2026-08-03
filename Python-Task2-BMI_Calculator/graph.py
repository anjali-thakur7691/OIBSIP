"""Visual analytics for saved BMI data."""
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


class BMIGraph:
    def show_graph(self, records):
        if not records:
            st.info("Save some BMI records to view analytics.")
            return
        columns = ["ID", "Name", "Age", "Gender", "Weight", "Height", "BMI", "Category", "Date"]
        df = pd.DataFrame(records, columns=columns).sort_values("ID")
        a, b, c = st.columns(3)
        a.metric("Measurements", len(df))
        b.metric("Average BMI", f"{df.BMI.mean():.2f}")
        c.metric("Highest BMI", f"{df.BMI.max():.2f}")
        palette = {"Underweight": "#3B82F6", "Normal": "#16A34A", "Overweight": "#F59E0B", "Obese": "#DC2626"}
        left, right = st.columns(2)
        with left:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(range(len(df)), df.BMI, color=[palette.get(x, "#64748B") for x in df.Category])
            ax.axhspan(18.5, 24.9, alpha=.15, color="#16A34A", label="Healthy BMI range")
            ax.set_xticks(range(len(df)), df.Name, rotation=35, ha="right")
            ax.set_ylabel("BMI"); ax.legend(); fig.tight_layout(); st.pyplot(fig, clear_figure=True)
        with right:
            counts = df.Category.value_counts()
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.pie(counts, labels=counts.index, autopct="%1.0f%%", colors=[palette.get(x, "#64748B") for x in counts.index])
            ax.set_title("Category distribution"); st.pyplot(fig, clear_figure=True)
        st.subheader("BMI trend")
        st.line_chart(df.set_index("Date")["BMI"])
