# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 15:13:39 2023

@author: nacha
"""


import pandas as pd
import networkx as nx

import sqlite3

from networkx.algorithms.simple_paths import all_simple_paths

class Empire:
    def __init__(self, countdown, bounty_hunters):
        self.countdown = countdown
        self.bounty_hunters = bounty_hunters

class Millennium_falcon(Empire):
    def __init__(self, autonomy, departure, arrival, routes_db, countdown, bounty_hunters):
        super().__init__(countdown, bounty_hunters)
        self.autonomy = autonomy
        self.departure = departure
        self.arrival = arrival
        self.routes_db = routes_db


    def read_ROUTES(self):
        # Create a SQL connection to our SQLite database
        con = sqlite3.connect(self.routes_db)
        routes = pd.read_sql_query("SELECT * from ROUTES", con)

        return routes

    def create_Graph(self):
        # create the SQLite table
        routes = self.read_ROUTES()

        # create an empty graph
        Graph = nx.Graph()

        # iterate over the rows of the dataframe and add an edge to the graph 
        for _, row in routes.iterrows():
            Graph.add_edge(row['origin'], row['destination'], distance = row['travel_time'])

        return Graph


    def find_feasible_paths(self):
        # Find all feasible paths that satisfy the constraint of millennium falcon's autonomy

        # create an the associated graph
        G = self.create_Graph()

        # From all paths from departure to arrival
        all_paths = all_simple_paths(G, self.departure, self.arrival) 
        feasible_paths = {}

        # Find all feasible paths that satisfy the constraint of millennium falcon's autonomy
        for idx,path in enumerate(all_paths):
            actual_autonomy = self.autonomy 
            travel_days = 0
            stops = [self.departure]
            days = [0]
            for u, v in zip(path[:-1], path[1:]):
                if G.get_edge_data(u, v)['distance'] <= self.autonomy:
                    travel_days += G.get_edge_data(u, v)['distance']
                    days.append(travel_days)
                    stops.append(v)
                    actual_autonomy = self.autonomy - G.get_edge_data(u, v)['distance']
                    if actual_autonomy == 0:
                        stops.append(v)
                        travel_days += 1
                        days.append(travel_days)
                        actual_autonomy = self.autonomy
            feasible_paths['path_'+str(idx+1)] = [stops, days]
        return feasible_paths

    def find_acceptable_paths(self):
        # Find all acceptable paths such that the Millennium falcon reaches Endor before countdown
        feasible_paths = self.find_feasible_paths()
        acceptable_paths = {key: value for key, value in feasible_paths.items() if value[1][-1] <= self.countdown}
        return acceptable_paths


    def find_alternative_paths(self):
        # Find all alternative paths when there cooldown days between the expected arrival and countdown

        acceptable_paths = self.find_acceptable_paths()
        alternative_paths = {}

        for key, value in acceptable_paths.items():
            path, day = value[0], value[1]
            possible_rest = self.countdown - day[-1]
            if possible_rest >= 1: 
                rest = 1

                for idx, stop in enumerate(list(set(path[:-1]))):
                    path_dup = path.copy()
                    day_dup = day.copy()
                    path_dup.insert(idx+1, stop*rest)
                    day_dup.insert(idx+1, day_dup[idx]+1)
                    day_dup[(idx+2):] = [x + 1 for x in day_dup[(idx+2):]]
                    alternative_paths[key+str(idx+1)] = [path_dup, day_dup]
                
        return alternative_paths


    def give_me_the_odds(self):
        # Compute the odds that the Millennium Falcon reaches Endor in time and saves the galaxy
        feasible_paths = self.find_feasible_paths()

        if len([[path,day] for path,day in feasible_paths.values() if day[-1] <= self.countdown])==0:
            # If the arrival day is above the countdown, then return 0 
            odds = 0
            optim_path = []
        else:
            # Otherwise, compute the positive odds of reaching Endor before the countdown
            acceptable_paths = self.find_acceptable_paths()
            alternative_paths = self.find_alternative_paths()

            # Add the alternative paths to acceptable paths
            acceptable_paths = {**acceptable_paths, **alternative_paths}
            

            k_table, final_paths = [], [] 
            for key, value in acceptable_paths.items():
                path, day = value[0], value[1] 
                k = 0
                n_path = len(path)
                for i in range(n_path):
                    for idx,bounty in enumerate(self.bounty_hunters):
                        if  bounty['planet'] == path[i] and  bounty['day'] == day[i]:
                            k+=1
                k_table.append(k)
                final_paths.append(path)

            k_min = min(k_table)
            optim_path = final_paths[k_table.index(k_min)]

            if k_min >= 1:
                prob = 1/10
                for j in range(1,k_min):
                    prob += 9**j/10**(j+1)
                odds = 100*(1-prob)
            else:
                odds = 100
        return odds, optim_path



if __name__ == "__main__": 
    input_frontend = 'exemple1/empire.json'
    Empire_json = pd.read_json(input_frontend, typ='series')
    empire = Empire(Empire_json.countdown, Empire_json.bounty_hunters)

    input_backend = 'exemple1/millennium-falcon.json'
    MF_json = pd.read_json(input_backend, typ='series') 
    millennium_falcon = Millennium_falcon(MF_json.autonomy, MF_json.departure, MF_json.arrival, MF_json.routes_db,
                                        empire.countdown, empire.bounty_hunters)

    result = Millennium_falcon.give_me_the_odds(millennium_falcon)
    odds = result[0]
    optim_path = result[1]
    print(odds)
    