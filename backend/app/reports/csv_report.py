import csv
from io import StringIO

def generate_trade_csv(trades):
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Date", "Symbol", "Side", "Qty", "Price",
        "SL", "Target", "Notes"
    ])

    for t in trades:
        writer.writerow([
            t.executed_at,
            t.symbol,
            t.side,
            t.quantity,
            t.price,
            t.sl,
            t.target,
            t.trade_notes
        ])

    return output.getvalue()
