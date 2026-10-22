# compare_cars.py
# Ranks used cars from a CSV file so the best choices come first.
# Run it with:  python3 compare_cars.py

import csv

BUDGET = 20000          # most I want to spend, in dollars
MIN_RELIABILITY = 3     # skip cars rated below this (1 = poor, 5 = excellent)


def score_car(price, miles, reliability):
    """Give a car a score from 0 to 100. Higher is better."""
    price_points = (BUDGET - price) / BUDGET * 30        # cheaper = more points (up to 30)
    miles_points = (150000 - miles) / 150000 * 30        # fewer miles = more points (up to 30)
    reliability_points = reliability / 5 * 40            # more reliable = more points (up to 40)
    return round(price_points + miles_points + reliability_points)


keep = []
skipped = []

with open("cars.csv") as file:
    for row in csv.DictReader(file):
        price = int(row["price"])
        miles = int(row["miles"])
        reliability = int(row["reliability"])

        if price > BUDGET:
            skipped.append(row["car"] + " (over budget)")
        elif reliability < MIN_RELIABILITY:
            skipped.append(row["car"] + " (not reliable enough)")
        elif row["awd"] != "yes":
            skipped.append(row["car"] + " (no all-wheel drive)")
        else:
            row["score"] = score_car(price, miles, reliability)
            keep.append(row)

# Sort so the highest score is first
keep.sort(key=lambda car: car["score"], reverse=True)

print("Best cars for me (highest score first):")
rank = 1
for car in keep:
    print(f"{rank}. {car['car']:<22} ${int(car['price']):>6,}  {int(car['miles']):>7,} miles  score {car['score']}")
    rank = rank + 1

print()
print("Skipped:")
for reason in skipped:
    print("-", reason)
