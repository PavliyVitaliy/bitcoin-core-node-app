INITIAL_REWARD = 50  # initial reward in BTC
HALVING_INTERVAL = 210000  # BTC halving intervals


def calculate_total_btc(height: int) -> int:
    reward = INITIAL_REWARD
    total_btc = 0

    # Loop through each halving period
    while height > 0:
        blocks = min(height, HALVING_INTERVAL)
        total_btc += blocks * reward
        height -= blocks
        reward /= 2  # Reward halves every interval

    return total_btc
