import numpy as np

""" File with a dummy data """


S = np.array([[1, 1, 0, 1, 0],
              [0, 1, 1, 1, 0],
              [0, 1, 1, 1, 0],
              [1, 0, 0, 0, 1]])
W = np.array([1, 4, 5, 6, 2]) # quantity
P = np.array([[10, 3, 4, 2, 1],
             [11, 3, 5, 3, 2],
             [9, 3, 3, 7, 3],
             [12, 3, 4, 6, 1]]) # price of 1 item in each shop

DISTANCES = np.array([3, 2, 2, 3]) # distance from the shop
PDIST_COST = 2 # price of gas

inputs_ = {
    'shop_buys': S,
    'food_weights': W,
    'food_prices': P,
    'shop_distances': DISTANCES,
    'gas_price': PDIST_COST,
}