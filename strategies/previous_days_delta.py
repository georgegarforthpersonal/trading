from datetime import timedelta


def forecast_increase(price_today, price_yesterday, min_threshold=0, max_threshold=0.01):
    """Next day will increase if previous days increase is greater than a minimum threshold
    and less than a maximum threshold. This captures the tendency for multi-day gradual trending upwards
    and the tendency for a sharp increase to be followed by a gradual decrease.
    """
    if (price_today - price_yesterday > min_threshold) and (price_today - price_yesterday < max_threshold):
        return True
    else:
        return False


def calculate_profit(buy_price, sell_price):
    return sell_price - buy_price


def calculate_statistics(series):
    profit_list = []
    for date in series.index[2:-2]:
        price_yesterday = series[date - timedelta(days=1)]
        price_today = series[date]
        price_tomorrow = series[date + timedelta(days=1)]
        buy_decision = forecast_increase(price_today, price_yesterday)
        if buy_decision:
            profit = calculate_profit(price_today, price_tomorrow)
            profit_list.append([date, profit])
    return profit_list


def calculate_annual_profit(profit_list, investment):
    return round(investment * sum(p[1] for p in profit_list) / len(profit_list) * 365, 2)