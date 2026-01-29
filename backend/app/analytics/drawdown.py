def max_drawdown(equity_curve):
    peak = equity_curve[0]
    max_dd = 0

    for value in equity_curve:
        peak = max(peak, value)
        dd = (peak - value)
        max_dd = max(max_dd, dd)

    return round(max_dd, 2)
