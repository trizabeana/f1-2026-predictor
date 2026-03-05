F1 2026 Season Predictor
A data-driven competitiveness model built to forecast team performance ahead of the 2026 Australian Grand Prix. The project uses pre-season testing data — the only empirical evidence available before the season begins — to rank all eleven teams by their likely readiness for the opening race at Albert Park.
Live app: f1-2026-predictor.streamlit.app

Context
Formula 1 enters a new regulatory era in 2026. Entirely new chassis rules, revised aerodynamic regulations, and new hybrid power unit specifications mean every team has built a car from scratch. There is no performance data to carry over from previous seasons.
The only observable evidence before Race 1 is pre-season testing: two sessions held in Bahrain in February, totalling six days of running across all eleven teams. This project treats that data as a signal and builds a structured model around it.

Methodology
The model combines three testing variables into a single weighted competitiveness score per team.
Pace (40%) — each team's fastest recorded lap time across both test sessions, normalised relative to the full field. Faster is better, but this metric is treated with caution: teams run different fuel loads, tyre compounds, and power unit modes during testing, so raw lap times are not a direct proxy for race pace.
Mileage (40%) — total laps completed across both sessions. High mileage indicates reliability, setup maturity, and the accumulation of engineering data. A team that ran 300 laps understands their car significantly better than one that managed 80.
Reliability rating (20%) — a qualitative signal derived from engineering reports and specialist journalism, covering power unit failures, mechanical stoppages, and unplanned interruptions. Rated on a four-point scale: excellent, good, average, poor.
Each variable is normalised to a 0-100 scale before weighting. The final score is the weighted sum of all three.

Data Sources
FastF1 API timing data for 2026 pre-season testing was not publicly available at the time of publication. F1 teams do not release official sector or lap time data during testing sessions.
All data reflects the state of testing as reported at the conclusion of the second Bahrain session.

Tech Stack
LayerToolLanguagePython 3.13Web frameworkStreamlitData processingPandasVisualisationPlotlyDependency managementpip / venv

Running Locally
Clone the repository and set up a virtual environment:
bashgit clone https://github.com/trizabeana/f1-2026-predictor.git
cd f1-2026-predictor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Run the app:
bashstreamlit run app.py
The app will open at http://localhost:8501.

Project Structure
f1-2026-predictor/
├── app.py              # Streamlit application and visualisations
├── data.py             # Testing data for all 11 teams
├── requirements.txt    # Python dependencies
└── README.md


Author
Ana Beatriz Carrione 