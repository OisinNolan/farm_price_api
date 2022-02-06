import gurobipy as gp
from gurobipy import GRB
import numpy as np


def transport_cost(x, distance, pdist_cost, M):
    '''
    Calculates full transportation cost to each buyer

    :param x: boolean list of chosen buyers
    :param distance: list of distances to each buyer
    :param pdist_cost:  cost per km for transportation
    :param M: number of crops

    :return: t_cost: transportation cost
    '''

    active_buyers = np.array([np.sum(x[i*M:(i+1)*M]) > 0 for i in range(len(distance))]).astype(int)
    t_cost = np.sum([distance[active_buyers[i]] for i in range(len(active_buyers))]) * pdist_cost

    return t_cost

def shop_crop(best_objectives, optimal_values, N, M):
    '''

    :param best_objectives:     not ordered list of best objective values
    :param optimal_values:      matrix of optimal values for each objective value
    :param N:   number of buyers
    :param M:   number of crops

    :return shop_crops:	ordered list of the optimal buyers (shops) ids and crop ids to sell
                e.g. [{'shop':1, 'crops': [2,3]},{'shops':3, 'crops':[0,4]}]
    '''

    shop_crops = []
    for i in np.argsort(best_objectives):
        shop_crops.append([])
        for j in range(N):
            if np.sum(optimal_values[i, j*M:(j+1)*M]) >= 1:
                shop_crops[-1].append({
                    'shop': j, 'crops' : np.where(optimal_values[i, j*M:(j+1)*M] == 1)[0]
                })
    return  shop_crops

def find_buyers(availability, quantity, profits, distance, pdist_cost, date=None):
    '''
        Find optimal buyers for list of crops

        :param availability:    NxM boolean matrix of crop m available to sell to n buyer
        :param quantity:    list of quantities for each crop
        :param profits:     list of profits for each crop unit
        :param distance:    list of distances to each buyer
        :param pdist_cost:  cost per km for transportation
        :param date:        date of the sale

        :return shop_crops:	ordered list of the optimal buyers (shops) ids and crop ids to sell
                e.g. [{'shop':1, 'crops': [2,3]},{'shops':3, 'crops':[0,4]}]
    '''


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
        else:
            pass
    shop_crops = shop_crop(best_objectives, optimal_values, N, M)
    return shop_crops

