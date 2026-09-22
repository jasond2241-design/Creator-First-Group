from datetime import date
from unittest.mock import MagicMock

import requests

from trade_tracker.models import (
    AmountRange,
    Chamber,
    Filing,
    Owner,
    Trade,
    TransactionType,
)
from trade_tracker.pipeline import filter_trades, run_pipeline


def _trade(name="Jane Doe", ticker="AAPL", d=date(2026, 1, 1)):
    return Trade(
        politician_name=name,
        chamber=Chamber.SENATE,
        office="Senator",
        owner=Owner.SELF,
        transaction_date=d,
        ticker=ticker,
        asset_name="Apple Inc.",
        asset_type="Stock",
        transaction_type=TransactionType.PURCHASE,
        amount=AmountRange(raw="$1,001 - $15,000", low=1001.0, high=15000.0),
        comment="",
        filing_id="abc",
        filing_url="https://efdsearch.senate.gov/search/view/ptr/abc/",
        filing_date=d,
    )


def test_filter_trades_by_politician_substring():
    trades = [_trade(name="Jane Doe"), _trade(name="John Smith")]
    result = filter_trades(trades, politician="doe")
    assert len(result) == 1
    assert result[0].politician_name == "Jane Doe"


def test_filter_trades_by_ticker_case_insensitive():
    trades = [_trade(ticker="AAPL"), _trade(ticker="NVDA")]
    result = filter_trades(trades, ticker="aapl")
    assert len(result) == 1
    assert result[0].ticker == "AAPL"


def test_run_pipeline_combines_both_sources():
    senate_client = MagicMock()
    senate_client.get_trades.return_value = ([_trade()], [])
    executive_client = MagicMock()
    executive_client.get_president_and_vp_filings.return_value = [
        Filing(
            filer_name="Doe, John",
            title="President - Annual Report",
            doc_type="New Filing",
            agency="The White House",
            level="President",
            doc_date=date(2026, 5, 1),
            document_url=None,
        )
    ]

    result = run_pipeline(
        user_agent="Test test@example.com",
        senate_client=senate_client,
        executive_client=executive_client,
    )

    assert len(result.trades) == 1
    assert len(result.executive_filings) == 1
    assert result.senate_errors == []
    assert result.executive_error is None


def test_run_pipeline_surfaces_executive_connection_failure_without_crashing():
    senate_client = MagicMock()
    senate_client.get_trades.return_value = ([], [])
    executive_client = MagicMock()
    executive_client.get_president_and_vp_filings.side_effect = requests.ConnectionError("reset")

    result = run_pipeline(
        user_agent="Test test@example.com",
        senate_client=senate_client,
        executive_client=executive_client,
    )

    assert result.executive_filings == []
    assert result.executive_error is not None


def test_run_pipeline_respects_skip_flags():
    senate_client = MagicMock()
    executive_client = MagicMock()

    result = run_pipeline(
        user_agent="Test test@example.com",
        skip_senate=True,
        skip_executive=True,
        senate_client=senate_client,
        executive_client=executive_client,
    )

    senate_client.get_trades.assert_not_called()
    executive_client.get_president_and_vp_filings.assert_not_called()
    assert result.trades == []
    assert result.executive_filings == []
