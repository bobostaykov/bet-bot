from math import ceil

PROFIT = 0.25

def bet():
    coef = float(input('initial coef: '))
    # amount paid since last win
    amount_paid = 0
    amount_to_bet = '0.25'
    if float(amount_to_bet) < PROFIT / (coef - 1):
        amount_to_bet = str(round_up(PROFIT / (coef - 1), 2))

    while True:
        print('Betting {}lv'.format(amount_to_bet))
        amount_paid += round(float(amount_to_bet), 2)

        coef = float(input('new coef: '))
        win = input('did we win? ')

        if win == 'yes':
            # we won
            cumulative_profit = 0
            print('cumulative_profit: ' + str(cumulative_profit))
            amount_paid = 0
            print('amount_paid: ' + str(amount_paid))
            amount_to_bet = '0.25'
            if float(amount_to_bet) < PROFIT / (coef - 1):
                amount_to_bet = str(round_up(PROFIT / (coef - 1), 2))
            print('amount_to_bet: ' + amount_to_bet + '\n')
        else:
            # we lost
            cumulative_profit = PROFIT + amount_paid
            print('amount_paid: {}'.format(amount_paid))
            print('cumulative_profit: ' + str(cumulative_profit))
            amount_to_bet = str(round_up(cumulative_profit / (coef - 1), 2))
            print('amount_to_bet: ' + amount_to_bet + '\n')



def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return ceil(n * multiplier) / multiplier


bet()