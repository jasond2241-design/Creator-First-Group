import json
from datetime import date
from unittest.mock import patch

from trade_tracker.models import AmountRange, Chamber, Owner, Trade, TrackerResult, TransactionType
from trade_tracker import update_data


def _trade(ticker="AAPL", d=date(2026, 1, 1), filing_id="f1"):
    return Trade(
        politician_name="Jane Doe",
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
        filing_id=filing_id,
        filing_url=f"https://efdsearch.senate.gov/search/view/ptr/{filing_id}/",
        filing_date=d,
    )


def _patch_paths(tmp_path, monkeypatch):
    monkeypatch.setattr(update_data, "TRADES_PATH", tmp_path / "senate_trades.json")
    monkeypatch.setattr(update_data, "EXECUTIVE_PATH", tmp_path / "executive_filings.json")
    monkeypatch.setattr(update_data, "STATE_PATH", tmp_path / "tracker_state.json")


def test_run_writes_new_trades_on_first_run(tmp_path, monkeypatch):
    _patch_paths(tmp_path, monkeypatch)
    result = TrackerResult(trades=[_trade()], executive_filings=[], senate_errors=[], executive_error=None)

    with patch.object(update_data, "run_pipeline", return_value=result) as mock_pipeline:
        summary = update_data.run(user_agent="Test test@example.com")

    assert summary["added_trades"] == 1
    assert summary["total_trades"] == 1
    assert mock_pipeline.call_args.kwargs["since"] is not None  # backfill window applied

    saved = json.loads(update_data.TRADES_PATH.read_text())
    assert len(saved) == 1
    assert saved[0]["ticker"] == "AAPL"

    state = json.loads(update_data.STATE_PATH.read_text())
    assert state["senate_last_filing_date"] == date.today().isoformat()


def test_run_dedupes_across_runs(tmp_path, monkeypatch):
    _patch_paths(tmp_path, monkeypatch)
    trade = _trade()
    result = TrackerResult(trades=[trade], executive_filings=[], senate_errors=[], executive_error=None)

    with patch.object(update_data, "run_pipeline", return_value=result):
        update_data.run(user_agent="Test test@example.com")
        summary = update_data.run(user_agent="Test test@example.com")

    assert summary["added_trades"] == 0
    assert summary["total_trades"] == 1


def test_run_uses_watermark_with_overlap_on_second_run(tmp_path, monkeypatch):
    _patch_paths(tmp_path, monkeypatch)
    result = TrackerResult(trades=[], executive_filings=[], senate_errors=[], executive_error=None)

    with patch.object(update_data, "run_pipeline", return_value=result) as mock_pipeline:
        update_data.run(user_agent="Test test@example.com")
        first_since = mock_pipeline.call_args.kwargs["since"]
        update_data.run(user_agent="Test test@example.com")
        second_since = mock_pipeline.call_args.kwargs["since"]

    assert second_since > first_since  # narrowed from the full backfill window to near-today
    assert second_since <= date.today()


def test_run_surviving_executive_error_still_saves_trades(tmp_path, monkeypatch):
    _patch_paths(tmp_path, monkeypatch)
    result = TrackerResult(
        trades=[_trade()], executive_filings=[], senate_errors=[], executive_error="connection reset"
    )

    with patch.object(update_data, "run_pipeline", return_value=result):
        summary = update_data.run(user_agent="Test test@example.com")

    assert summary["added_trades"] == 1
    assert summary["executive_error"] == "connection reset"
