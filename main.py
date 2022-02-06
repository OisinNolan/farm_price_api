import gurobipy as gp
from gurobipy import GRB
import numpy as np

s = np.array([[1, 1, 0, 1, 0],
              [0, 1, 1, 1, 0],
              [0, 1, 1, 1, 0],
              [1, 0, 0, 0, 1]])
w = np.array([1, 4, 5, 6, 2]) # quantity
p = np.array([[10, 3, 4, 2, 1],
             [11, 3, 5, 3, 2],
             [9, 3, 3, 7, 3],
             [12, 3, 4, 6, 1]]) # price of 1 item in each shop

distance = np.array([3, 2, 2, 3]) # distance from the shop
pdist_cost = 2 # price of gas

def transport_cost(x, distance, pdist_cost, M):
    active_buyers = np.array([np.sum(x[i*M:(i+1)*M]) > 0 for i in range(len(distance))]).astype(int)
    t_cost = 0
    for i in range(len(active_buyers)):
        t_cost += distance[active_buyers[i]] * pdist_cost
    return t_cost


def find_buyers(availability, quantity, profits, distance, pdist_cost):

    N, M = availability.shape[0], availability.shape[1]
    availability= availability.flatten()
    prof_mask = np.tile(quantity, N) * profits.flatten() * availability.flatten()

    model = gp.Model('LP')
    model.setParam('LogToConsole', 0)
    x = model.addMVar(shape=(N * M), vtype=GRB.BINARY, name="x")

    model.addConstr(x @ np.ones(N * M) <= M)
    for i in range(M):
        arr_index = [i + j * M for j in range(N)]
        model.addConstr(x[arr_index] @ np.ones(N) == 1)
    best_objectives = np.zeros(N)
    optimal_values = np.zeros((N, N*M))
    for i in range(N):
        if i > 0:
            arr_index = x.x.astype(bool)
            model.addConstr(x @ arr_index <= M-1)

        model.setObjective(x @ prof_mask, GRB.MAXIMIZE)
        model.update()
        model.optimize()

        if model.status == GRB.OPTIMAL:
            best_objectives[i] = model.objVal - transport_cost(x.x, distance, pdist_cost, M)
            optimal_values[i] = x.x
            print('Success', ' Status:', model.status)
            print('Optimal objective: %g' % model.objVal)
            for i in range(N):
                print(f'X{i}: ', x.x[i * M:(i + 1) * M])
    shop_crops = []
    for i in np.argsort(best_objectives):
        shop_crops.append([])
        for j in range(N):
            if np.sum(optimal_values[i, j*M:(j+1)*M]) >= 1:
                shop_crops[-1].append({
                    'shops': j, 'crops' : np.where(optimal_values[i, j*M:(j+1)*M] == 1)[0]
                })
    return shop_crops

# order by the distance
# shop_crops = find_buyers(s, w, p, distance, pdist_cost)
#print(shop_crops)
#print(best_objectives)
