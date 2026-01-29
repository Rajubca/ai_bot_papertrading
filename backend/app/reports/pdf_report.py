from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table

def generate_trade_pdf(file_path, trades):
    pdf = SimpleDocTemplate(file_path, pagesize=A4)

    table_data = [[
        "Date", "Symbol", "Side", "Qty", "Price", "Notes"
    ]]

    for t in trades:
        table_data.append([
            str(t.executed_at),
            t.symbol,
            t.side,
            t.quantity,
            t.price,
            t.trade_notes or ""
        ])

    table = Table(table_data)
    pdf.build([table])
