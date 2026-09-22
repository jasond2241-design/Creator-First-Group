from datetime import date
from unittest.mock import MagicMock

import pytest

from trade_tracker.models import Chamber, Owner, ParseStatus, TransactionType
from trade_tracker.senate_efd import (
    SenateEFDClient,
    _parse_amount,
    _parse_date,
    parse_transactions_table,
)

# A trimmed, real PTR detail page (fetched live from efdsearch.senate.gov
# during development) -- exercises the nested <div class="text-muted"> aside
# on the Asset Name column and the <a>-wrapped ticker on the Ticker column,
# both of which broke naive text-extraction approaches.
PTR_DETAIL_HTML = """
<div class="table-responsive">
<table class="table table-striped">
<thead>
<tr class="header">
<th scope="col">#</th><th scope="col">Transaction Date</th><th scope="col">Owner</th>
<th scope="col">Ticker</th><th scope="col">Asset Name</th><th scope="col">Asset Type</th>
<th scope="col">Type</th><th scope="col">Amount</th><th scope="col">Comment</th>
</tr>
</thead>
<tbody>
<tr>
<td>2</td>
<td>08/11/2026</td>
<td>Spouse</td>
<td><a href="https://finance.yahoo.com/quote/NVDA" target="_blank">NVDA</a></td>
<td>
    NVIDIA Corporation - Common Stock
    <div class="text-muted"><em>Company:</em> NVIDIA Corporation&nbsp;(Santa Clara, CA)</div>
    <div class="text-muted"><em>Description:</em>&nbsp;Technology Company</div>
</td>
<td>Stock</td>
<td>Sale (Full)</td>
<td>$15,001 - $50,000</td>
<td>--</td>
</tr>
<tr>
<td>1</td>
<td>08/18/2026</td>
<td>Self</td>
<td>--</td>
<td>
    webAI, Inc.
    <div class="text-muted"><em>Company:</em> webAI, Inc.&nbsp;(Austin, TX)</div>
</td>
<td>Non-Public Stock</td>
<td>Purchase</td>
<td>$1,001 - $15,000</td>
<td>Some comment</td>
</tr>
</tbody>
</table>
</div>
"""


def test_parse_transactions_table_extracts_ticker_past_anchor_and_skips_muted_aside():
    rows = parse_transactions_table(PTR_DETAIL_HTML)
    assert len(rows) == 2

    row0 = rows[0]
    assert row0[1] == "08/11/2026"  # Transaction Date
    assert row0[2] == "Spouse"  # Owner
    assert row0[3] == "NVDA"  # Ticker, pulled out from inside <a>
    assert row0[4] == "NVIDIA Corporation - Common Stock"  # Asset Name, muted aside excluded
    assert row0[6] == "Sale (Full)"  # Type
    assert row0[7] == "$15,001 - $50,000"  # Amount

    row1 = rows[1]
    assert row1[3] == "--"
    assert row1[4] == "webAI, Inc."
    assert row1[8] == "Some comment"


def test_parse_amount_range():
    r = _parse_amount("$15,001 - $50,000")
    assert r.low == 15001.0
    assert r.high == 50000.0
    assert r.raw == "$15,001 - $50,000"


def test_parse_amount_over():
    r = _parse_amount("Over $50,000,000")
    assert r.low == 50000000.0
    assert r.high is None


def test_parse_amount_empty():
    r = _parse_amount("--")
    assert r.low is None and r.high is None


def test_parse_date_valid_and_invalid():
    assert _parse_date("08/11/2026") == date(2026, 8, 11)
    assert _parse_date("") is None
    assert _parse_date("not a date") is None


def test_owner_from_raw():
    assert Owner.from_raw("Spouse") == Owner.SPOUSE
    assert Owner.from_raw("Joint") == Owner.JOINT
    assert Owner.from_raw("garbage") == Owner.UNKNOWN


def test_transaction_type_from_raw():
    assert TransactionType.from_raw("Purchase") == TransactionType.PURCHASE
    assert TransactionType.from_raw("Sale (Full)") == TransactionType.SALE_FULL
    assert TransactionType.from_raw("Sale (Partial)") == TransactionType.SALE_PARTIAL
    assert TransactionType.from_raw("Exchange") == TransactionType.EXCHANGE


def test_requires_contactable_user_agent():
    with pytest.raises(ValueError):
        SenateEFDClient(user_agent="no-contact-info")


def _mock_response(status_code=200, text="", json_data=None):
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    if json_data is not None:
        resp.json.return_value = json_data
    resp.raise_for_status.return_value = None
    return resp


def _client_with_session():
    client = SenateEFDClient(user_agent="Test test@example.com", request_delay=0)
    client.session = MagicMock()
    return client


def test_ensure_agreement_posts_once_and_is_idempotent():
    client = _client_with_session()
    home_html = '<input type="hidden" name="csrfmiddlewaretoken" value="TOKEN1">'
    client.session.get.return_value = _mock_response(text=home_html)
    client.session.post.return_value = _mock_response()

    client.ensure_agreement()
    client.ensure_agreement()

    assert client.session.post.call_count == 1
    posted_data = client.session.post.call_args.kwargs["data"]
    assert posted_data["prohibition_agreement"] == "1"
    assert posted_data["csrfmiddlewaretoken"] == "TOKEN1"


def test_search_ptr_filings_paginates_and_parses_rows():
    client = _client_with_session()
    home_html = '<input type="hidden" name="csrfmiddlewaretoken" value="HOME_TOKEN">'
    search_html = '<input type="hidden" name="csrfmiddlewaretoken" value="SEARCH_TOKEN">'

    page1 = {
        "recordsFiltered": 1,
        "data": [
            [
                "Jane",
                "Doe",
                "Doe, Jane (Senator)",
                '<a href="/search/view/ptr/abc123/" target="_blank">Periodic Transaction Report for 09/01/2026</a>',
                "09/02/2026",
            ]
        ],
    }

    client.session.get.side_effect = [_mock_response(text=home_html), _mock_response(text=search_html)]
    client.session.post.side_effect = [_mock_response(), _mock_response(json_data=page1)]

    filings = client.search_ptr_filings()

    assert len(filings) == 1
    f = filings[0]
    assert f["politician_name"] == "Jane Doe"
    assert f["filing_id"] == "abc123"
    assert f["filing_kind"] == "ptr"
    assert f["filing_url"] == "https://efdsearch.senate.gov/search/view/ptr/abc123/"
    assert f["filing_date"] == date(2026, 9, 2)


def test_fetch_filing_trades_paper_filing_is_unsupported_not_dropped_silently():
    client = _client_with_session()
    meta = {
        "politician_name": "Jane Doe",
        "office": "Doe, Jane (Senator)",
        "filing_id": "xyz",
        "filing_url": "https://efdsearch.senate.gov/search/view/paper/xyz/",
        "filing_kind": "paper",
        "filing_date": date(2026, 1, 1),
    }

    result = client.fetch_filing_trades(meta)

    assert result.status == ParseStatus.UNSUPPORTED_FORMAT
    assert result.trades == []
    assert result.error is not None
    client.session.get.assert_not_called()


def test_fetch_filing_trades_parses_ptr_html_into_trades():
    client = _client_with_session()
    client.session.get.return_value = _mock_response(text=PTR_DETAIL_HTML)
    meta = {
        "politician_name": "Jane Doe",
        "office": "Doe, Jane (Senator)",
        "filing_id": "abc123",
        "filing_url": "https://efdsearch.senate.gov/search/view/ptr/abc123/",
        "filing_kind": "ptr",
        "filing_date": date(2026, 9, 2),
    }

    result = client.fetch_filing_trades(meta)

    assert result.status == ParseStatus.PARSED
    assert len(result.trades) == 2
    trade = result.trades[0]
    assert trade.politician_name == "Jane Doe"
    assert trade.chamber == Chamber.SENATE
    assert trade.ticker == "NVDA"
    assert trade.transaction_type == TransactionType.SALE_FULL
    assert trade.owner == Owner.SPOUSE
    assert trade.amount.low == 15001.0
    assert trade.filing_date == date(2026, 9, 2)
