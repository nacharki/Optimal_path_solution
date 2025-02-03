"""
Galaxy Module

This module implements the core game logic for the Millennium Falcon odds calculator.
"""

from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import pandas as pd
import networkx as nx
import sqlite3
import logging
from networkx.algorithms.simple_paths import all_simple_paths

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class BountyHunter:
    """Represents a bounty hunter's location and timing."""
    planet: str
    day: int


class Empire:
    """Represents the Galactic Empire's state and constraints."""

    def __init__(self, countdown: int, bounty_hunters: List[Dict[str, Any]]):
        """Initialize Empire parameters."""
        self.countdown = countdown
        # Store bounty hunters as plain dictionaries
        self.bounty_hunters = bounty_hunters
        logger.info(
            f"Initializing Empire with countdown: {countdown} and bounty hunters: {bounty_hunters}"
        )


class MillenniumFalcon(Empire):
    """Represents the Millennium Falcon's capabilities and mission parameters."""

    def __init__(
        self,
        autonomy: int,
        departure: str,
        arrival: str,
        routes_db: str,
        countdown: int,
        bounty_hunters: List[Dict[str, Any]],
    ):
        """Initialize Millennium Falcon parameters."""
        super().__init__(countdown, bounty_hunters)
        self.autonomy = autonomy
        self.departure = departure
        self.arrival = arrival
        self.routes_db = routes_db
        logger.info(
                    f"Initializing Millennium Falcon with autonomy: {autonomy}, departure: {departure}, arrival: {arrival}, routes_db: {routes_db}"  # noqa: E501
        )

    def read_routes(self) -> pd.DataFrame:
        """Read routes from SQLite database."""
        try:
            with sqlite3.connect(self.routes_db) as conn:
                return pd.read_sql_query("SELECT * from ROUTES", conn)
        except sqlite3.Error as e:
            logger.error(f"Database error: {str(e)}")
            raise

    def create_graph(self) -> nx.Graph:
        """Create graph representation of routes."""
        routes = self.read_routes()
        graph = nx.Graph()

        for _, row in routes.iterrows():
            graph.add_edge(
                row["origin"], row["destination"], distance=row["travel_time"]
            )

        return graph

    def find_feasible_paths(self) -> Dict[str, List]:
        """Find all paths that satisfy autonomy constraints."""
        graph = self.create_graph()
        paths = list(all_simple_paths(graph, self.departure, self.arrival))
        feasible_paths = {}

        for idx, path in enumerate(paths, 1):
            current_autonomy = self.autonomy
            travel_days = 0
            stops = [self.departure]
            days = [0]

            for current, next_stop in zip(path[:-1], path[1:]):
                travel_time = graph[current][next_stop]["distance"]

                if travel_time <= self.autonomy:
                    travel_days += travel_time
                    days.append(travel_days)
                    stops.append(next_stop)
                    current_autonomy = self.autonomy - travel_time

                    if current_autonomy == 0:
                        stops.append(next_stop)
                        travel_days += 1
                        days.append(travel_days)
                        current_autonomy = self.autonomy

            feasible_paths[f"path_{idx}"] = [stops, days]

        return feasible_paths

    def find_acceptable_paths(self) -> Dict[str, List]:
        """Find paths that reach Endor before countdown."""
        feasible_paths = self.find_feasible_paths()
        return {
            key: value
            for key, value in feasible_paths.items()
            if value[1][-1] <= self.countdown
        }

    def find_alternative_paths(self) -> Dict[str, List]:
        """Find alternative paths with rest stops."""
        acceptable_paths = self.find_acceptable_paths()
        alternative_paths = {}

        for key, (path, day) in acceptable_paths.items():
            possible_rest = self.countdown - day[-1]

            if possible_rest >= 1:
                rest = 1
                unique_stops = set(path[:-1])

                for idx, stop in enumerate(unique_stops):
                    path_copy = path.copy()
                    day_copy = day.copy()
                    path_copy.insert(idx + 1, f"{stop}*{rest}")
                    day_copy.insert(idx + 1, day_copy[idx] + 1)

                    # Adjust subsequent days
                    for i in range(idx + 2, len(day_copy)):
                        day_copy[i] += 1

                    alternative_paths[f"{key}_{idx + 1}"] = [path_copy, day_copy]

        return alternative_paths

    def give_me_the_odds(self) -> Tuple[float, List[str]]:
        """Calculate odds of mission success and determine optimal path."""
        feasible_paths = self.find_feasible_paths()
        valid_paths = [
            [path, day]
            for path, day in feasible_paths.values()
            if day[-1] <= self.countdown
        ]

        if not valid_paths:
            return 0, []

        acceptable_paths = self.find_acceptable_paths()
        alternative_paths = self.find_alternative_paths()
        all_paths = {**acceptable_paths, **alternative_paths}

        encounters_by_path = []
        paths = []

        # Calculate encounters for each path
        for path, days in all_paths.values():
            encounter_count = 0
            for i in range(len(path)):
                current_stop = path[i]
                current_day = days[i]

                # Check each bounty hunter
                for bh in self.bounty_hunters:
                    if bh["planet"] == current_stop and bh["day"] == current_day:
                        encounter_count += 1

            encounters_by_path.append(encounter_count)
            paths.append(path)

        min_encounters = min(encounters_by_path)
        optimal_path = paths[encounters_by_path.index(min_encounters)]

        if min_encounters > 0:
            prob = 0.1  # Initial capture probability
            for i in range(1, min_encounters):
                prob += (9**i) / (10 ** (i + 1))
            return 100 * (1 - prob), optimal_path

        return 100, optimal_path


if __name__ == "__main__":
    """Entry point for command line execution."""

    def load_config(filepath: str) -> Dict:
        """Load JSON configuration file."""
        logging.info("Loading configuration from %s", filepath)
        return pd.read_json(filepath, typ="series").to_dict()

    # Load configurations
    empire_config = load_config("example4/empire.json")
    falcon_config = load_config("example4/millennium-falcon.json")

    # Initialize game state
    empire = Empire(
        countdown=empire_config["countdown"],
        bounty_hunters=empire_config["bounty_hunters"],
    )

    falcon = MillenniumFalcon(
        autonomy=falcon_config["autonomy"],
        departure=falcon_config["departure"],
        arrival=falcon_config["arrival"],
        routes_db=falcon_config["routes_db"],
        countdown=empire.countdown,
        bounty_hunters=empire.bounty_hunters,
    )

    # Calculate odds and optimal path
    odds, optimal_path = falcon.give_me_the_odds()

    logging.info("Success probability: %.1f%%", odds)
    logging.info("Optimal path: %s", " -> ".join(optimal_path))
