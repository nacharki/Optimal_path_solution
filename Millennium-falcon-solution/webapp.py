"""
Millennium Falcon Odds Calculator - Streamlit Web Application

A modern web interface for calculating the odds of the Millennium Falcon
successfully reaching Endor.
"""

import streamlit as st
import json
from typing import Dict, Tuple
import plotly.graph_objects as go

from Galaxy import Empire, MillenniumFalcon

# Configuration
st.set_page_config(
    page_title="Millennium Falcon Mission Calculator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    .success-text {
        color: #00CC66;
        font-size: 24px;
        font-weight: bold;
    }
    .failure-text {
        color: #FF4B4B;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_json_file(file_content) -> Dict:
    """Load and validate JSON data."""
    try:
        if isinstance(file_content, bytes):
            return json.loads(file_content.decode("utf-8"))
        return json.loads(file_content)
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON file: {str(e)}")
        return None


def create_route_visualization(falcon: MillenniumFalcon, optimal_path: list):
    """Create an interactive route visualization."""
    # Define fixed positions for known planets
    planet_positions = {
        "Tatooine": (0, 0),
        "Hoth": (2, 2),
        "Endor": (4, 0),
        "Dagobah": (-1, 1),
        "Bespin": (1, 3),
    }

    # Create figure
    fig = go.Figure()

    # Add all planets as points
    x_planets, y_planets, names = [], [], []
    for planet, pos in planet_positions.items():
        x_planets.append(pos[0])
        y_planets.append(pos[1])
        names.append(planet)

    # Add planets
    fig.add_trace(
        go.Scatter(
            x=x_planets,
            y=y_planets,
            mode="markers+text",
            name="Planets",
            text=names,
            textposition="top center",
            marker=dict(
                size=20,
                color="gold",
                symbol="circle",
                line=dict(color="white", width=2),
            ),
            hovertemplate="%{text}<extra></extra>",
        )
    )

    # Create path coordinates
    path_x, path_y = [], []
    for planet in optimal_path:
        if planet in planet_positions:
            path_x.append(planet_positions[planet][0])
            path_y.append(planet_positions[planet][1])

    # Add path line
    fig.add_trace(
        go.Scatter(
            x=path_x,
            y=path_y,
            mode="lines+markers",
            name="Route",
            line=dict(color="#FF4B4B", width=3),
            marker=dict(size=12, color="#FF4B4B", symbol="arrow", angleref="previous"),
            hoverinfo="skip",
        )
    )

    # Update layout
    fig.update_layout(
        title=dict(text="Galaxy Route Map", x=0.5, font=dict(size=24, color="white")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        width=800,
        height=500,
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="#333",
            zeroline=False,
            showticklabels=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor="#333",
            zeroline=False,
            showticklabels=False,
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="closest",
    )

    # Add route annotations
    for i in range(len(optimal_path) - 1):
        fig.add_annotation(
            x=(path_x[i] + path_x[i + 1]) / 2,
            y=(path_y[i] + path_y[i + 1]) / 2,
            text=f"path {i+1}",
            showarrow=False,
            font=dict(size=12, color="white"),
            bgcolor="rgba(0,0,0,0.5)",
        )

    return fig


def compute_odds(falcon_data: Dict, empire_data: Dict) -> Tuple[float, list]:
    """Calculate mission success probability."""
    try:
        # Initialize game objects
        empire = Empire(
            countdown=empire_data["countdown"],
            bounty_hunters=empire_data["bounty_hunters"],
        )

        falcon = MillenniumFalcon(
            autonomy=falcon_data["autonomy"],
            departure=falcon_data["departure"],
            arrival=falcon_data["arrival"],
            routes_db=falcon_data["routes_db"],
            countdown=empire.countdown,
            bounty_hunters=empire.bounty_hunters,
        )

        # Calculate odds
        odds, optimal_path = falcon.give_me_the_odds()

        return odds, optimal_path, falcon

    except Exception as e:
        st.error(f"Error computing odds: {str(e)}")
        return None, None, None


def main():
    """Main application."""
    # Header
    st.title("🚀 Millennium Falcon Mission Calculator")
    st.markdown(
        """
        Calculate the odds of successfully reaching Endor and saving the galaxy!
        Upload both configuration files below.
    """
    )

    # File upload section
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Millennium Falcon Configuration")
        falcon_file = st.file_uploader(
            "Upload millennium-falcon.json",
            type=["json"],
            help="Select the millennium-falcon.json file containing ship configuration",
        )

    with col2:
        st.subheader("Empire Intelligence")
        empire_file = st.file_uploader(
            "Upload empire.json",
            type=["json"],
            help="Select the empire.json file containing countdown and bounty hunter information",
        )

    if falcon_file and empire_file:
        falcon_data = load_json_file(falcon_file.read())
        empire_data = load_json_file(empire_file.read())

        if falcon_data and empire_data:
            # Show configurations
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Millennium Falcon Parameters")
                st.json(falcon_data)

            with col2:
                st.subheader("Empire Intelligence")
                st.json(empire_data)

            # Calculate button
            if st.button("Calculate Odds", key="calc_button"):
                odds, optimal_path, falcon = compute_odds(falcon_data, empire_data)

                if odds is not None:
                    # Display results
                    st.markdown("### Mission Success Probability")
                    probability_text = f"{odds:.1f}%"

                    if odds > 50:
                        st.markdown(
                            f'<p class="success-text">{probability_text}</p>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f'<p class="failure-text">{probability_text}</p>',
                            unsafe_allow_html=True,
                        )

                    if optimal_path:
                        st.markdown("### Optimal Route")
                        st.write(" → ".join(optimal_path))

                        # Create and display route visualization
                        fig = create_route_visualization(falcon, optimal_path)
                        st.plotly_chart(fig, use_container_width=True)

                    # Display additional metrics
                    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                    with metrics_col1:
                        st.metric(
                            "Time to Destruction", f"{empire_data['countdown']} days"
                        )
                    with metrics_col2:
                        st.metric("Bounty Hunters", len(empire_data["bounty_hunters"]))
                    with metrics_col3:
                        st.metric(
                            "Route Length",
                            f"{len(optimal_path) - 1} paths" if optimal_path else "N/A",
                        )

    # Instructions
    with st.sidebar:
        st.header("Instructions")
        st.markdown(
            """
        1. Upload both required configuration files:
           - `millennium-falcon.json`: Ship configuration
           - `empire.json`: Empire intelligence data
        2. Review the loaded configurations
        3. Click "Calculate Odds" to analyze the mission
        4. Review the results and optimal route

        ### File Format Examples

        millennium-falcon.json:
        ```json
        {
            "autonomy": 6,
            "departure": "Tatooine",
            "arrival": "Endor",
            "routes_db": "universe.db"
        }
        ```

        empire.json:
        ```json
        {
            "countdown": 7,
            "bounty_hunters": [
                {"planet": "Hoth", "day": 6},
                {"planet": "Hoth", "day": 7}
            ]
        }
        ```
        """
        )

        # Add some Star Wars theming
        st.markdown("---")
        st.markdown("*May God be with you!* ⚔️")


if __name__ == "__main__":
    main()
