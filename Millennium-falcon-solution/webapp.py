"""
Millennium Falcon Odds Calculator - Streamlit Web Application

A modern web interface for calculating the odds of the Millennium Falcon
successfully reaching Endor.
"""

import streamlit as st
import json
from typing import Dict, Tuple
import plotly.express as px
import networkx as nx

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
    G = falcon.create_graph()

    # Create positions for nodes
    pos = nx.spring_layout(G)

    # Create edge trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_color = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        if node in optimal_path:
            node_color.append("#FF4B4B")  # Red for optimal path
        else:
            node_color.append("#1f77b4")  # Blue for other nodes

    # Create figure
    fig = px.scatter(
        x=node_x,
        y=node_y,
        text=node_text,
        title="Galaxy Route Map",
    )

    # Add edges
    fig.add_scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(color="#888", width=1),
        hoverinfo="none",
    )

    # Update layout
    fig.update_layout(
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        plot_bgcolor="white",
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
                            f"{len(optimal_path) - 1} jumps" if optimal_path else "N/A",
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
