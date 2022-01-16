
def read_input(filename):
    try:
        input_file = open(filename, "r")
        money = input_file.readline().rstrip('\n')
        coins = input_file.readline().rstrip('\n').split(",")
        coins = [int(c) for c in coins]
        input_file.close()
    except:
        print("Exception caught, file probably doesnt exist")
    return int(money), coins

def DPChange(money, coins):
    n = len(coins)
    min_num_coins = [0]
    for m in range(1, money+1):
        min_num_coins.append(float('inf'))
        for i in range(0, n):
            if m >= coins[i]:
                num_of_coins_of_m = min_num_coins[m-coins[i]] + 1
                if num_of_coins_of_m < min_num_coins[m]:
                    min_num_coins[m] = num_of_coins_of_m
    return min_num_coins[money]

def start():
    money, coins = read_input("dataset.txt")
    result = DPChange(money, coins)
    print(result)

if __name__ == '__main__':
    start()
