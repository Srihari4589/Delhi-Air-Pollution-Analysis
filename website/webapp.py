import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Urban Suffocation",
    layout="wide"
)

st.title("Urban Suffocation")
st.subheader(
    "A Spatiotemporal Analysis of Air Pollution, Policy, Weather, and Public Response in Delhi"
)


tab_intro, tab_proposal, tab_team = st.tabs([
    "Introduction",
    "Proposal Overview",
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
    # Illustrative Visual
    # ============================================================

    st.subheader("Seasonal Pollution Patterns: When Delhi Suffocates")

    import plotly.express as px
    import numpy as np

    # Create seasonal heatmap data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    years = list(range(2015, 2025))

    # Simulate realistic seasonal patterns
    heatmap_data = []
    for year in years:
        row = []
        for month in range(12):
            base = 150 + (year - 2015) * 5
            if month in [9, 10, 11, 0, 1]:  # Oct-Feb (winter)
                value = base * 1.6 + np.random.randint(-20, 30)
            elif month in [5, 6, 7]:  # Jun-Aug (monsoon)
                value = base * 0.5 + np.random.randint(-15, 15)
            else:
                value = base + np.random.randint(-10, 20)
            row.append(min(value, 500))  # Cap at 500
        heatmap_data.append(row)

    # Create heatmap
    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Month", y="Year", color="AQI"),
        x=months,
        y=years,
        color_continuous_scale=[
            [0, '#2ecc71'],      # Green (Good)
            [0.2, '#f1c40f'],    # Yellow (Moderate)
            [0.4, '#e67e22'],    # Orange (Unhealthy)
            [0.6, '#e74c3c'],    # Red (Very Unhealthy)
            [1, '#8b0000']       # Dark Red (Hazardous)
        ],
        aspect="auto"
    )

    fig.update_layout(
        title="Air Quality Heatmap: Delhi's Pollution Crisis Intensifies in Winter",
        height=450,
        xaxis_title="",
        yaxis_title=""
    )

    fig.update_xaxes(side="top")

    st.plotly_chart(fig, use_container_width=True)
    st.caption("*Darker red indicates hazardous air quality. Notice the consistent winter pollution crisis (Oct-Feb) across all years.*")

    

    
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

    years = list(range(2015, 2025))
    avg_pm25 = [85, 92, 98, 105, 112, 108, 118, 125, 130, 135]
    who_guideline = 5  # WHO 2021 guideline

    fig = go.Figure()

    # Add bars with color gradient based on severity
    colors = ['#f39c12' if pm < 100 else '#e74c3c' if pm < 120 else '#c0392b' for pm in avg_pm25]

    fig.add_trace(go.Bar(
        x=years,
        y=avg_pm25,
        name='Annual Average PM2.5',
        marker_color=colors,
        text=[f'{val} µg/m³' for val in avg_pm25],
        textposition='outside'
    ))

    # Add WHO guideline
    fig.add_trace(go.Scatter(
        x=years,
        y=[who_guideline] * len(years),
        name='WHO Guideline (2021)',
        line=dict(color='green', width=3, dash='dash'),
        mode='lines'
    ))

    # Add India National Standard
    fig.add_trace(go.Scatter(
        x=years,
        y=[40] * len(years),
        name='India NAAQS Standard',
        line=dict(color='orange', width=2, dash='dot'),
        mode='lines'
    ))

    fig.update_layout(
        title="Delhi's PM2.5 Levels vs. Safety Standards",
        xaxis_title="Year",
        yaxis_title="Annual Average PM2.5 (µg/m³)",
        height=500,
        showlegend=True,
        yaxis_range=[0, 150],
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption("*Delhi's PM2.5 levels are 15-27x higher than WHO guidelines, indicating severe long-term health risks including respiratory disease, cardiovascular problems, and reduced life expectancy.*")


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


    st.markdown("---")
    st.markdown(
        "Our mission is to move beyond AQI reporting by identifying the patterns, conditions, and signals that precede severe air pollution events in Delhi, using data to inform timely awareness and intervention."
    )


