import time
import random
from typing import Any, Dict, List, Union, Literal, TypedDict

import numpy as np

from orca_python import Processor

# Type definitions
Number = Union[int, float]
MarketTrend = Literal["bullish", "bearish", "neutral"]
TradeAction = Literal["buy", "sell", "hold"]


class DataLoaderResult(TypedDict):
    features: List[List[float]]
    timestamps: List[float]


class MarketDataResult(TypedDict):
    prices: List[float]
    volume: List[int]


class ConfigResult(TypedDict):
    threshold: float
    window_sise: int
    min_samples: int


class FeatureResult(TypedDict):
    technical_indicators: List[List[float]]
    metadata: Dict[str, float]


class MarketAnalysisResult(TypedDict):
    trend: MarketTrend
    confidence: float


class SignalResult(TypedDict):
    signals: List[int]
    strength: float


class RiskMetrics(TypedDict):
    var: float
    sharpe: float
    max_drawdown: float


class PortfolioResult(TypedDict):
    weights: List[float]
    expected_return: float
    risk_adjusted_return: float


class TradeActionCls(TypedDict):
    asset: int
    action: TradeAction


class StrategyResult(TypedDict):
    actions: List[TradeActionCls]
    execution_time: float
    confidence_score: float


proc = Processor("ml_v2")


# base layer algorithms (no dependencies)
@proc.algorithm("DataLoader", "1.0.0", "WindowA", "1.0.0")
def load_data() -> DataLoaderResult:
    """Simulates loading and preprocessing data"""
    time.sleep(0.5)  # simulate data fetch delay
    return {
        "features": np.random.randn(100, 10).tolist(),
        "timestamps": [time.time() - i for i in range(100)],
    }


@proc.algorithm("MarketData", "1.0.0", "WindowA", "1.0.0")
def fetch_market_data() -> MarketDataResult:
    """Simulates fetching market data"""
    time.sleep(0.3)  # simulate deata fetch delay
    return {
        "prices": [random.uniform(10, 100) for _ in range(50)],
        "volume": [random.randint(1000, 10000) for _ in range(50)],
    }


@proc.algorithm("ConfigLoader", "1.0.0", "WindowA", "1.0.0")
def load_config() -> ConfigResult:
    """Loads configuration settings"""
    return {"threshold": 0.75, "window_sise": 20, "min_samples": 50}


# second layer algorithms (single dependencies)
@proc.algorithm("FeatureExtractor", "1.0.0", "WindowA", "1.0.0", depends_on=[load_data])
def extract_features(**kwargs: Dict[str, Any]) -> FeatureResult:
    """Extracts features from raw data"""
    time.sleep(0.8)  # Simulate complex computation
    return {
        "technical_indicators": np.random.randn(100, 5).tolist(),
        "metadata": {"processing_time": time.time()},
    }


@proc.algorithm(
    "MarketAnalyser", "1.0.0", "WindowA", "1.0.0", depends_on=[fetch_market_data]
)
def analyse_market(**kwargs: Dict[str, Any]) -> MarketAnalysisResult:
    """Analyses market data for patterns"""
    time.sleep(0.4)
    return {
        "trend": random.choice(["bullish", "bearish", "neutral"]),
        "confidence": random.uniform(0.6, 0.9),
    }


# Third layer algorithms (multiple dependencies)
@proc.algorithm(
    "SignalGenerator",
    "1.0.0",
    "WindowA",
    "1.0.0",
    depends_on=[extract_features, analyse_market, load_config],
)
def generate_signals(**kwargs: Dict[str, Any]) -> SignalResult:
    """Generates trading signals based on features and market analysis"""
    time.sleep(1.0)  # Complex signal generation
    return {
        "signals": [random.choice([-1, 0, 1]) for _ in range(10)],
        "strength": random.uniform(0.1, 1.0),
    }


@proc.algorithm(
    "RiskCalculator",
    "1.0.0",
    "WindowA",
    "1.0.0",
    depends_on=[analyse_market, load_config],
)
def calculate_risk(**kwargs: Dict[str, Any]) -> RiskMetrics:
    """Calculates risk metrics"""
    time.sleep(0.6)
    return {
        "var": random.uniform(0.1, 0.3),
        "sharpe": random.uniform(0.5, 2.0),
        "max_drawdown": random.uniform(0.1, 0.4),
    }


# Fourth layer algorithms (complex dependencies)
@proc.algorithm(
    "PortfolioOptimiser",
    "1.0.0",
    "WindowA",
    "1.0.0",
    depends_on=[generate_signals, calculate_risk],
)
def optimise_portfolio(**kwargs: Dict[str, Any]) -> PortfolioResult:
    """Optimises portfolio based on signals and risk"""
    time.sleep(1.5)  # Heavy optimisation computation
    return {
        "weights": [random.uniform(0, 1) for _ in range(5)],
        "expected_return": random.uniform(0.05, 0.15),
        "risk_adjusted_return": random.uniform(0.1, 0.2),
    }


# final layer algorithm (aggregates everything)
@proc.algorithm(
    "TradingStrategy",
    "1.0.0",
    "WindowA",
    "1.0.0",
    depends_on=[optimise_portfolio, calculate_risk, generate_signals],
)
def execute_strategy(**kwargs: Dict[str, Any]) -> StrategyResult:
    """Executes final trading strategy"""
    time.sleep(0.7)
    return {
        "actions": [
            {"asset": i, "action": random.choice(["buy", "sell", "hold"])}
            for i in range(5)
        ],
        "execution_time": time.time(),
        "confidence_score": random.uniform(0.5, 1.0),
    }


if __name__ == "__main__":
    proc.Register()
    proc.Start()
