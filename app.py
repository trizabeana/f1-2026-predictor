import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data import testing_data

st.set_page_config(
    page_title="F1 2026 Season Predictor",
    page_icon="🏎️",
    layout="wide"
)

st.title("🏎️ F1 2026 Season Predictor")
st.markdown("### Pre-Season Testing Analysis — Australian GP Preview")
st.info("📌 Data sourced from official testing reports (The Race, PlanetF1, RacingNews365) as FastF1 API timing data for 2026 testing is not yet publicly available.")
st.markdown("---")

# Build DataFrame
df = pd.DataFrame(testing_data)
df['drivers_str'] = df['drivers'].apply(lambda x: ' & '.join(x))
df['reliability_score'] = df['reliability'].map({'excellent': 100, 'good': 75, 'average': 50, 'poor': 25})

def normalize(series, ascending=True):
    if series.max() == series.min():
        return series * 0
    if ascending:
        return (series - series.min()) / (series.max() - series.min()) * 100
    else:
        return (series.max() - series) / (series.max() - series.min()) * 100

df['pace_score'] = normalize(df['fastest_lap'], ascending=False)
df['laps_score'] = normalize(df['total_laps'], ascending=True)
df['score'] = (df['pace_score'] * 0.4 + df['laps_score'] * 0.4 + df['reliability_score'] * 0.2).round(1)
df = df.sort_values('score', ascending=False).reset_index(drop=True)
df['rank'] = df.index + 1

def fmt_lap(s):
    return f"{int(s//60)}:{s%60:06.3f}"

df['fastest_lap_fmt'] = df['fastest_lap'].apply(fmt_lap)

# ── SCORE GERAL ──
st.markdown("## 🏆 Predicted Competitiveness — Australian GP 2026")
st.markdown("*Weighted model: 40% pace · 40% reliability (laps) · 20% reliability rating*")

colors = {'excellent': '#00C851', 'good': '#33b5e5', 'average': '#ffbb33', 'poor': '#ff4444'}
df['color'] = df['reliability'].map(colors)

fig1 = px.bar(
    df,
    x='score',
    y='team',
    orientation='h',
    color='reliability',
    color_discrete_map=colors,
    text='score',
    title='🏆 Competitiveness Score — 2026 Australian GP Prediction',
    hover_data={'drivers_str': True, 'fastest_lap_fmt': True, 'total_laps': True, 'notes': True}
)
fig1.update_layout(
    height=500,
    yaxis={'categoryorder': 'total ascending'},
    legend_title='Reliability'
)
fig1.update_traces(textposition='outside')
st.plotly_chart(fig1, use_container_width=True)

# ── VOLTAS ──
st.markdown("## 📊 Reliability — Total Laps Completed")
st.markdown("*More laps = more data, more setup knowledge, better prepared*")

fig2 = px.bar(
    df.sort_values('total_laps'),
    x='total_laps',
    y='team',
    orientation='h',
    color='total_laps',
    color_continuous_scale='RdYlGn',
    text='total_laps',
    title='Total Laps — 2026 Pre-Season Testing (Both Tests Combined)'
)
fig2.update_layout(height=500, showlegend=False)
fig2.update_traces(textposition='outside')
st.plotly_chart(fig2, use_container_width=True)

# ── PACE ──
st.markdown("## ⚡ Raw Pace — Fastest Lap per Team")
st.markdown("*⚠️ Indicative only — fuel loads and tyre compounds vary between teams*")

fig3 = px.bar(
    df.sort_values('fastest_lap', ascending=False),
    x='team',
    y='fastest_lap',
    color='fastest_lap',
    color_continuous_scale='RdYlGn_r',
    text='fastest_lap_fmt',
    title='Fastest Lap Time — 2026 Pre-Season Testing'
)
fig3.update_layout(height=450, showlegend=False)
fig3.update_traces(textposition='outside')
st.plotly_chart(fig3, use_container_width=True)

# ── WEEK 1 vs WEEK 2 ──
st.markdown("## 📈 Progress — Week 1 vs Week 2 Laps")
st.markdown("*Teams that improved mileage in Week 2 show better development trajectory*")

fig4 = go.Figure()
fig4.add_trace(go.Bar(name='Week 1', x=df['team'], y=df['week1_laps'], marker_color='#33b5e5'))
fig4.add_trace(go.Bar(name='Week 2', x=df['team'], y=df['week2_laps'], marker_color='#00C851'))
fig4.update_layout(
    barmode='group',
    title='Laps by Week — Testing Progress',
    height=450,
    xaxis_tickangle=-30
)
st.plotly_chart(fig4, use_container_width=True)

# ── TABELA ──
st.markdown("## 📋 Full Rankings")
table = df[['rank', 'team', 'drivers_str', 'fastest_lap_fmt', 'total_laps', 'reliability', 'score', 'notes']].copy()
table.columns = ['#', 'Team', 'Drivers', 'Fastest Lap', 'Total Laps', 'Reliability', 'Score', 'Notes']
st.dataframe(table, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("⚠️ This is a predictive model based on pre-season testing data. Results may vary significantly in race conditions.")
st.caption("📊 Data: The Race · PlanetF1 · RacingNews365 · Crash.net | FastF1 API timing data for 2026 testing not yet available.")
st.caption("🔧 Built with Python · Pandas · Plotly · Streamlit")