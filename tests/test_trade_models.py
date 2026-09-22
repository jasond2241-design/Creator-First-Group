from datetime import date

from trade_tracker.models import (
    AmountRange,
    Chamber,
    Owner,
    ParseStatus,
    Trade,
    TransactionType,
)


def test_owner_from_raw_unknown_value():
    assert Owner.from_raw("") == Owner.UNKNOWN
    assert Owner.from_raw(None) == Owner.UNKNOWN


def test_transaction_type_from_raw_unknown_value():
    assert TransactionType.from_raw("Merger") == TransactionType.UNKNOWN


def test_trade_construction():
    trade = Trade(
        politician_name="Jane Doe",
        chamber=Chamber.SENATE,
        office="Senator",
        owner=Owner.SELF,
        transaction_date=date(2026, 1, 1),
        ticker="AAPL",
        asset_name="Apple Inc.",
        asset_type="Stock",
        transaction_type=TransactionType.PURCHASE,
        amount=AmountRange(raw="$1,001 - $15,000", low=1001.0, high=15000.0),
        comment="",
        filing_id="abc",
        filing_url="https://efdsearch.senate.gov/search/view/ptr/abc/",
        filing_date=date(2026, 1, 5),
    )
    assert trade.ticker == "AAPL"
    assert trade.amount.high == 15000.0


def test_parse_status_values():
    assert ParseStatus.PARSED.value == "parsed"
    assert ParseStatus.UNSUPPORTED_FORMAT.value == "unsupported_format"
