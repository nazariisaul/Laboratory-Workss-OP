crypto_name = "Ethereum"                # Назва криптовалюти
symbol = "ETH"                          # Біржовий символ
network = "Ethereum Mainnet"            # Назва мережі
consensus = "Proof-of-Stake"            # Механізм консенсусу
organization = "Ethereum Foundation"    # Організація-розробник

launch_year = 2015                      # Рік запуску
current_rank = 2                        # Позиція за капіталізацією (після Bitcoin)
daily_transactions = 1_200_000          # Середня кількість транзакцій на добу
contracts_deployed = 4_500_000          # Кількість смарт-контрактів, розгорнутих у мережі
erc20_tokens = 600_000                  # Кількість ERC-20 токенів

current_price = 2200.75                 # Ціна ETH у доларах
market_cap = 270_000_000_000.00         # Ринкова капіталізація ($)
daily_volume = 14_200_000_000.75        # Добовий обсяг торгів ($)
circulating_supply = 122_345_678.55     # Монет в обігу
energy_consumption = 0.0026             # Споживання енергії на транзакцію (кВт·год)

print("Назва:", crypto_name)
print("Символ:", symbol)
print("Назва мережі:", network)
print("Механізм консенсусу:", consensus)
print("Організація-розробник:", organization)

print()

print("Рік запуску:", launch_year)
print("Позиція за капіталізацією:", current_rank, "після Bitcoin")
print("Середня кількість транзакцій на добу:",daily_transactions)
print("Кількість смарт-контрактів, розгорнутих у мережі:", contracts_deployed)
print("Кількість ERC-20 токенів:",erc20_tokens)

print()

print("Ціна ETH:", current_price, "$")
print("Ринкова капіталізація:", market_cap, "$")
print("Добовий обсяг торгів:", daily_volume, "$")
print("Монет в обігу:", circulating_supply)
print("Споживання енергії на транзакцію", energy_consumption, "кВт·год")
