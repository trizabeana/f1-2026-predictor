import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timezone
from data import testing_data

st.set_page_config(
    page_title="F1 2026 Season Predictor",
    page_icon="F1",
    layout="wide"
)

# ── TEAM COLORS ──
TEAM_COLORS = {
    "Ferrari": "#E8002D",
    "Mercedes": "#27F4D2",
    "McLaren": "#FF8000",
    "Red Bull": "#3671C6",
    "Williams": "#64C4FF",
    "Racing Bulls": "#6692FF",
    "Haas": "#999999",
    "Alpine": "#FF87BC",
    "Audi": "#C22B30",
    "Aston Martin": "#229971",
    "Cadillac": "#AAAAAA",
}

# ── CUSTOM CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: #141414;
}

[data-testid="stHeader"] {
    background: #141414;
}

.hero {
    background: #1c1c1c;
    border: 1px solid #2e2e2e;
    padding: 56px 48px 40px 48px;
    margin-bottom: 0px;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #E8002D, #FF8000, #27F4D2);
}

.hero-eyebrow {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #E8002D;
    margin-bottom: 16px;
}

.hero-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 64px;
    font-weight: 800;
    line-height: 1;
    color: #ffffff;
    text-transform: uppercase;
    letter-spacing: -1px;
    margin-bottom: 24px;
}

.hero-title span {
    color: #E8002D;
}

.hero-body {
    font-size: 15px;
    font-weight: 300;
    line-height: 1.75;
    color: #aaaaaa;
    max-width: 720px;
    margin-bottom: 0;
}

.countdown-wrap {
    background: #1c1c1c;
    border: 1px solid #2e2e2e;
    border-top: none;
    padding: 28px 48px 36px 48px;
    margin-bottom: 48px;
}

.countdown-block {
    display: inline-flex;
    gap: 32px;
    background: #242424;
    border: 1px solid #333;
    padding: 20px 32px;
}

.countdown-unit {
    text-align: center;
}

.countdown-number {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 48px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
}

.countdown-label {
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #666;
    margin-top: 4px;
}

.countdown-divider {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 40px;
    font-weight: 300;
    color: #444;
    align-self: center;
    padding-bottom: 8px;
}

.countdown-caption {
    font-size: 11px;
    color: #555;
    margin-top: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.section-header {
    margin: 48px 0 8px 0;
}

.section-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 28px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #ffffff;
    margin-bottom: 4px;
}

.section-desc {
    font-size: 14px;
    font-weight: 300;
    color: #888;
    line-height: 1.7;
    max-width: 680px;
    margin-bottom: 20px;
}

.podium-card {
    padding: 28px 24px;
    border-top: 3px solid;
    background: #1c1c1c;
    border-left: 1px solid #2e2e2e;
    border-right: 1px solid #2e2e2e;
    border-bottom: 1px solid #2e2e2e;
    height: 100%;
}

.podium-position {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.podium-team {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 36px;
    font-weight: 800;
    text-transform: uppercase;
    line-height: 1;
    margin-bottom: 8px;
}

.podium-drivers {
    font-size: 13px;
    font-weight: 400;
    color: #888;
    margin-bottom: 20px;
}

.podium-score-label {
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #555;
    margin-bottom: 4px;
}

.podium-score {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 48px;
    font-weight: 700;
    line-height: 1;
}

.methodology-box {
    background: #1c1c1c;
    border: 1px solid #2e2e2e;
    border-left: 3px solid #E8002D;
    padding: 20px 24px;
    margin-bottom: 28px;
    font-size: 13px;
    font-weight: 300;
    color: #888;
    line-height: 1.8;
}

.methodology-box strong {
    color: #ccc;
    font-weight: 500;
}

.disclaimer {
    font-size: 12px;
    color: #555;
    border-top: 1px solid #2a2a2a;
    padding-top: 24px;
    margin-top: 48px;
    line-height: 1.9;
}
</style>
""", unsafe_allow_html=True)

# ── COUNTDOWN ──
gp_date = datetime(2026, 3, 8, 4, 0, 0, tzinfo=timezone.utc)
now = datetime.now(timezone.utc)
delta = gp_date - now
days = max(delta.days, 0)
hours, remainder = divmod(max(int(delta.total_seconds()), 0), 3600)
hours = hours % 24
minutes = remainder // 60

# ── HERO ──
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">2026 Formula 1 Season — Round 1</div>
    <div class="hero-title">Australian GP<br><span>Predictor</span></div>
    <div class="hero-body">
        Formula 1 enters a new regulatory era in 2026 — entirely new chassis rules, new power units,
        and eleven teams with radically different cars. Before a single race lap has been run,
        the only available evidence is pre-season testing: six days across two sessions in Bahrain
        in February.<br><br>
        This dashboard distills that evidence into a structured competitiveness model. It does not
        predict race outcomes with certainty — no model can. What it does is translate observable
        testing signals into a ranked assessment of which teams arrived in Melbourne best prepared,
        and which face the sharpest questions going into the season opener.
    </div>
</div>
""", unsafe_allow_html=True)

# ── COUNTDOWN — separate block ──
if delta.total_seconds() > 0:
    st.markdown(f"""
    <div class="countdown-wrap">
        <div class="countdown-block">
            <div class="countdown-unit">
                <div class="countdown-number">{days}</div>
                <div class="countdown-label">Days</div>
            </div>
            <div class="countdown-divider">:</div>
            <div class="countdown-unit">
                <div class="countdown-number">{hours:02d}</div>
                <div class="countdown-label">Hours</div>
            </div>
            <div class="countdown-divider">:</div>
            <div class="countdown-unit">
                <div class="countdown-number">{minutes:02d}</div>
                <div class="countdown-label">Minutes</div>
            </div>
        </div>
        <div class="countdown-caption">Until race start — Albert Park, Melbourne — March 8, 2026</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="countdown-wrap">
        <div class="countdown-block">
            <div class="countdown-unit">
                <div class="countdown-number" style="color:#27F4D2;">LIVE</div>
                <div class="countdown-label">Race Day</div>
            </div>
        </div>
        <div class="countdown-caption">The race is underway — check back for results vs predictions</div>
    </div>
    """, unsafe_allow_html=True)

# ── BUILD DATAFRAME ──
df = pd.DataFrame(testing_data)
df['drivers_str'] = df['drivers'].apply(lambda x: ' & '.join(x))
df['reliability_score'] = df['reliability'].map({'excellent': 100, 'good': 75, 'average': 50, 'poor': 25})
df['color'] = df['team'].map(TEAM_COLORS)

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

PLOT_BG = '#1c1c1c'
PAPER_BG = '#141414'
GRID_COLOR = '#2a2a2a'
FONT_COLOR = '#aaa'

# ── PODIUM ──
st.markdown("""
<div class="section-header">
    <div class="section-title">Predicted Podium</div>
    <div class="section-desc">
        The three teams the model identifies as most likely to compete at the front in Melbourne,
        based on the combined competitiveness score described below.
    </div>
</div>
""", unsafe_allow_html=True)

podium = df.head(3)
positions = ["1st Place", "2nd Place", "3rd Place"]
col1, col2, col3 = st.columns(3)

for col, (_, row), pos in zip([col1, col2, col3], podium.iterrows(), positions):
    with col:
        color = TEAM_COLORS.get(row['team'], '#888')
        st.markdown(f"""
        <div class="podium-card" style="border-top-color: {color};">
            <div class="podium-position" style="color: {color};">{pos}</div>
            <div class="podium-team" style="color: {color};">{row['team']}</div>
            <div class="podium-drivers">{row['drivers_str']}</div>
            <div class="podium-score-label">Competitiveness Score</div>
            <div class="podium-score" style="color: {color};">{row['score']}</div>
        </div>
        """, unsafe_allow_html=True)

# ── COMPETITIVENESS SCORE ──
st.markdown("""
<div class="section-header" style="margin-top:48px;">
    <div class="section-title">Competitiveness Score</div>
    <div class="section-desc">
        A single composite index ranking each team's readiness for the Australian GP.
        It is not a lap time prediction — it is a preparation signal.
    </div>
</div>
<div class="methodology-box">
    <strong>How the score is calculated:</strong> Three testing variables are each normalised
    to a 0–100 scale and combined into a weighted index.
    <strong>Pace (40%)</strong> — the team's best recorded lap time relative to the field,
    treating faster as better.
    <strong>Mileage (40%)</strong> — total laps completed across both tests, treating higher
    as a proxy for reliability and setup maturity.
    <strong>Reliability rating (20%)</strong> — a qualitative assessment drawn from engineering
    and journalist reports covering power unit issues, mechanical failures, and unplanned stoppages.
    Teams rated "excellent" experienced no significant reliability problems; teams rated "poor"
    lost substantial running to repeated failures.
</div>
""", unsafe_allow_html=True)

fig1 = go.Figure()
for _, row in df.sort_values('score').iterrows():
    fig1.add_trace(go.Bar(
        x=[row['score']],
        y=[row['team']],
        orientation='h',
        marker_color=TEAM_COLORS.get(row['team'], '#888'),
        text=f"{row['score']}",
        textposition='outside',
        textfont=dict(color='#ccc', size=12),
        name=row['team'],
        hovertemplate=f"<b>{row['team']}</b><br>Score: {row['score']}<br>Drivers: {row['drivers_str']}<br>Fastest: {row['fastest_lap_fmt']}<br>Laps: {row['total_laps']}<extra></extra>"
    ))

fig1.update_layout(
    showlegend=False,
    height=480,
    plot_bgcolor=PLOT_BG,
    paper_bgcolor=PAPER_BG,
    font=dict(color=FONT_COLOR, family='Barlow Condensed'),
    xaxis=dict(gridcolor=GRID_COLOR, color='#666'),
    yaxis=dict(gridcolor=GRID_COLOR, color='#ccc'),
    margin=dict(l=0, r=60, t=20, b=20),
)
st.plotly_chart(fig1, use_container_width=True)

# ── RELIABILITY ──
st.markdown("""
<div class="section-header">
    <div class="section-title">Mileage — Total Laps Completed</div>
    <div class="section-desc">
        Lap count across both Bahrain tests is one of the most reliable testing signals available.
        Teams with high mileage have more data on tyre behaviour, fuel load sensitivity,
        and mechanical durability. Teams with low mileage — whether through choice or failure —
        arrive in Melbourne with fewer answers.
    </div>
</div>
""", unsafe_allow_html=True)

fig2 = go.Figure()
for _, row in df.sort_values('total_laps').iterrows():
    fig2.add_trace(go.Bar(
        x=[row['total_laps']],
        y=[row['team']],
        orientation='h',
        marker_color=TEAM_COLORS.get(row['team'], '#888'),
        text=str(row['total_laps']),
        textposition='outside',
        textfont=dict(color='#ccc', size=12),
        showlegend=False
    ))

fig2.update_layout(
    height=480,
    plot_bgcolor=PLOT_BG,
    paper_bgcolor=PAPER_BG,
    font=dict(color=FONT_COLOR, family='Barlow Condensed'),
    xaxis=dict(gridcolor=GRID_COLOR, color='#666', title='Laps'),
    yaxis=dict(gridcolor=GRID_COLOR, color='#ccc'),
    margin=dict(l=0, r=60, t=20, b=20),
)
st.plotly_chart(fig2, use_container_width=True)

# ── PACE ──
st.markdown("""
<div class="section-header">
    <div class="section-title">Raw Pace — Fastest Lap</div>
    <div class="section-desc">
        The fastest lap each team recorded during testing. This number should be read carefully:
        teams run different fuel loads, tyre compounds, and engine modes. A faster lap time does
        not guarantee race-day pace advantage. It is one signal among several, weighted accordingly
        in the model. The axis is compressed to reflect the real gaps — all cars finished within
        six seconds of each other.
    </div>
</div>
""", unsafe_allow_html=True)

fig3 = go.Figure()
for _, row in df.sort_values('fastest_lap').iterrows():
    fig3.add_trace(go.Bar(
        x=[row['team']],
        y=[row['fastest_lap']],
        marker_color=TEAM_COLORS.get(row['team'], '#888'),
        text=row['fastest_lap_fmt'],
        textposition='outside',
        textfont=dict(color='#ccc', size=11),
        showlegend=False
    ))

min_lap = df['fastest_lap'].min()
max_lap = df['fastest_lap'].max()

fig3.update_layout(
    height=450,
    plot_bgcolor=PLOT_BG,
    paper_bgcolor=PAPER_BG,
    font=dict(color=FONT_COLOR, family='Barlow Condensed'),
    xaxis=dict(gridcolor=GRID_COLOR, color='#ccc'),
    yaxis=dict(
        gridcolor=GRID_COLOR,
        color='#666',
        range=[min_lap - 1.0, max_lap + 1.5],
        title='Lap time (seconds)',
        tickformat='.1f'
    ),
    margin=dict(l=0, r=20, t=20, b=20),
)
st.plotly_chart(fig3, use_container_width=True)

# ── WEEK 1 vs WEEK 2 ──
st.markdown("""
<div class="section-header">
    <div class="section-title">Testing Trajectory — Week 1 vs Week 2</div>
    <div class="section-desc">
        Comparing mileage between the first and second Bahrain tests reveals development momentum.
        A team that increased lap count in Week 2 resolved early problems and built confidence.
        A team that regressed — or barely ran — carries unresolved questions into the season opener.
    </div>
</div>
""", unsafe_allow_html=True)

fig4 = go.Figure()
for _, row in df.iterrows():
    color = TEAM_COLORS.get(row['team'], '#888')
    fig4.add_trace(go.Bar(
        name=row['team'] + ' — Week 1',
        x=[row['team']],
        y=[row['week1_laps']],
        marker_color=color,
        opacity=0.4,
        showlegend=False
    ))
    fig4.add_trace(go.Bar(
        name=row['team'] + ' — Week 2',
        x=[row['team']],
        y=[row['week2_laps']],
        marker_color=color,
        showlegend=False
    ))

fig4.update_layout(
    barmode='group',
    height=450,
    plot_bgcolor=PLOT_BG,
    paper_bgcolor=PAPER_BG,
    font=dict(color=FONT_COLOR, family='Barlow Condensed'),
    xaxis=dict(gridcolor=GRID_COLOR, color='#ccc', tickangle=-30),
    yaxis=dict(gridcolor=GRID_COLOR, color='#666', title='Laps'),
    margin=dict(l=0, r=20, t=40, b=60),
    annotations=[dict(
        text="Faded = Week 1     Solid = Week 2",
        x=0.5, y=1.06, xref='paper', yref='paper',
        showarrow=False, font=dict(size=11, color='#666')
    )]
)
st.plotly_chart(fig4, use_container_width=True)

# ── TABLE ──
st.markdown("""
<div class="section-header">
    <div class="section-title">Full Data Table</div>
    <div class="section-desc">Complete testing data used as input to the model.</div>
</div>
""", unsafe_allow_html=True)

table = df[['rank', 'team', 'drivers_str', 'fastest_lap_fmt', 'total_laps', 'reliability', 'score', 'notes']].copy()
table.columns = ['Rank', 'Team', 'Drivers', 'Fastest Lap', 'Total Laps', 'Reliability', 'Score', 'Notes']
st.dataframe(table, use_container_width=True, hide_index=True)

