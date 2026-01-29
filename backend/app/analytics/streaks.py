def trade_streaks(pnl_list):
    """
    pnl_list: list of realized P&L values in chronological order
    Example: [1200, -500, -300, 800, 900]
    """

    max_win_streak = 0
    max_loss_streak = 0
    current_win = 0
    current_loss = 0

    for pnl in pnl_list:
        if pnl > 0:
            current_win += 1
            current_loss = 0
        else:
            current_loss += 1
            current_win = 0

        if current_win > max_win_streak:
            max_win_streak = current_win

        if current_loss > max_loss_streak:
            max_loss_streak = current_loss

    return {
        "max_win_streak": max_win_streak,
        "max_loss_streak": max_loss_streak
    }
