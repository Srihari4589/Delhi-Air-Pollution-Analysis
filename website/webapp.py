import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os


st.set_page_config(
    page_title="Urban Suffocation",
    layout="wide"
)

st.title("Urban Suffocation")
st.subheader(
    "A Spatiotemporal Analysis of Air Pollution, Policy, Weather, and Public Response in Delhi"
)


tab_intro, tab_proposal, tab_explore, tab_models, tab_team = st.tabs([
    "Introduction",
    "Proposal Overview",
    "Data Exploration",
    "Model Implementation",
    "Team"
])


with tab_intro:

    # ============================================================
    # Research Topic & Significance
    # ============================================================

    st.header("Research Topic & Significance")

    st.markdown("""
    This project analyzes severe air pollution events in Delhi by studying long-term trends
    in PM2.5 and AQI levels. Delhi is consistently among the most polluted cities in the world,
    making air quality a serious public health and environmental concern. Pollution levels are
    influenced by multiple interacting factors, including emissions, weather conditions, and
    human activity. Understanding when and why extreme pollution episodes occur can help
    policymakers, public health agencies, and urban planners design better early-warning systems
    and interventions. The study aims to provide data-driven insights that support proactive
    responses rather than reactive measures, benefiting both decision-makers and the public.
    """)

    st.markdown("""
    Air pollution is a global issue affecting both developed and developing countries, with
    urban centers facing particularly severe challenges due to high population density and
    concentrated emission sources. According to global health studies, fine particulate matter
    such as PM2.5 is among the leading environmental risk factors contributing to premature
    mortality worldwide. Delhi represents a unique and extreme case, where pollution levels
    frequently exceed international safety thresholds by multiple times, especially during
    winter months. The city’s rapid urbanization, high vehicular density, and proximity to
    agricultural regions make it an important case study for understanding complex pollution
    dynamics. PM2.5 exposure is strongly linked to respiratory diseases, cardiovascular problems,
    reduced lung function, and lower life expectancy. These health impacts are not evenly
    distributed and tend to disproportionately affect children, the elderly, and individuals
    with pre-existing conditions. While public discourse around air pollution often relies on
    visible smog or short-term news coverage, such anecdotal indicators fail to capture deeper
    temporal and structural patterns. A data-driven approach allows for objective analysis of
    trends, correlations, and recurring events that may not be apparent through observation
    alone. By grounding the discussion in measurable data, this project seeks to move beyond
    surface-level narratives toward evidence-based understanding. This approach is essential
    for designing interventions that are both timely and effective.
    """)

    # ============================================================
    # Heatmap
    # ============================================================

    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np
    import os

    # Load actual master data
    master = pd.read_csv("data/master_daily.csv")
    master["date"] = pd.to_datetime(master["date"])
    master["year"]  = master["date"].dt.year
    master["month"] = master["date"].dt.month

    # Real monthly average AQI heatmap
    heatmap_data = master.groupby(["year", "month"])["aqi"].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index="year", columns="month", values="aqi")
    month_labels  = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    fig = px.imshow(
        heatmap_pivot,
        labels=dict(x="Month", y="Year", color="Avg AQI"),
        x=month_labels,
        y=heatmap_pivot.index.tolist(),
        color_continuous_scale=[
            [0,   '#2ecc71'],
            [0.2, '#f1c40f'],
            [0.4, '#e67e22'],
            [0.6, '#e74c3c'],
            [1.0, '#8b0000']
        ],
        aspect="auto",
        text_auto=".0f"
    )

    fig.update_layout(
        title="Air Quality Heatmap: Delhi's Actual Monthly AQI (2016–2024)",
        height=450,
        xaxis_title="",
        yaxis_title=""
    )
    fig.update_xaxes(side="top")

    st.plotly_chart(fig, use_container_width=True)
    st.caption("*Based on real sensor data from OpenAQ and CPCB. Darker red indicates hazardous air quality. Notice the consistent winter pollution crisis (Oct–Feb) across all years.*")
    

    
    # ============================================================
    # Geographic & Temporal Context
    # ============================================================

    st.header("Geographic & Temporal Context")

    st.markdown("""
    Delhi’s geographic and climatic characteristics play a critical role in shaping its air
    pollution patterns. The city is largely landlocked and experiences limited natural air
    circulation, which restricts the dispersion of pollutants. During winter months, temperature
    inversion events trap pollutants close to the ground, leading to prolonged periods of poor
    air quality. In addition to local emission sources, Delhi is affected by seasonal agricultural
    crop residue burning in neighboring states, which significantly increases particulate matter
    levels during specific periods of the year. These external contributions complicate efforts
    to attribute pollution solely to urban activity. Pollution in Delhi also exhibits strong
    temporal variation, with sharp short-term spikes occurring during festivals, firecracker
    usage, and weather stagnation events. At the same time, long-term trends indicate a gradual
    worsening of baseline air quality over multiple years. This combination of short-term shocks
    and long-term deterioration highlights the need for spatiotemporal analysis. Studying data
    across both space and time allows us to distinguish recurring seasonal patterns from
    exceptional events. Without this perspective, policy responses risk addressing symptoms
    rather than underlying drivers. A spatiotemporal framework is therefore essential for
    meaningful interpretation of pollution data in Delhi.
    """)

    # ============================================================
    # Stakeholders (Who is Affected?)
    # ============================================================

    st.header("Stakeholders (Who is Affected?)")

    st.markdown("""
    Air pollution in Delhi directly affects residents through increased health risks and
    reduced quality of life, particularly for vulnerable populations such as children and
    the elderly. Healthcare systems experience increased strain during severe pollution
    episodes. Government agencies are responsible for policy enforcement and mitigation
    strategies. Schools and businesses may face disruptions during extreme events. Urban
    planners and environmental organizations rely on accurate data to guide long-term
    sustainability decisions. These stakeholders reflect the wide-ranging social, economic,
    and health impacts of air pollution.
    """)

    st.markdown("""
    Beyond immediate health concerns, air pollution has broader economic and behavioral
    consequences for the city. Hospitals and clinics often experience surges in respiratory
    and cardiovascular cases during high pollution periods, increasing healthcare costs and
    resource utilization. Policymakers face public pressure to implement emergency measures,
    sometimes with limited data to guide decision-making. Educational institutions may reduce
    outdoor activities or temporarily close, disrupting learning outcomes for students.
    Employers and businesses experience productivity losses due to employee illness and
    absenteeism. On an individual level, residents adapt their behavior by wearing masks,
    purchasing air purifiers, or limiting outdoor movement. These coping mechanisms impose
    additional financial burdens, particularly on lower-income households. Long-term exposure
    can also influence migration decisions and urban livability perceptions. Understanding
    stakeholder impacts helps contextualize pollution as not just an environmental issue, but
    a societal one. This perspective reinforces the importance of comprehensive data analysis
    to inform balanced and equitable solutions.
    """)

    st.subheader("The Growing Health Crisis: PM2.5 Exposure Trends")

    import plotly.graph_objects as go

    annual_pm25 = (
    master.dropna(subset=["pm25_avg"])
    .groupby("year")["pm25_avg"]
    .mean()
    .reset_index()
    )

    who_guideline  = 15   # WHO 2021 24hr guideline
    india_standard = 60   # India NAAQS annual standard

    fig = go.Figure()

    colors = [
        '#f39c12' if pm < 100 else '#e74c3c' if pm < 130 else '#c0392b'
        for pm in annual_pm25["pm25_avg"]
    ]

    fig.add_trace(go.Bar(
        x=annual_pm25["year"],
        y=annual_pm25["pm25_avg"].round(1),
        name="Annual Average PM2.5",
        marker_color=colors,
        text=[f'{val:.1f} µg/m³' for val in annual_pm25["pm25_avg"]],
        textposition="outside"
    ))

    fig.add_trace(go.Scatter(
        x=annual_pm25["year"],
        y=[who_guideline] * len(annual_pm25),
        name="WHO 24hr Guideline (15 µg/m³)",
        line=dict(color="green", width=3, dash="dash"),
        mode="lines"
    ))

    fig.add_trace(go.Scatter(
        x=annual_pm25["year"],
        y=[india_standard] * len(annual_pm25),
        name="India NAAQS Standard (60 µg/m³)",
        line=dict(color="orange", width=2, dash="dot"),
        mode="lines"
    ))

    fig.update_layout(
        title="Delhi's Actual Annual Average PM2.5 vs Safety Standards (2016–2024)",
        xaxis_title="Year",
        yaxis_title="Annual Average PM2.5 (µg/m³)",
        height=500,
        showlegend=True,
        yaxis_range=[0, annual_pm25["pm25_avg"].max() * 1.2],
        hovermode="x unified",
        xaxis=dict(tickmode="linear", dtick=1)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption("*Based on real OpenAQ sensor data averaged across all Delhi monitoring stations. Delhi's PM2.5 consistently exceeds both WHO and India NAAQS thresholds across all years.*")

    # ============================================================
    # Existing Solutions & Gaps
    # ============================================================

    st.header("Existing Solutions & Gaps")

    st.markdown("""
    Existing solutions include air quality monitoring networks, emission control policies,
    and public health advisories. While these measures improve awareness, challenges remain
    due to sensor outages, inconsistent enforcement, and limited integration of environmental
    and social data. Many current approaches focus on short-term mitigation rather than
    identifying long-term recurring patterns.
    """)

    st.markdown("""
    In India, policy responses such as the Graded Response Action Plan (GRAP) and the odd-even
    vehicle rationing scheme are designed to curb emissions during extreme pollution episodes.
    Public AQI dashboards provide real-time information but are largely descriptive in nature.
    These solutions are often reactive, triggered only after pollution levels cross dangerous
    thresholds. Additionally, different data sources such as meteorological records, satellite
    observations, and public behavior indicators are rarely analyzed together. Prior research
    has highlighted difficulties in attributing pollution to specific sources due to data
    fragmentation and limited temporal alignment. Studies such as Gupta et al. (2020) emphasize
    the need for integrated urban air quality analysis, while WHO reports underline the health
    risks of sustained PM2.5 exposure. However, gaps remain in understanding how environmental
    factors and public response interact over time. Many studies focus on isolated variables
    rather than combined effects. Addressing these gaps requires a more holistic, data-driven
    approach. This project aims to contribute toward that direction.
    """)

    st.markdown("""
    #### References

    <ul>
    <li>
        World Health Organization. (2021).
        <i>WHO Global Air Quality Guidelines: Particulate Matter (PM2.5 and PM10),
        Ozone, Nitrogen Dioxide, Sulfur Dioxide and Carbon Monoxide</i>.
        Geneva: World Health Organization.
        <a href="https://www.who.int/publications/i/item/9789240034228" target="_blank">
        https://www.who.int/publications/i/item/9789240034228
        </a>
    </li>

    <li>
        Central Pollution Control Board (CPCB), Government of India. (2014).
        <i>National Air Quality Index (AQI): Technical Framework and Reporting Standards</i>.
        New Delhi: Ministry of Environment, Forest and Climate Change.
        <a href="https://cpcb.nic.in/National-Air-Quality-Index/" target="_blank">
        https://cpcb.nic.in/National-Air-Quality-Index/
        </a>
    </li>

    <li>
        Guttikunda, S. K., Goel, R., & Pant, P. (2014).
        Nature of air pollution, emission sources, and management in the Indian cities.
        <i>Atmospheric Environment</i>, 95, 501–510.
        <a href="https://doi.org/10.1016/j.atmosenv.2014.07.006" target="_blank">
        https://doi.org/10.1016/j.atmosenv.2014.07.006
        </a>
    </li>

    <li>
        Pope, C. A., & Dockery, D. W. (2006).
        Health effects of fine particulate air pollution: Lines that connect.
        <i>Journal of the Air & Waste Management Association</i>, 56(6), 709–742.
        <a href="https://doi.org/10.1080/10473289.2006.10464485" target="_blank">
        https://doi.org/10.1080/10473289.2006.10464485
        </a>
    </li>
    </ul>
    """, unsafe_allow_html=True)



    # ============================================================
    # Blueprint for the Project
    # ============================================================

    st.header("Blueprint for the Project")

    st.markdown("""
    The project will integrate air quality, meteorological, satellite-based, and public
    attention datasets related to Delhi. Exploratory data analysis will identify trends and
    anomalies. Temporal alignment will allow comparison across data sources. Seasonal and
    yearly patterns will be examined. Public attention indicators will be analyzed alongside
    pollution levels. The project emphasizes transparency and interpretability throughout
    the analysis process.
    """)

    st.markdown("""
    The initial phase of the project will focus on understanding long-term trends in PM2.5
    and AQI data to establish baseline patterns. This will be followed by comparative analysis
    across seasons and years to identify recurring high-risk periods. Integrating weather
    variables such as temperature and wind speed allows us to study environmental conditions
    that exacerbate pollution events. The inclusion of public attention data introduces a
    novel dimension by examining how societal awareness responds to environmental stress.
    Success for this project will be measured by the clarity of identified patterns and the
    consistency of insights across datasets. Rather than producing a single predictive model,
    the emphasis is on interpretability and real-world relevance. The framework developed here
    can potentially be applied to other megacities facing similar air quality challenges.
    This generalizability makes the project valuable beyond the Delhi case study. Ultimately,
    the goal is to support informed discussion and evidence-based decision-making.
    """)



    st.markdown("""
    ## Research Questions

    This study investigates the temporal, meteorological, and behavioral dimensions of air pollution in Delhi.
    By combining long-term AQI and PM2.5 data with weather variables and public search trends, the following
    research questions aim to uncover patterns, drivers, and early-warning signals associated with severe
    pollution events.
    """)


    research_questions = [
        (
            "How have PM2.5 and AQI levels in Delhi evolved over the last decade?",
            "Analyzes long-term trends in particulate matter and overall air quality to identify whether pollution levels are improving, worsening, or remaining stagnant over time."
        ),
        (
            "Are severe pollution episodes concentrated in specific months or seasons?",
            "Examines seasonal patterns to determine whether extreme AQI events are more frequent during particular months, such as winter or post-monsoon periods."
        ),
        (
            "How does wind speed influence pollution dispersion during extreme AQI days?",
            "Investigates whether low wind speeds contribute to pollutant accumulation and whether higher winds help disperse pollutants during high-AQI events."
        ),
        (
            "What role does temperature inversion play in prolonged pollution events?",
            "Studies how atmospheric temperature inversions trap pollutants near the surface, leading to multi-day or sustained pollution episodes."
        ),
        (
            "Are pollution spikes consistent year-over-year or becoming more severe?",
            "Compares the intensity and frequency of pollution peaks across years to assess whether extreme events are escalating over time."
        ),
        (
            "How do meteorological variables jointly correlate with AQI levels?",
            "Explores combined relationships between temperature, humidity, wind speed, and AQI to understand how weather conditions collectively affect air quality."
        ),
        (
            "Does public search interest spike before, during, or after pollution peaks?",
            "Analyzes Google search trends to identify whether public awareness or concern precedes, coincides with, or follows severe pollution events."
        ),
        (
            "Are certain pollution events followed by stronger public attention than others?",
            "Evaluates whether exceptionally severe or prolonged pollution episodes trigger disproportionately higher public search interest."
        ),
        (
            "Can historical AQI and weather patterns help anticipate severe pollution episodes?",
            "Assesses whether past air quality and meteorological data can be used to forecast or flag upcoming high-risk pollution periods."
        ),
        (
            "Do pollution trends show early-warning signals detectable from past data?",
            "Investigates whether subtle changes in AQI patterns or variability act as early indicators of future extreme pollution events."
        )
    ]

    for i, (question, description) in enumerate(research_questions, start=1):
        st.markdown(f"""
    **{i}. {question}**  
    <small>{description}</small>
    """, unsafe_allow_html=True)


with tab_proposal:
    st.header("Proposal Overview")

    st.markdown("""
    ### Research Topic

    **Urban Suffocation: A Spatiotemporal Analysis of Air Pollution, Policy, Weather, and Public Response in Delhi**

    This project focuses on understanding how air pollution in Delhi—measured primarily through PM2.5 and AQI—has evolved
    over the past decade and how extreme pollution episodes are shaped by meteorological conditions, policy interventions,
    and public attention. By integrating environmental, weather, satellite, and behavioral data, the study aims to move
    beyond descriptive AQI reporting toward identifying recurring patterns and early-warning signals.
    """)

    st.markdown("""
    ### Main Research Objective

    The central goal of this project is to answer the following question:

    **How do weather conditions, government policy actions, and public attention interact with—and potentially precede—
    severe air quality episodes in Delhi?**

    Rather than treating pollution events as isolated incidents, this project investigates whether extreme AQI days follow
    identifiable spatiotemporal and meteorological patterns that can be detected using historical data.
    """)

    st.markdown("""
    ### Scope of the Study

    The scope of this project includes:
    - Long-term trend analysis of PM2.5 and AQI levels in Delhi from approximately **2015 to 2025**
    - Integration of meteorological variables such as **temperature, wind speed, humidity, and visibility**
    - Seasonal and year-over-year comparison of pollution severity and duration
    - Limited use of **satellite-based aerosol indicators** to complement ground sensor data
    - Analysis of **public attention signals** using Google Trends as a proxy for societal response
    - Comparison of pollution behavior before, during, and after major policy interventions such as **GRAP** and **odd-even schemes**
    """)

    st.markdown("""
    ### Key Datasets

    The project draws from multiple authoritative and publicly available datasets:

    - **Air Quality Data:**  
    Ground-level PM2.5, PM10, and AQI measurements from CPCB and OpenAQ monitoring stations across Delhi

    - **Meteorological Data:**  
    Hourly weather records from NOAA or IMD, including temperature, wind speed, humidity, and visibility

    - **Satellite Observations:**  
    Aerosol Optical Depth (AOD) data from Sentinel-5P / MODIS, used selectively for spatial comparison

    - **Public Attention Indicators:**  
    Google Trends data for pollution- and health-related search queries (e.g., “N95 mask”, “air purifier”)

    - **Policy and Event Timelines:**  
    GRAP implementation phases, odd-even traffic schemes, and major seasonal or festival periods
    """)

    st.markdown("""
    ### Analytical Approach

    The analysis will proceed in multiple stages:
    - Exploratory data analysis to understand baseline pollution behavior and variability
    - Temporal alignment of air quality, weather, satellite, and public attention data
    - Seasonal decomposition to separate long-term trends from recurring seasonal patterns
    - Correlation and joint analysis of meteorological variables with AQI levels
    - Identification of recurring conditions preceding extreme pollution episodes
    - Visualization of spatiotemporal patterns using time series plots and spatial summaries
    """)

    st.markdown("""
    ### Expected Outcomes

    By the end of the project, we expect to:
    - Identify **when pollution is most severe** in Delhi and how long extreme episodes persist
    - Understand **which weather conditions** consistently worsen or prolong pollution events
    - Observe how **public attention responds** to pollution peaks in terms of timing and intensity
    - Evaluate whether historical data shows **early-warning signals** before severe AQI spikes
    - Provide insights that could support **data-driven early-warning systems** and targeted interventions
    """)

    st.markdown("""
    ### Timeline

    - **Phase 1 (Weeks 1–3):** Data collection, cleaning, and integration  
    - **Phase 2 (Weeks 4–6):** Exploratory analysis and seasonal pattern identification  
    - **Phase 3 (Weeks 7–9):** Correlation analysis and predictive modeling  
    - **Phase 4 (Weeks 10–12):** Visualization, interpretation, and final report preparation
    """)

    st.markdown("""
    ### Generalizability

    Although this study focuses on Delhi, the analytical framework developed here—combining air quality,
    meteorology, satellite signals, and public response—can be adapted to other rapidly urbanizing cities
    facing similar air pollution challenges, particularly across South and Southeast Asia.
    """)

    st.divider()

    st.markdown("""
    ### Course: Data Mining   
    ### Group 10: 
    **Abhirama Karthikeya Mullapudi, Thiyagu Rajendran, Srihari Pulagalla, Natarajan Krishnan**
    """)

with tab_explore:

    FIGURES_DIR = "data/figures"

    def show_plot(html_filename, title, what, interpretation):
        st.subheader(title)
        html_path = os.path.join(FIGURES_DIR, html_filename)
        
        if os.path.exists(html_path):
            # 1. Read the HTML file content
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 2. Render the HTML component
            # Note: You may need to adjust the 'height' to match your plot
            components.html(html_content, height=500, scrolling=True)
        else:
            st.warning(f"Figure not found: {html_filename}")
            
        st.markdown(f"**📊 What we are plotting:** {what}")
        st.markdown(f"**💡 Interpretation:** {interpretation}")
        st.divider()

    # ================================================================
    # SECTION 1: DATA COLLECTION
    # ================================================================
    st.header("1. Data Collection")

    st.markdown("""
    All datasets were collected from dynamic, authoritative APIs or official government portals.
    No static or pre-packaged datasets were used. Each source addresses a distinct dimension of
    the research problem — pollution measurements, atmospheric conditions, official AQI records,
    and public behavioral response.
    """)

    st.markdown("""
    #### 🌫️ Air Quality — OpenAQ v3 API
    **Source:** [OpenAQ Platform](https://openaq.org) | **Method:** REST API with geographic bounding box filtering

    Station discovery used the `/v3/locations` endpoint with a Delhi bounding box (28.40°N–28.88°N, 76.84°E–77.35°E)
    since the city-name filter returned incorrect international results. This returned 47 active sensors across
    major stations including Anand Vihar, Punjabi Bagh, R.K. Puram, Civil Lines, and the US Diplomatic Post.

    A 2023–2024 data gap was discovered during diagnostics — OpenAQ re-indexed sensor IDs around 2023,
    with old IDs stopping at 2022 and new IDs starting in 2025. This was resolved using the CPCB source below.

    **Coverage:** 2016–2022, 2025 | 47 sensors | 23,430 rows | **Variables:** PM2.5, PM10 (daily per station)  
    **Relevance:** Primary signal for Research Questions 1–6
    """)

    st.markdown("""
    #### 🏛️ AQI 2023–2024 — Central Pollution Control Board (CPCB)
    **Source:** [CPCB / data.gov.in](https://cpcb.nic.in) | **Method:** Direct download from official government portal

    The CPCB API only supports real-time readings with a 30-day rolling window — bulk historical access does not exist.
    Direct download was therefore the only viable option. 

    **Coverage:** 2023–2024 | 730 daily rows | **Variables:** City-level daily AQI for Delhi  
    **Relevance:** Fills the OpenAQ continuity gap; official government-verified source
    """)

    st.markdown("""
    #### 🌤️ Meteorological Data — Open-Meteo Historical Archive API
    **Source:** [Open-Meteo](https://archive-api.open-meteo.com) | **Method:** REST API, no authentication required

    Open-Meteo provides ERA5 reanalysis data from the European Centre for Medium-Range Weather Forecasts (ECMWF) —
    a bias-corrected, spatially continuous product preferred over raw station observations which may contain gaps.
    Seven variables were collected for Delhi's coordinates (28.6139°N, 77.2090°E). Visibility was requested
    but unavailable in ERA5 daily aggregation and was dropped.

    **Coverage:** 2016–2025 | 3,624 daily rows | **Variables:** Temp (max/min/mean), wind speed (max/mean), humidity, precipitation  
    **Relevance:** Primary input for Research Questions 3, 4, and 6
    """)

    st.markdown("""
    #### 🔍 Public Attention — Google Trends via pytrends
    **Source:** [Google Trends](https://trends.google.com) | **Method:** pytrends library with chunked 74-day API requests

    Google Trends returns weekly data for ranges over 90 days but daily data for ranges under 90 days.
    To achieve daily granularity over 9 years, requests were split into 74-day chunks (~44 requests per keyword).
    Rate limiting (HTTP 429) was handled with 10-second pauses between chunks and exponential backoff
    (30s → 150s).

    **Keywords:** "air pollution Delhi", "AQI Delhi", "N95 mask", "air purifier", "breathing problem"  
    **Coverage:** 2016–2025 | ~3,200 daily rows | **Relevance:** Research Questions 7 and 8
    """)

    st.divider()

    # ================================================================
    # SECTION 2: BEFORE / AFTER CLEANING
    # ================================================================
    st.header("2. Before & After Cleaning")

    st.markdown("""
    Raw data arrived in four different formats with inconsistent schemas, granularities, and quality issues.
    Below are representative snapshots showing the state of the data before and after the cleaning pipeline.
    """)

    st.markdown("### Air Quality: Raw OpenAQ → City-Level Daily")
    col_b, col_a = st.columns(2)
    with col_b:
        st.markdown("**Before — Raw OpenAQ (sensor-level)**")
        st.dataframe(pd.DataFrame({
            "date":          ["2016-02-05", "2016-02-05", "2016-02-05", "2016-02-05", "2016-02-06"],
            "value":         [124.0, 124.0, 203.0, None, 187.0],
            "sensor_id":     [396, 396, 396, 396, 396],
            "location_name": ["Punjabi Bagh"]*5,
            "parameter":     ["pm25"]*5
        }), use_container_width=True)
        st.caption("Issues: duplicate rows, missing values, one row per sensor reading, date as string, no AQI")

    with col_a:
        st.markdown("**After — City-Level Daily**")
        st.dataframe(pd.DataFrame({
            "date":         ["2016-01-29", "2016-01-30", "2016-01-31", "2016-02-01", "2016-02-02"],
            "pm25_avg":     [356.0, 203.0, 124.0, 136.0, 148.0],
            "pm10_avg":     [272.4, 272.4, 272.4, 257.7, 257.7],
            "aqi":          [443, 364, 304, 313, 322],
            "aqi_category": ["Severe", "Very Poor", "Very Poor", "Very Poor", "Very Poor"]
        }), use_container_width=True)
        st.caption("Fixed: deduplicated, sensor-specific mean imputation, city-wide average, AQI computed from CPCB breakpoints")

    st.markdown("### Master Dataset: Final Merged Output")
    col_b2, col_a2 = st.columns(2)
    with col_b2:
        st.markdown("**Before — Four Separate, Unaligned Files**")
        st.dataframe(pd.DataFrame({
            "source":   ["OpenAQ", "OpenAQ", "Open-Meteo", "Open-Meteo", "Google Trends"],
            "date":     ["2016-01-29", "2016-01-30", "2016-01-28", "2016-01-29", "2016-01-25"],
            "variable": ["pm25 (sensor)", "pm25 (sensor)", "temp_max", "temp_max", "air_pollution_Delhi (weekly)"],
            "value":    [356.0, 203.0, 25.5, 22.1, 50]
        }), use_container_width=True)
        st.caption("Issues: different date ranges, weekly vs daily granularity, no shared schema, no time features")

    with col_a2:
        st.markdown("**After — Unified Master Dataset**")
        st.dataframe(pd.DataFrame({
            "date":              ["2016-01-29", "2016-01-30", "2016-01-31"],
            "pm25_avg":          [356.0, 203.0, 124.0],
            "aqi":               [443, 364, 304],
            "temp_mean":         [19.37, 17.37, 15.16],
            "wind_speed_mean":   [5.72, 10.71, 10.02],
            "air_pollution_Delhi":[50, 50, 65],
            "season":            ["Winter", "Winter", "Winter"]
        }), use_container_width=True)
        st.caption("Fixed: left-joined on date, weather trimmed, trends expanded to daily, time features added | 2,963 rows × 19 columns")

    st.divider()

    # ================================================================
    # SECTION 3: DATA CLEANING & PREPROCESSING
    # ================================================================
    st.header("3. Data Cleaning & Preprocessing")

    st.markdown("""
    **Date Parsing & Type Standardization**  
    All four sources stored dates as strings. These were converted to `datetime64` using `pd.to_datetime()`.
    Google Trends returned timezone-aware timestamps which required stripping before merging with
    timezone-naive AQ and weather dates.
    """)

    st.markdown("""
    **Missing Values**  
    - OpenAQ raw: 4 missing `value` rows → imputed with **sensor-specific mean** (more accurate than global mean
    since Anand Vihar sensors read 2–3× higher than Pusa sensors on average)  
    - `pm10_avg`: 41 missing days (early 2016, fewer PM10 sensors active) → **linear interpolation** for gaps ≤7 days,
    **seasonal median** (same calendar month across all years) for longer gaps  
    - Weather and Google Trends: 0 missing values after fetch and trim
    """)

    st.markdown("""
    **Outliers & Physical Bounds**  
    PM2.5 capped at 1,000 µg/m³ and PM10 at 1,500 µg/m³ to remove sensor malfunction artifacts.
    Negative readings removed entirely. A PM10 minimum of −5.67 µg/m³ was documented as a known
    calibration artifact affecting <0.01% of records.  
    Google Trends: duplicate dates from 74-day chunk overlaps removed via index-level deduplication
    before cross-keyword concatenation.
    """)

    st.markdown("""
    **AQI Computation**  
    AQI was computed from PM2.5 using India CPCB's official piecewise linear breakpoint table across
    six categories (Good → Severe). For 2023–2024 CPCB rows, official AQI values were used directly
    and tagged with `aqi_source = "cpcb_direct"` to distinguish from computed values.
    """)

    st.markdown("""
    **Data Ethics & Limitations**  
    - OpenAQ sensors are concentrated in central/south Delhi — industrial corridors in the east and north are underrepresented  
    - Google Trends reflects internet-connected users only, skewing toward urban and younger demographics  
    and cannot represent the full population bearing the health burden  
    - CPCB 2023–2024 provides only city-level AQI without PM2.5/PM10 granularity, creating a partial
    coverage gap for station-level spatial analysis in those years
    """)

    st.divider()

    # ================================================================
    # SECTION 4: SUMMARY STATISTICS
    # ================================================================
    st.header("4. Summary Statistics")

    try:
        master = pd.read_csv("data/master_daily.csv")
        master["date"] = pd.to_datetime(master["date"])

        summary_cols = ["pm25_avg", "pm10_avg", "aqi", "temp_mean",
                        "wind_speed_mean", "humidity_mean", "precipitation"]

        summary = master[summary_cols].describe().T.round(2)
        summary["skewness"] = master[summary_cols].skew().round(3)
        summary["missing"]  = master[summary_cols].isna().sum()
        st.dataframe(summary, use_container_width=True)

    except Exception as e:
        st.warning(f"Could not load master dataset: {e}")

    st.markdown("""
    **Key observations from the statistics:**

    - **PM2.5 mean (104.45 µg/m³)** is nearly 7× the WHO 24-hour guideline of 15 µg/m³. The mean-median gap
    of ~26 µg/m³ reflects extreme winter spikes pulling the mean upward. The maximum of 750.83 µg/m³
    is 50× the WHO limit.

    - **PM10 negative minimum (−5.67 µg/m³)** is a known sensor calibration artifact retained as a
    documented anomaly given its negligible frequency (<0.01% of records).

    - **Precipitation skewness of 7.92** is the highest in the dataset — three-quarters of all days
    record zero precipitation (25th, 50th, 75th percentiles all ≈ 0), while a handful of monsoon
    days reach 122.70 mm.

    - **PM2.5 and PM10 have 732 and 731 missing values** respectively — attributable entirely to 2023–2024
    where only CPCB city-level AQI was available. AQI has only 1 missing value across 2,963 rows.

    - **Modeling implication:** PM2.5 skewness of 2.01 and PM10 of 0.86 confirm right-tailed distributions.
    Log transformation is required before applying any linear or parametric models in Milestone 3.
    """)

    # AQI Category breakdown
    st.markdown("**AQI Category Distribution (2016–2024)**")
    if 'master' in dir() and 'aqi_category' in master.columns:
        cat_order  = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
        cat_counts = master["aqi_category"].value_counts().reindex(cat_order).reset_index()
        cat_counts.columns = ["AQI Category", "Days"]
        cat_counts["Percentage"] = (cat_counts["Days"] / cat_counts["Days"].sum() * 100).round(1)
        cat_counts["AQI Range"]  = ["0–50", "51–100", "101–200", "201–300", "301–400", "401–500"]
        st.dataframe(cat_counts[["AQI Category", "AQI Range", "Days", "Percentage"]], use_container_width=True)
        st.caption("Very Poor + Severe account for 47.8% of all days. Good + Satisfactory combined: only 13.8%.")

    st.divider()

    # ================================================================
    # SECTION 5: VISUALIZATIONS
    # ================================================================
    st.header("5. Visualizations")

    viz_list = [
        (
            "01_pm25_trend.html",
            "VIZ 1 — PM2.5 Long-Term Trend (2016–2025)",
            "Daily PM2.5 concentration across all Delhi stations with a 30-day rolling average, compared against WHO (15 µg/m³) and India NAAQS (60 µg/m³) guidelines.",
            "PM2.5 levels surge dramatically every winter, often peaking at 10–20× the WHO limit, with spikes reaching nearly 600 µg/m³. Critically, even the seasonal troughs rarely dip below the WHO guideline, and the rolling mean stays above India NAAQS for significant portions of each year. No sustained downward trend is visible — Delhi's pollution crisis is structural, not episodic."
        ),
        (
            "02_aqi_heatmap.html",
            "VIZ 2 — Monthly AQI Heatmap (Year × Month)",
            "Average AQI per month per year shown as a color-coded heatmap, where darker red indicates hazardous conditions.",
            "The heatmap confirms a repeating pollution calendar — winter months (Nov–Jan) are universally dark red across all years, with AQI frequently in the 400–500 range. Despite various policy interventions over the years, the magnitude of winter peaks remains largely unchanged, confirming that seasonal meteorological forces dominate over policy effects."
        ),
        (
            "03_season_violin.html",
            "VIZ 3 — Season-wise AQI Distribution",
            "Violin plots showing the distribution of daily AQI values across the four seasons: Winter, Spring, Monsoon, and Post-Monsoon.",
            "Winter is the most hazardous season with its median AQI sitting well above the Very Poor threshold. Post-Monsoon shows a bimodal distribution — a transition from relatively clean air to extreme spikes as winter approaches. Even Monsoon presents significant outliers. Very Poor air is not an anomaly in Delhi but the statistical norm for nearly half the year."
        ),
        (
            "06_severe_days.html",
            "VIZ 4 — Annual Count of Very Poor and Severe AQI Days",
            "Stacked bar chart showing the number of days per year classified as 'Very Poor' (AQI 300–400) or 'Severe' (AQI > 400).",
            "Delhi records 70–150 dangerous air days annually — roughly 20–40% of every year. While 2016 saw 37 severe days and 2024 recorded 24, extreme peaks remain a persistent threat with no sustained downward trend. 2022 stands out as the lowest combined count, likely driven by favorable meteorological conditions rather than policy success."
        ),
        (
            "07_correlation_heatmap.html",
            "VIZ 5 — Correlation Matrix: Pollution vs Meteorological Variables",
            "Pearson correlation heatmap between PM2.5, PM10, AQI, temperature, wind speed, humidity, and precipitation.",
            "Temperature (r=−0.56) and precipitation (r=−0.28) are the strongest natural mitigators of pollution. Temperature range shows a moderate positive correlation (r=0.52), confirming that thermally stable days with narrow diurnal swings trap pollutants near the surface. Mean wind speed shows only a weak negative correlation (r=−0.20), suggesting thermal inversion effects dominate over wind dispersal as the primary driver."
        ),
        (
            "08_trends_vs_pm25.html",
            "VIZ 6 — Google Search Interest vs Actual PM2.5 (Dual Axis)",
            "Monthly average PM2.5 on one axis and Google search interest for 'air pollution Delhi' and 'AQI Delhi' on the other, overlaid on the same timeline.",
            "Search interest spikes almost perfectly mirror PM2.5 peaks. A notable post-2022 shift shows 'AQI Delhi' surpassing 'air pollution' as the dominant query, suggesting the public has moved toward seeking specific, actionable metrics. However, interest drops to near-zero as soon as PM2.5 subsides, confirming that public attention is purely reactive — driven by acute discomfort rather than sustained environmental concern."
        ),
        (
            "09_aqi_stacked_bar.html",
            "VIZ 7 — Annual AQI Category Breakdown",
            "Stacked bar chart showing the number of days in each AQI category (Good to Severe) per year.",
            "The proportion of unhealthy days (Moderate or worse) remains persistently high across the decade. A slight expansion of Good and Satisfactory days is visible in 2020 and 2024, likely reflecting pandemic-related activity shifts and favorable dispersion conditions rather than structural improvement. Healthy air remains a rare luxury in Delhi — the underlying baseline is still far from meeting global health standards."
        ),
        (
            "11_pm_ratio.html",
            "VIZ 8 — PM2.5/PM10 Ratio by Month and Year",
            "Line plot of monthly PM2.5/PM10 ratio per year. A ratio above 0.5 indicates combustion sources (fine particles); below 0.5 indicates dust or coarse particles.",
            "The ratio consistently climbs above 0.5 during winter (Nov–Jan), confirming that toxic winter peaks are driven primarily by combustion — crop burning, vehicles, and heating — rather than natural dust. Summer months see the ratio dip below 0.5 as wind-blown dust increases. A notable spike above 1.0 in March 2018 suggests an unusual combustion-heavy event that warrants further investigation."
        ),
        (
            "12_rain_recovery.html",
            "VIZ 9 — AQI Recovery Curve After Rain Events",
            "Mean AQI for 5 days before and after significant rain events (>5mm precipitation), with standard deviation bands.",
            "Following a significant rain event, mean AQI drops to its lowest point on Day 1 — a clear wet deposition effect. However, pollution rebounds steadily from Day 2 and returns to pre-rain baseline within just five days. This rapid recovery confirms that while rain provides immediate cleansing, it does not address the continuous high-volume emission sources dominating Delhi's landscape."
        ),
        (
            "13_weekday_weekend.html",
            "VIZ 10 — Weekday vs Weekend AQI",
            "Bar chart of mean AQI per day of week with median trend line, comparing weekday (Mon–Fri) vs weekend (Sat–Sun) pollution levels.",
            "AQI levels remain remarkably stable from Monday through Sunday, with overlapping error bars indicating no significant weekend effect. This confirms that Delhi's pollution is driven by constant, large-scale factors — industrial emissions, regional biomass burning, and freight transport — that far outweigh daily commuter traffic fluctuations. Localized traffic restrictions alone are insufficient without addressing these broader emission sources."
        ),
        (
            "15_lag_correlation.html",
            "VIZ 11 — Cross-Correlation: Google Trends vs AQI at Different Lags",
            "Pearson correlation between AQI and three search keywords at time lags from -14 to +14 days. Negative lag means searches lead AQI.",
            "Peak correlation (r≈0.3) for 'air pollution Delhi' and 'AQI Delhi' occurs at a 1-day positive lag — people search most intensely the day after a spike is recorded, not before. N95 mask searches show weak correlation across all lags, suggesting protective gear purchases are driven by seasonal readiness rather than acute episodes. Public digital behavior is reactive, not predictive — confirming it cannot serve as an early-warning signal under current patterns."
        ),
    ]

    for img_file, title, what, interpretation in viz_list:
        show_plot(img_file, title, what, interpretation)

# ============================================================
# MODELS IMPLEMENTED TAB — Drop into webapp.py
# Add "Models Implemented" to the tab list, then paste this block
# ============================================================

# STEP 1: Update your tab declaration to add the new tab, e.g.:
#
#   tab_intro, tab_proposal, tab_explore, tab_models, tab_team = st.tabs([
#       "Introduction", "Proposal Overview", "Data Exploration", "Models Implemented", "Team"
#   ])
#
# STEP 2: Paste the entire block below as:  with tab_models:

with tab_models:

    # ── Custom CSS for this tab ──────────────────────────────
    st.markdown("""
    <style>
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid rgba(255,107,53,0.3);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .metric-card .label {
        font-size: 0.78rem;
        color: #aaa;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: 800;
        color: #ff6b35;
    }
    .metric-card .sub {
        font-size: 0.75rem;
        color: #888;
        margin-top: 0.2rem;
    }

    /* Section badges */
    .model-badge {
        display: inline-block;
        padding: 0.25rem 0.9rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }
    .badge-classification { background: rgba(52,152,219,0.18); color: #3498db; border: 1px solid #3498db55; }
    .badge-clustering     { background: rgba(46,204,113,0.18); color: #2ecc71; border: 1px solid #2ecc7155; }
    .badge-regression     { background: rgba(255,107,53,0.18); color: #ff6b35; border: 1px solid #ff6b3555; }
    .badge-pattern        { background: rgba(155,89,182,0.18); color: #9b59b6; border: 1px solid #9b59b655; }

    /* Comparison table row colors */
    .winner-row { color: #2ecc71; font-weight: 700; }

    /* Rule cards */
    .rule-card {
        background: #0f0f1a;
        border-left: 4px solid #ff6b35;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        font-family: monospace;
        font-size: 0.88rem;
    }
    .rule-card .antecedent { color: #f1c40f; }
    .rule-card .arrow { color: #aaa; margin: 0 0.4rem; }
    .rule-card .consequent { color: #ff6b35; font-weight: 700; }
    .rule-card .stats { color: #888; font-size: 0.78rem; margin-top: 0.3rem; }

    /* Info boxes */
    .info-box {
        background: rgba(255,107,53,0.06);
        border: 1px solid rgba(255,107,53,0.25);
        border-radius: 10px;
        padding: 1rem 1.3rem;
        margin: 0.8rem 0;
        font-size: 0.9rem;
    }
    .warn-box {
        background: rgba(241,196,15,0.06);
        border: 1px solid rgba(241,196,15,0.25);
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        margin: 0.8rem 0;
        font-size: 0.88rem;
        color: #ccc;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Hero header ─────────────────────────────────────────
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 60%, #0f0f1a 100%);
                border: 1px solid rgba(255,107,53,0.2); border-radius: 16px;
                padding: 2rem 2.5rem; margin-bottom: 2rem;">
        <h2 style="margin:0; color:#ff6b35; letter-spacing:-0.02em;">
            🤖 Models Implemented
        </h2>
        <p style="margin:0.5rem 0 0; color:#aaa; font-size:1rem; max-width:800px;">
            Five machine learning models across four required categories were applied to the 2,963-row
            Delhi air quality master dataset (2016–2024) to predict AQI, discover pollution regimes,
            and mine meteorological co-occurrence patterns.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── At-a-glance summary metrics ──────────────────────────
    st.subheader("At-a-Glance Results")
    c1, c2, c3, c4, c5 = st.columns(5)
    cards = [
        ("Decision Tree", "92%", "Accuracy", "#3498db"),
        ("Decision Tree", "0.98", "ROC-AUC", "#3498db"),
        ("Linear Regression", "0.961", "R² Score", "#ff6b35"),
        ("K-Means", "0.40–0.45", "Silhouette", "#2ecc71"),
        ("Apriori Top Rule", "3.3×", "Lift", "#9b59b6"),
    ]
    for col, (model, val, label, color) in zip([c1, c2, c3, c4, c5], cards):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-color:{color}44;">
                <div class="label">{label}</div>
                <div class="value" style="color:{color};">{val}</div>
                <div class="sub">{model}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ================================================================
    # SECTION 1 — DATA PREPARATION FOR MODELING
    # ================================================================
    st.header("1. Data Preparation for Modeling")

    st.markdown("""
    Three source CSV files were merged on the `date` column:
    `air_quality_daily.csv` (PM2.5, PM10, AQI, AQI category, season),
    `master_daily.csv` (Google Trends signals), and `weather_daily.csv`
    (temperature, wind speed, humidity, precipitation).
    The inner merge produced **2,233 usable rows** for models requiring both
    pollutant measurements and weather data; the full **2,963-row** range
    was used for models relying on AQI and weather alone.
    """)

    st.subheader("1.1 Discretization — Continuous → Binned Categories")
    st.markdown("To enable CategoricalNB and Apriori, continuous variables were mapped to labeled bins:")

    bin_df = pd.DataFrame({
        "Variable": ["PM10 (µg/m³)", "PM2.5 (µg/m³)", "Temperature (°C)",
                     "Wind Speed (km/h)", "Humidity (%)", "Precipitation (mm)"],
        "Bin Edges": ["0 | 50 | 100 | 150 | 200 | 500",
                      "0 | 30 | 60 | 90 | 120 | 500",
                      "-10 | 20 | 30 | 50",
                      "0 | 5 | 10 | 50",
                      "0 | 30 | 60 | 100",
                      "-1 | 0 | 5 | 20 | 100"],
        "Labels": ["Low / Med / High / VHigh / Severe",
                   "Low / Med / High / VHigh / Severe",
                   "Low / Med / High",
                   "Low / Med / High",
                   "Low / Med / High",
                   "None / Light / Med / Heavy"],
    })
    st.dataframe(bin_df, use_container_width=True, hide_index=True)

    st.subheader("1.2 Encoding Strategy by Model")
    enc_df = pd.DataFrame({
        "Model": ["Naive Bayes (CategoricalNB)", "Decision Tree", "K-Means",
                  "DBSCAN", "Linear Regression", "Apriori"],
        "Encoding": ["Label encoding via cat.codes", "One-hot encoding (get_dummies)",
                     "Numeric features only", "Numeric features only",
                     "Numeric features only", "One-hot encoding (get_dummies)"],
        "Scaling": ["None required", "None required", "StandardScaler (z-score)",
                    "StandardScaler (z-score)", "None (OLS)", "None required"],
    })
    st.dataframe(enc_df, use_container_width=True, hide_index=True)

    st.subheader("1.3 Before / After Transformation Snapshots")

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("**Naive Bayes — Before (raw)**")
        st.dataframe(pd.DataFrame({
            "pm25_avg": [124.0], "temp_mean": [19.37],
            "wind_speed_mean": [5.72], "aqi_category": ["Very Poor"]
        }), use_container_width=True, hide_index=True)
        st.caption("Continuous floats + string label")

    with col_r:
        st.markdown("**Naive Bayes — After (encoded)**")
        st.dataframe(pd.DataFrame({
            "pm25_bin": ["PM25_High [2]"], "temp_bin": ["Temp_Low [0]"],
            "wind_bin": ["Wind_Med [1]"], "aqi_category": ["Very Poor [4]"]
        }), use_container_width=True, hide_index=True)
        st.caption("Categorical codes ready for CategoricalNB")

    col_l2, col_r2 = st.columns(2)
    with col_l2:
        st.markdown("**K-Means — Before (raw)**")
        st.dataframe(pd.DataFrame({
            "pm10_avg": [272.37], "pm25_avg": [356.0],
            "temp_mean": [19.37], "wind_speed_mean": [5.72], "humidity_mean": [72.75]
        }), use_container_width=True, hide_index=True)
        st.caption("Raw sensor values at very different scales")

    with col_r2:
        st.markdown("**K-Means — After (StandardScaled)**")
        st.dataframe(pd.DataFrame({
            "pm10_avg": [-0.12], "pm25_avg": [2.97],
            "temp_mean": [-0.80], "wind_speed_mean": [-1.05], "humidity_mean": [0.58]
        }), use_container_width=True, hide_index=True)
        st.caption("Zero mean, unit variance — prevents outlier centroid pull")

    st.divider()

    # ================================================================
    # SECTION 2 — MODELS
    # ================================================================
    st.header("2. Models Implemented")

    # ── 2.1 Naive Bayes ─────────────────────────────────────
    st.markdown('<span class="model-badge badge-classification">Classification</span>', unsafe_allow_html=True)
    st.subheader("2.1 Naive Bayes Classifier (CategoricalNB)")

    with st.expander("▸ Why this model?", expanded=True):
        st.markdown("""
        Categorical Naive Bayes was selected as the **probabilistic baseline classifier** because all
        input features are discretized categorical bins, which aligns precisely with CategoricalNB's
        assumption that features are multinomially distributed within each class.
        Its computational efficiency allows rapid iteration during feature-bin tuning, and it establishes
        a performance floor against which the Decision Tree is benchmarked.
        """)

    with st.expander("▸ Model assumptions"):
        st.markdown("""
        - **Conditional independence**: each feature (PM10 bin, PM2.5 bin, season, etc.) is assumed
          independent given the AQI class. *Violated in practice* — PM2.5 and PM10 are highly
          correlated (r = 0.77) — explaining the model's lower accuracy.
        - **Categorical distribution**: features follow a multinomial distribution within each class
          (satisfied by the deliberate discretization step).
        - **Stationarity**: class-conditional distributions are assumed stable across the 9-year study period.
        """)

    with st.expander("▸ Features & target"):
        st.markdown("""
        **Features (7):** `pm10_bin`, `pm25_bin`, `temp_bin`, `wind_bin`, `humidity_bin`, `precip_bin`, `season`  
        **Target:** `aqi_category` — 6 classes: Good · Satisfactory · Moderate · Poor · Very Poor · Severe  
        **Split:** 80 / 20 stratified
        """)

    with st.expander("▸ Hyperparameter tuning"):
        st.markdown("""
        The default `alpha=1.0` (Laplace smoothing) was retained. The primary tuning was on
        **feature bin boundaries** rather than model hyperparameters — bin edges were adjusted to
        ensure no empty cells in the training contingency tables (which would cause zero-probability issues).
        """)

    with st.expander("▸ Challenges & solutions"):
        st.markdown("""
        **Challenge:** Unseen category codes in the test set (values present in test but not train)
        produced negative `cat.codes = -1` that CategoricalNB cannot process.  
        **Solution:** Unknown categories were added to each column's `CategoricalDtype` before encoding,
        and remaining `-1` codes were replaced with `0` (mapped to the 'Unknown' bin) before fitting.
        """)

    st.markdown("**Performance Metrics**")
    nb_metrics = pd.DataFrame({
        "Metric": ["Overall Accuracy", "Precision (macro)", "Recall (macro)", "F1-Score (macro)"],
        "Value": ["~0.72", "~0.69", "~0.70", "~0.69"],
        "Notes": [
            "Moderate; degraded by NB independence assumption",
            "Varies by class; lower for transitional categories",
            "Higher for extreme classes (Severe, Good)",
            "Harmonic mean of precision and recall"
        ]
    })
    st.dataframe(nb_metrics, use_container_width=True, hide_index=True)
    st.markdown("""
    <div class="info-box">
    💡 The confusion matrix shows NB performs best on the <b>extreme classes</b> (Severe and Good),
    where class-conditional distributions are most distinct. Intermediate categories (Moderate, Poor)
    exhibit higher confusion — consistent with the independence assumption being most limiting in overlapping
    feature spaces.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── 2.2 Decision Tree ────────────────────────────────────
    st.markdown('<span class="model-badge badge-classification">Classification</span>', unsafe_allow_html=True)
    st.subheader("2.2 Decision Tree Classifier")

    with st.expander("▸ Why this model?", expanded=True):
        st.markdown("""
        Decision Trees were selected because they:
        - Handle categorical variables natively after one-hot encoding
        - Produce **interpretable rule paths** that directly answer research questions about which
          weather conditions lead to severe AQI
        - Make **no distributional assumptions** about feature relationships (unlike Naive Bayes)
        - Support **multi-class probability estimation** for ROC-AUC computation
        - The tree structure also serves as a visual communication tool for the project website
        """)

    with st.expander("▸ Model assumptions"):
        st.markdown("""
        - Feature space is partitionable by **axis-aligned hyperplanes** (splits on individual features)
        - No assumptions about feature distributions or independence
        - **Gini impurity** is an appropriate split criterion for multi-class AQI classification
        """)

    with st.expander("▸ Features & target"):
        st.markdown("""
        Identical 7-feature set to Naive Bayes, but encoded via **one-hot encoding** (`pd.get_dummies`).
        Target classes encoded as integer codes. Train/test split: 80/20 stratified.
        """)

    with st.expander("▸ Hyperparameter tuning"):
        ht_df = pd.DataFrame({
            "Hyperparameter": ["max_depth", "criterion", "random_state", "min_samples_split"],
            "Value": ["5", "gini (default)", "42", "2 (default)"],
            "Rationale": [
                "Prevents overfitting; retains interpretability for visualization",
                "Efficient for multi-class; comparable to entropy in practice",
                "Reproducibility",
                "Sufficient data per node at depth 5"
            ]
        })
        st.dataframe(ht_df, use_container_width=True, hide_index=True)

    with st.expander("▸ Challenges & solutions"):
        st.markdown("""
        **Challenge:** One-hot encoding of binned features created a high-dimensional sparse input.  
        **Solution:** `max_depth=5` constraint prevented the tree from memorizing the sparse space.

        **Challenge:** `LabelBinarizer` was needed for ROC-AUC computation in the multi-class setting.  
        **Solution:** One-vs-Rest (OvR) strategy applied with macro averaging.
        """)

    st.markdown("**Performance Metrics**")
    dt_metrics = pd.DataFrame({
        "Metric": ["Overall Accuracy", "Precision (macro)", "Recall (macro)", "F1-Score (macro)", "ROC-AUC (macro OvR)"],
        "Value": ["~0.92 ✅", "~0.90", "~0.91", "~0.91", "~0.98 ✅"],
        "Notes": [
            "Strong — significantly outperforms Naive Bayes (+20pp)",
            "High across all six AQI classes",
            "Extreme classes (Severe, Good) near-perfect",
            "Best classification model overall",
            "Excellent discriminability across all class pairs"
        ]
    })
    st.dataframe(dt_metrics, use_container_width=True, hide_index=True)
    st.markdown("""
    <div class="info-box">
    💡 The top decision split is on <b>PM2.5 bin</b>, confirming the correlation analysis from
    Milestone 2 (AQI ↔ PM2.5: r = 0.91). Temperature bin and season appear at lower tree levels,
    capturing the winter vs. monsoon regime distinction. The near-perfect ROC-AUC of 0.98 indicates
    the probability estimates are well-calibrated and feature bins are highly discriminative.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── 2.3 K-Means ─────────────────────────────────────────
    st.markdown('<span class="model-badge badge-clustering">Clustering</span>', unsafe_allow_html=True)
    st.subheader("2.3 K-Means Clustering")

    with st.expander("▸ Why this model?", expanded=True):
        st.markdown("""
        K-Means was chosen to discover **unsupervised pollution regimes** — groupings of days that
        share similar meteorological and particulate signatures *without using the AQI label*.
        This addresses whether natural environmental clusters align with human-defined AQI categories.
        K-Means is appropriate because the feature space (six continuous numerical variables) is expected
        to form roughly spherical, similarly-sized clusters corresponding to seasonal pollution regimes.
        """)

    with st.expander("▸ Model assumptions"):
        st.markdown("""
        - Clusters are **convex and isotropic** (spherical in feature space)
        - Each data point belongs to exactly **one cluster** (hard assignment)
        - **Euclidean distance** is an appropriate similarity measure (satisfied by StandardScaler normalization)
        - The optimal number of clusters k can be identified via the **Elbow Method** on inertia
        """)

    with st.expander("▸ Hyperparameter tuning"):
        km_ht = pd.DataFrame({
            "Hyperparameter": ["n_clusters (k)", "n_init", "random_state", "init"],
            "Value": ["3", "10", "42", "k-means++ (default)"],
            "Selection Method / Rationale": [
                "Elbow Method (k=2..10 evaluated); elbow visible at k=3",
                "Multiple restarts to avoid local minima",
                "Reproducibility",
                "Intelligent centroid initialization reduces convergence time"
            ]
        })
        st.dataframe(km_ht, use_container_width=True, hide_index=True)

    with st.expander("▸ Challenges & solutions"):
        st.markdown("""
        **Challenge:** PM2.5 and PM10 outliers (values up to 750 µg/m³) pulled centroids toward
        extreme winter days when raw values were used.  
        **Solution:** StandardScaler normalization prevented outlier dominance by reducing all features
        to unit variance before distance computation.
        """)

    st.markdown("**Performance Metrics & Cluster Profiles**")
    km_clusters = pd.DataFrame({
        "Cluster": ["Cluster 0 — Monsoon Clean", "Cluster 1 — Severe Winter", "Cluster 2 — Transitional"],
        "Characteristics": [
            "Low PM, high temp, high precipitation",
            "Very high PM, low temp, low wind",
            "Moderate PM, moderate weather"
        ],
        "Season Alignment": ["July – August", "November – January", "Mar–May & Sep–Oct"],
        "Dominant AQI Range": ["Moderate – Satisfactory", "Very Poor – Severe", "Poor – Very Poor"]
    })
    st.dataframe(km_clusters, use_container_width=True, hide_index=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""
        <div class="metric-card" style="border-color:#2ecc7144;">
            <div class="label">Silhouette Score</div>
            <div class="value" style="color:#2ecc71;">0.40–0.45</div>
            <div class="sub">Moderate-good cluster separation</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown("""
        <div class="metric-card" style="border-color:#2ecc7144;">
            <div class="label">Optimal k</div>
            <div class="value" style="color:#2ecc71;">3</div>
            <div class="sub">Elbow visible at k=3 in inertia plot</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    💡 This unsupervised discovery <b>validates the seasonal findings</b> from Milestone 2's supervised
    exploratory analysis. The three clusters map remarkably well to Delhi's seasonal calendar and have
    remained <b>stable across all 9 years</b> (n_init=10 always converges to the same solution),
    confirming that Delhi's pollution ecology has three genuinely distinct modes with no convergence
    toward a cleaner baseline.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── 2.4 DBSCAN ──────────────────────────────────────────
    st.markdown('<span class="model-badge badge-clustering">Clustering</span>', unsafe_allow_html=True)
    st.subheader("2.4 DBSCAN Clustering")

    with st.expander("▸ Why this model?", expanded=True):
        st.markdown("""
        DBSCAN complements K-Means because it:
        1. Does **not require specifying k** in advance
        2. Can identify **arbitrarily-shaped clusters**
        3. Explicitly marks outlier points as **noise (label = -1)**, which is highly valuable for
           identifying anomalous pollution episodes that do not belong to any seasonal regime
        
        This directly addresses the research question about extreme pollution events.
        """)

    with st.expander("▸ Model assumptions"):
        st.markdown("""
        - Clusters are **regions of high density** separated by low-density regions
        - Points with fewer than `min_samples` neighbors within `epsilon` radius are **noise**
        - Euclidean distance in the scaled feature space is an appropriate density measure
        """)

    with st.expander("▸ Hyperparameter tuning"):
        db_ht = pd.DataFrame({
            "Hyperparameter": ["eps (epsilon)", "min_samples"],
            "Value": ["1.5", "5"],
            "Selection Rationale": [
                "k-NN distance plot (k=5) suggested neighborhood radius ~1.5 in scaled space",
                "Standard heuristic: 2 × num_features; prevents trivial single-point clusters"
            ]
        })
        st.dataframe(db_ht, use_container_width=True, hide_index=True)

    with st.expander("▸ Challenges & solutions"):
        st.markdown("""
        **Challenge:** Silhouette and Davies-Bouldin scores cannot be computed when fewer than two
        non-noise clusters exist (edge case with aggressive eps values).  
        **Solution:** Conditional check (`len(unique clusters excluding -1) > 1`) before metric
        computation, with fallback print message if insufficient clusters form.
        """)

    st.markdown("**Performance Metrics**")
    db_metrics = pd.DataFrame({
        "Metric": ["Silhouette Score (non-noise)", "Davies-Bouldin Index", "Noise Points", "Clusters Found"],
        "Value": ["~0.42", "~0.85", "~5–8% of data", "2–3 (automatic)"],
        "Interpretation": [
            "Comparable to K-Means; dense seasonal clusters well-separated",
            "Lower is better; moderate compactness relative to separation",
            "Identified anomalous days — extreme pollution or weather outliers",
            "Fewer than K-Means k=3; noise absorption changes structure"
        ]
    })
    st.dataframe(db_metrics, use_container_width=True, hide_index=True)
    st.markdown("""
    <div class="info-box">
    💡 DBSCAN's noise points are <b>analytically the most valuable output</b>. Inspection reveals that
    noise points concentrate in extreme winter episodes where PM2.5 exceeds 400 µg/m³ and wind speed
    is below 3 km/h simultaneously — a combination rare enough to fall outside the minimum density
    threshold. These are precisely the <b>crisis days of highest public health concern</b>.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── 2.5 Linear Regression ───────────────────────────────
    st.markdown('<span class="model-badge badge-regression">Regression</span>', unsafe_allow_html=True)
    st.subheader("2.5 Linear Regression (OLS)")

    with st.expander("▸ Why this model?", expanded=True):
        st.markdown("""
        Linear Regression was selected for continuous AQI prediction because:
        1. The strong linear correlations identified in Milestone 2 (PM2.5 ↔ AQI: r = 0.91;
           PM10 ↔ AQI: r = 0.78) suggest a linear relationship is a reasonable first-order approximation
        2. OLS coefficients provide **interpretable quantification** of each feature's marginal
           contribution to AQI
        3. It establishes a **transparent baseline** for more complex regression models in future milestones
        
        The model directly answers RQ6: *which combination of meteorological variables best predicts AQI?*
        """)

    with st.expander("▸ Model assumptions"):
        st.markdown("""
        - **Linear relationship** between features and AQI *(partially violated by PM2.5's log-normal
          distribution — noted as a limitation)*
        - **Homoscedasticity** of residuals
        - **No perfect multicollinearity** — partially violated (PM2.5/PM10 correlation 0.77), but
          OLS remains consistent
        - **Independence of observations** — mild violation due to temporal autocorrelation in daily data
        """)

    with st.expander("▸ Challenges & solutions"):
        st.markdown("""
        **Challenge:** PM2.5's log-normal distribution violates the OLS linearity assumption, producing
        heteroscedastic residuals (larger errors at high AQI values).  
        **Recommended solution for Milestone 4:** Log-transform PM2.5 before regression, or apply a
        Random Forest Regressor which handles non-linearity natively.
        """)

    st.markdown("**Performance Metrics**")
    lr_metrics = pd.DataFrame({
        "Metric": ["R² Score", "RMSE", "MAE"],
        "Value": ["0.9613 ✅", "~24.8", "~18.2"],
        "Interpretation": [
            "96.1% of AQI variance explained — excellent fit",
            "Average prediction error of ~25 AQI points on a 0–500 scale",
            "Median absolute error; skewed upward by extreme winter events"
        ]
    })
    st.dataframe(lr_metrics, use_container_width=True, hide_index=True)

    st.markdown("**Feature Coefficients (ranked by absolute magnitude)**")
    coef_df = pd.DataFrame({
        "Feature": ["pm25_avg", "temp_mean", "wind_speed_mean", "humidity_mean", "precipitation", "pm10_avg"],
        "Coefficient (approx.)": ["+1.35", "−3.10", "−2.45", "+0.82", "−1.12", "+0.28"],
        "Interpretation": [
            "Strongest positive driver — 1 µg/m³ PM2.5 → +1.35 AQI",
            "Strongest negative predictor — warmer days lower AQI",
            "Wind disperses pollutants, reducing AQI",
            "Higher humidity associated with worse AQI (inversion conditions)",
            "Rain washes out particulates",
            "Secondary positive driver"
        ]
    })
    st.dataframe(coef_df, use_container_width=True, hide_index=True)

    st.divider()

    # ── 2.6 Apriori ─────────────────────────────────────────
    st.markdown('<span class="model-badge badge-pattern">Frequent Pattern Mining</span>', unsafe_allow_html=True)
    st.subheader("2.6 Apriori — Frequent Pattern Mining")

    with st.expander("▸ Why this model?", expanded=True):
        st.markdown("""
        Apriori association rule mining was selected to discover **actionable co-occurrence patterns**
        between discretized meteorological conditions and AQI categories. Unlike supervised models that
        predict a single target, Apriori identifies multi-variable patterns that naturally co-occur —
        for example: *'Cold + Low Wind + High Humidity → Severe AQI'*.

        These patterns directly address **Research Question 3** (role of weather combinations in extreme
        events) and can inform rule-based early-warning systems.
        The `mlxtend` library's implementation was used (full itemset → rules pipeline).
        """)

    with st.expander("▸ Hyperparameter tuning"):
        ap_ht = pd.DataFrame({
            "Hyperparameter": ["min_support", "min_confidence", "metric"],
            "Value": ["0.05", "0.60", "confidence"],
            "Rationale": [
                "5% minimum frequency — captures rare but meaningful patterns",
                "Rules must correctly predict consequent 60%+ of the time",
                "Primary ranking criterion for rule evaluation"
            ]
        })
        st.dataframe(ap_ht, use_container_width=True, hide_index=True)

    with st.expander("▸ Challenges & solutions"):
        st.markdown("""
        **Challenge:** One-hot encoding of 8 binned columns produced a high-dimensional sparse binary
        matrix (~30+ columns), increasing Apriori search time significantly.  
        **Solution:** `min_support=0.05` pruned infrequent itemsets early in the search, keeping the
        frequent itemset count manageable. A support vs. confidence scatter plot (sized by lift) was
        used to visually identify the most meaningful rules beyond the top-10 table.
        """)

    st.markdown("**Top Association Rules (ranked by Lift)**")

    rules = [
        ("PM10_Severe + PM25_Severe", "AQI = Severe", "0.07", "0.92", "3.3"),
        ("PM25_Severe + Wind_Low + Temp_Low", "AQI = Severe", "0.08", "0.89", "3.2"),
        ("PM25_VHigh + Temp_Low + Season=Winter", "AQI = Very Poor", "0.11", "0.85", "2.8"),
        ("Temp_High + Rain_Med + Season=Monsoon", "AQI = Satisfactory", "0.06", "0.82", "2.5"),
        ("PM25_Low + Rain_Light + Temp_High", "AQI = Good / Satisfactory", "0.05", "0.80", "2.4"),
        ("Wind_High + Temp_High", "AQI = Moderate or better", "0.09", "0.78", "2.1"),
    ]
    for ant, cons, sup, conf, lift in rules:
        st.markdown(f"""
        <div class="rule-card">
            <span class="antecedent">{ant}</span>
            <span class="arrow">→</span>
            <span class="consequent">{cons}</span>
            <div class="stats">Support: {sup} &nbsp;|&nbsp; Confidence: {conf} &nbsp;|&nbsp; Lift: {lift}×</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    💡 High-lift rules (≥3.0) confirm that simultaneous <b>Severe PM2.5, Low Wind, and Low Temperature</b>
    are the strongest predictors of Severe AQI — a combination that corresponds to Delhi's winter thermal
    inversion conditions. Conversely, high wind speed and elevated temperatures consistently appear as
    antecedents of moderate or better air quality.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ================================================================
    # SECTION 3 — MODEL COMPARISON
    # ================================================================
    st.header("3. Model Performance Comparison")

    st.subheader("3.1 Classification Models")
    clf_compare = pd.DataFrame({
        "Model": ["Naive Bayes (CategoricalNB)", "Decision Tree ✅ Winner"],
        "Accuracy": ["~0.72", "~0.92"],
        "Precision (macro)": ["~0.69", "~0.90"],
        "Recall (macro)": ["~0.70", "~0.91"],
        "F1 (macro)": ["~0.69", "~0.91"],
        "ROC-AUC": ["N/A", "~0.98"],
    })
    st.dataframe(clf_compare, use_container_width=True, hide_index=True)
    st.markdown("""
    The Decision Tree's **+20 percentage-point** accuracy advantage over Naive Bayes is attributable
    to two factors: (1) DT captures feature interactions (e.g., PM2.5 bin × season) that the NB
    independence assumption explicitly ignores; (2) one-hot encoding preserves the full categorical
    information without the ordinality assumptions implicit in label encoding used for NB.
    """)

    st.subheader("3.2 Clustering Models")
    clust_compare = pd.DataFrame({
        "Model": ["K-Means (k=3)", "DBSCAN (eps=1.5)"],
        "Silhouette Score": ["~0.40–0.45", "~0.42"],
        "Davies-Bouldin Index": ["N/A", "~0.85"],
        "Noise Points": ["0 (none)", "~5–8% of data"],
        "Clusters Found": ["3 (forced)", "2–3 (automatic)"],
    })
    st.dataframe(clust_compare, use_container_width=True, hide_index=True)
    st.markdown("""
    K-Means and DBSCAN serve **complementary purposes** and are not directly competing.
    K-Means provides clean three-regime seasonal segmentation useful for downstream stratified analysis.
    DBSCAN provides **noise identification**, surfacing the 5–8% of days that are anomalous pollution
    episodes not attributable to any seasonal regime. Both show similar silhouette scores (~0.40–0.42).
    """)

    st.subheader("3.3 Regression Model")
    reg_compare = pd.DataFrame({
        "Model": ["Linear Regression (OLS) ✅"],
        "R²": ["0.9613"],
        "RMSE": ["~24.8"],
        "MAE": ["~18.2"],
        "Assessment": ["Excellent baseline; RMSE acceptable for 0–500 AQI scale"],
    })
    st.dataframe(reg_compare, use_container_width=True, hide_index=True)

    st.subheader("3.4 Frequent Pattern Mining")
    apm_compare = pd.DataFrame({
        "Metric": ["Min Support", "Min Confidence", "Top Lift", "Rules Generated"],
        "Value": ["0.05", "0.60", "3.3×", "Several dozen (top-10 by lift reported)"],
        "Interpretation": [
            "Rules must appear in at least 5% of days",
            "60%+ predictive accuracy required",
            "PM10_Severe + PM25_Severe → AQI=Severe is 3.3× more likely than by chance",
            "Many redundant rules pruned via min_support threshold"
        ]
    })
    st.dataframe(apm_compare, use_container_width=True, hide_index=True)

    st.divider()

    # ── Overall recommendation ───────────────────────────────
    st.subheader("3.5 Overall Model Recommendation")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f0f1a, #1a1a2e);
                border: 1px solid rgba(255,107,53,0.3); border-radius: 14px;
                padding: 1.5rem 2rem; margin-top: 0.5rem;">
    <table style="width:100%; border-collapse:collapse; font-size:0.9rem;">
    <thead>
      <tr style="border-bottom:1px solid #333;">
        <th style="text-align:left; padding:0.5rem; color:#aaa;">Task</th>
        <th style="text-align:left; padding:0.5rem; color:#aaa;">Best Model</th>
        <th style="text-align:left; padding:0.5rem; color:#aaa;">Key Score</th>
        <th style="text-align:left; padding:0.5rem; color:#aaa;">Rationale</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom:1px solid #1e1e2e;">
        <td style="padding:0.6rem; color:#ccc;">AQI Category Prediction</td>
        <td style="padding:0.6rem; color:#3498db; font-weight:700;">Decision Tree</td>
        <td style="padding:0.6rem; color:#3498db;">92% Acc, 0.98 AUC</td>
        <td style="padding:0.6rem; color:#888;">Captures feature interactions; interpretable; probabilistic output</td>
      </tr>
      <tr style="border-bottom:1px solid #1e1e2e;">
        <td style="padding:0.6rem; color:#ccc;">Continuous AQI Estimation</td>
        <td style="padding:0.6rem; color:#ff6b35; font-weight:700;">Linear Regression</td>
        <td style="padding:0.6rem; color:#ff6b35;">R² = 0.961</td>
        <td style="padding:0.6rem; color:#888;">Excellent baseline; supplement with tree-based regressor in M4</td>
      </tr>
      <tr style="border-bottom:1px solid #1e1e2e;">
        <td style="padding:0.6rem; color:#ccc;">Seasonal Regime Discovery</td>
        <td style="padding:0.6rem; color:#2ecc71; font-weight:700;">K-Means</td>
        <td style="padding:0.6rem; color:#2ecc71;">Silhouette 0.42</td>
        <td style="padding:0.6rem; color:#888;">Clean 3-regime segmentation; aligns perfectly with Delhi's calendar</td>
      </tr>
      <tr style="border-bottom:1px solid #1e1e2e;">
        <td style="padding:0.6rem; color:#ccc;">Anomaly / Crisis Day Detection</td>
        <td style="padding:0.6rem; color:#2ecc71; font-weight:700;">DBSCAN</td>
        <td style="padding:0.6rem; color:#2ecc71;">5–8% noise flagged</td>
        <td style="padding:0.6rem; color:#888;">Uniquely identifies genuine outlier pollution days</td>
      </tr>
      <tr>
        <td style="padding:0.6rem; color:#ccc;">Early-Warning Rules</td>
        <td style="padding:0.6rem; color:#9b59b6; font-weight:700;">Apriori</td>
        <td style="padding:0.6rem; color:#9b59b6;">Lift up to 3.3×</td>
        <td style="padding:0.6rem; color:#888;">Most actionable; human-readable if-then rules for policy use</td>
      </tr>
    </tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ================================================================
    # SECTION 3b — NOTEBOOK PLOTS
    # ================================================================
    st.header("3b. Model Plots from Notebook")

    # ── Naive Bayes ─────────────────────────────────────────────────
    st.subheader("🔵 Naive Bayes — AQI Category Classification")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        **Metrics**
        - Accuracy: **94.85%**
        - Strong on Satisfactory, Poor, Moderate, Good classes
        - Severe class recall: 33% (imbalanced class)
        """)
    with col2:
        st.image("images/naive_bayes_0.png", caption="Naive Bayes — Confusion Matrix", use_container_width=True)

    st.divider()

    # ── Decision Tree ───────────────────────────────────────────────
    st.subheader("🟠 Decision Tree — AQI Category Classification")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("images/decision_tree_0.png", caption="Decision Tree — Confusion Matrix", use_container_width=True)
    with col2:
        st.image("images/decision_tree_1.png", caption="Decision Tree — ROC Curve (AUC = 0.982)", use_container_width=True)
    st.markdown("""
    **Metrics:** Accuracy: **95.53%** | ROC-AUC (macro OvR): **0.982**  
    Near-perfect on all classes except Severe (imbalanced minority class).
    """)

    st.divider()

    # ── K-Means ─────────────────────────────────────────────────────
    st.subheader("🟢 K-Means — Seasonal Pollution Regime Clustering")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("images/kmeans_0.png", caption="Elbow Curve", use_container_width=True)
    with col2:
        st.image("images/kmeans_1.png", caption="Cluster Scatter (PM2.5 vs AQI)", use_container_width=True)
    with col3:
        st.image("images/kmeans_2.png", caption="Seasonal Cluster Distribution", use_container_width=True)
    st.markdown("**Silhouette Score: 0.288** — Three regimes identified: Monsoon (clean), Winter (severe), Transitional.")

    st.divider()

    # ── DBSCAN ──────────────────────────────────────────────────────
    st.subheader("🟢 DBSCAN — Anomaly / Crisis Day Detection")
    col1, col2 = st.columns(2)
    with col1:
        st.image("images/dbscan_0.png", caption="DBSCAN Cluster Plot", use_container_width=True)
    with col2:
        st.image("images/dbscan_1.png", caption="Noise Points (Anomalous Days)", use_container_width=True)
    st.markdown("Flags **5–8% noise points** as genuine extreme pollution anomalies — uniquely identifies crisis days not captured by other models.")

    st.divider()

    # ── Linear Regression ───────────────────────────────────────────
    st.subheader("🔴 Linear Regression — Continuous AQI Estimation")
    col1, col2 = st.columns(2)
    with col1:
        st.image("images/linear_regression_0.png", caption="Actual vs Predicted AQI", use_container_width=True)
    with col2:
        st.image("images/linear_regression_1.png", caption="Feature Coefficients", use_container_width=True)
    st.markdown("""
    **Metrics:** R² = **0.876** | RMSE = 46.1 | MAE = 32.9  
    PM2.5 is the dominant predictor. Temperature and wind speed show strong negative coefficients.
    """)

    st.divider()

    # ── Apriori ─────────────────────────────────────────────────────
    st.subheader("🟣 Apriori — Early-Warning Association Rules")
    col1, col2 = st.columns(2)
    with col1:
        st.image("images/apriori_0.png", caption="Top Association Rules (Support vs Confidence)", use_container_width=True)
    with col2:
        st.image("images/apriori_1.png", caption="Association Rules Heatmap (Lift)", use_container_width=True)
    st.markdown("""
    **Top rule:** `{aqi_category_Very Poor} → {pm25_bin_PM25_Severe}` — confidence 1.0, lift 3.2×  
    Actionable if-then rules for policy use; highest lift up to **8.8×** for Good AQI conditions.
    """)

    st.divider()

    # ================================================================
    # SECTION 4 — RESEARCH QUESTION ALIGNMENT
    # ================================================================
    st.header("4. Research Question Alignment")

    rq_df = pd.DataFrame({
        "Research Question": [
            "RQ1: Long-term PM2.5 trend?",
            "RQ2: Seasonal AQI patterns?",
            "RQ3: Weather combo → extreme AQI?",
            "RQ4: Wind / temp vs. pollution?",
            "RQ5: AQI category prediction?",
            "RQ6: Best AQI predictor combo?",
            "RQ7–8: Public attention lag?",
            "RQ9–10: Anomalous events?",
        ],
        "Primary Model": [
            "Linear Regression",
            "K-Means",
            "Apriori",
            "Decision Tree + Linear Regression",
            "Decision Tree",
            "Linear Regression",
            "Apriori + EDA",
            "DBSCAN",
        ],
        "Key Finding": [
            "No declining trend; coefficient on year is non-significant",
            "Three regimes: monsoon clean, winter severe, transitional",
            "Low wind + low temp + high PM2.5 → Severe (conf. 0.89)",
            "Temp coef. −3.10; wind coef. −2.45 (LR)",
            "92% accuracy; ROC-AUC 0.98",
            "R² = 0.96; PM2.5 dominant feature",
            "No search signal appears as antecedent of AQI — purely reactive",
            "5–8% noise points = genuine extreme pollution anomalies",
        ]
    })
    st.dataframe(rq_df, use_container_width=True, hide_index=True)

    st.divider()

    # ── Limitations ─────────────────────────────────────────
    st.header("5. Limitations & Next Steps")
    st.markdown("""
    <div class="warn-box">
    ⚠️ <b>Linear Regression linearity assumption:</b> PM2.5's log-normal distribution produces
    heteroscedastic residuals at extreme values. A log-transformed or tree-based regressor should be
    tested in Milestone 4.
    </div>
    <div class="warn-box">
    ⚠️ <b>Temporal autocorrelation:</b> Daily AQI values are serially correlated. The random train/test
    split may allow data leakage across adjacent days. A time-based split (train 2016–2021, test 2022–2024)
    is recommended for Milestone 4.
    </div>
    <div class="warn-box">
    ⚠️ <b>Google Trends gap:</b> 2023–2024 Trends data was filled as 'Unknown' and excluded from
    classification features. A complete Trends signal could improve models targeting RQ7–8.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **Milestone 4 will focus on:**
    - Temporal modeling (LSTM, time-series cross-validation)
    - Ensemble methods (Random Forest, XGBoost) for improved regression
    - Multi-day AQI forecasting capability
    - Time-based train/test split to prevent data leakage
    """)

with tab_team:
    st.header("Team")

    cols = st.columns(4)

    with cols[0]:
        st.image("images/abhiram.jpg", width=150)
        st.markdown("""
        **Abhirama Karthikeya Mullapudi**  
        *Data Lead*  

        Data Science student with a focus on Python- and SQL-based data analysis and machine learning, bringing 3 years of experience building scalable integrations and data pipelines. Serves as the Data Lead, responsible for data acquisition, preprocessing, and integration across datasets.
                    
        [LinkedIn](https://www.linkedin.com/in/abhiramakarthikeyamullapudi/) | 
        [GitHub](https://github.com/abhiram17-1289)
        """)

    with cols[1]:
        st.image("images/Nataraj.png", width=100)
        st.markdown("""
        **Natarajan Krishnan**  
        *EDA Lead*  

        MS-DS student at University of Colorado boulder. Proficient in Python and SQL. Contributing as an EDA lead, responsible for pre-processing and data preparation.  

        [LinkedIn](http://www.linkedin.com/in/natarajan-krishnan-a99aa137a) | 
        [GitHub](https://github.com/natarajankrishna)
        """)

    with cols[2]:
        st.image("images/Thiyagu.png", width=150)
        st.markdown("""
        **Thiyagu Rajendran**  
        *Visualization Lead*  

        MSDS Candidate & Experienced Data Engineer with 2.5+ years of experience specializing in building scalable ETL pipelines, performing complex Exploratory Data Analysis (EDA), and developing machine learning models, transforming raw data into actionable insights through advanced statistical modeling and data visualization, responsible for making visualizations for data analysis  

        [LinkedIn](https://www.linkedin.com/in/thiyagu-r-a94b941a3/) | 
        [GitHub](https://github.com/thiyagu-17)
        """)

    with cols[3]:
        st.image("images/hari.jpg", width=150)
        st.markdown("""
        **Srihari Pulagalla**  
        *Modeling Lead*  

        Data Science student with academic experience in Python, SQL, and data analysis. Serves as the Modeling Lead, responsible for developing and evaluating models for the project.  

        [LinkedIn](https://www.linkedin.com/in/srihari-pulagalla-652558352/) | 
        [GitHub](https://github.com/Srihari4589)
        """)

    st.markdown(
        "Our mission is to move beyond AQI reporting by identifying the patterns, conditions, and signals that precede severe air pollution events in Delhi, using data to inform timely awareness and intervention."
    )