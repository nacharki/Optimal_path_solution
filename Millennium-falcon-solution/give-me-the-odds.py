#!/usr/bin/env python3
"""
Give Me The Odds - CLI Tool

This script calculates the odds of the Millennium Falcon successfully reaching
Endor based on provided configuration files.

Usage:
    python give-me-the-odds.py <millennium-falcon.json> <empire.json>
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Tuple
import pandas as pd
import argparse

from Galaxy import Empire, MillenniumFalcon

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def setup_argparser() -> argparse.ArgumentParser:
    """Configure and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Calculate the odds of the Millennium Falcon reaching Endor.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
    python give-me-the-odds.py millennium-falcon.json empire.json
        """,
    )

    parser.add_argument(
        "falcon_config",
        type=str,
        help="Path to Millennium Falcon configuration file (JSON)",
    )

    parser.add_argument(
        "empire_config", type=str, help="Path to Empire configuration file (JSON)"
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    return parser


def validate_file(file_path: str) -> Path:
    """
    Validate that the file exists and is readable.

    Parameters:
        file_path: Path to the file to validate

    Returns:
        Path object for the validated file

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file isn't readable
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not path.is_file():
        raise ValueError(f"Not a file: {file_path}")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"File not readable: {file_path}")
    return path


def load_config(file_path: Path) -> dict:
    """
    Load and validate JSON configuration file.

    Parameters:
        file_path: Path to the JSON file

    Returns:
        Dictionary containing the configuration

    Raises:
        JSONDecodeError: If JSON is invalid
        KeyError: If required fields are missing
    """
    try:
        config = pd.read_json(file_path, typ="series").to_dict()
        return config
    except (json.JSONDecodeError, pd.errors.EmptyDataError) as e:
        raise ValueError(f"Invalid JSON in {file_path}: {str(e)}")
    except Exception as e:
        raise Exception(f"Error loading {file_path}: {str(e)}")


def calculate_odds(
    falcon_config: dict, empire_config: dict, verbose: bool = False
) -> Tuple[float, list]:
    """
    Calculate success probability and optimal path.

    Parameters:
        falcon_config: Millennium Falcon configuration
        empire_config: Empire configuration
        verbose: Whether to print detailed information

    Returns:
        Tuple of (success probability, optimal path)
    """
    # Initialize Empire
    empire = Empire(
        countdown=empire_config["countdown"],
        bounty_hunters=empire_config["bounty_hunters"],
    )

    # Initialize Millennium Falcon
    falcon = MillenniumFalcon(
        autonomy=falcon_config["autonomy"],
        departure=falcon_config["departure"],
        arrival=falcon_config["arrival"],
        routes_db=falcon_config["routes_db"],
        countdown=empire.countdown,
        bounty_hunters=empire.bounty_hunters,
    )

    # Calculate odds
    odds, path = falcon.give_me_the_odds()

    if verbose and path:
        logger.info(f"Optimal path found: {' -> '.join(path)}")

    return odds, path


def main() -> int:
    """Main entry point for the script."""
    try:
        # Parse command line arguments
        parser = setup_argparser()
        args = parser.parse_args()

        # Enable verbose logging if requested
        if args.verbose:
            logger.setLevel(logging.DEBUG)

        # Validate input files
        falcon_path = validate_file(args.falcon_config)
        empire_path = validate_file(args.empire_config)

        # Load configurations
        logger.debug("Loading configuration files...")
        falcon_config = load_config(falcon_path)
        empire_config = load_config(empire_path)

        # Calculate odds
        logger.debug("Calculating odds...")
        odds, _ = calculate_odds(falcon_config, empire_config, args.verbose)

        # Print result
        logger.info(f"Success probability: {odds:.1f}%")

        return 0

    except KeyboardInterrupt:
        logger.error("\nOperation cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if args.verbose:
            logger.exception("Detailed error information:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
