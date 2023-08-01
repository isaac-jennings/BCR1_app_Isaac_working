mpledef normalize_objectives(solutions):
    num_objectives = len(solutions[0]['objectives'])
    min_objectives = [float('inf')] * num_objectives
    max_objectives = [-float('inf')] * num_objectives

    for solution in solutions:
        for i in range(num_objectives):
            min_objectives[i] = min(min_objectives[i], solution['objectives'][i])
            max_objectives[i] = max(max_objectives[i], solution['objectives'][i])

    for solution in solutions:
        solution['normalizedObjectives'] = [
            (objective - min_objectives[index]) / (max_objectives[index] - min_objectives[index])
            for index, objective in enumerate(solution['objectives'])
        ]


def calculate_grid_indices(solutions, num_divisions):
    for solution in solutions:
        solution['gridIndex'] = [
            int(normalized_objective * num_divisions)
            for normalized_objective in solution['normalizedObjectives']
        ]


def calculate_grid_density(solutions, num_divisions):
    density_map = {}

    for solution in solutions:
        grid_key = ','.join(map(str, solution['gridIndex']))

        if grid_key in density_map:
            density_map[grid_key] += 1
        else:
            density_map[grid_key] = 1

    return density_map


def adaptive_grid_culling(solutions, desired_size, num_divisions):
    normalize_objectives(solutions)
    calculate_grid_indices(solutions, num_divisions)
    density_map = calculate_grid_density(solutions, num_divisions)
    try:
        solutions.sort(key=lambda x: (density_map[str(x['gridIndex'])], str(x['gridIndex'])))
    except KeyError:
        pass
    return solutions[:desired_size]

# Solutions = total number of current solutions before adapative grid reduction
# Desired size = preferred number of solutions 
# Number of divisions = number of divisions/segements for each dimension. For example, three dimensions will equate to 1000
# cubes. Density is irrelavant per cube, as some cubes may be empty.
# Reduction will focus on the densest cube, repeating reduction until desired size is reached.

import pandas as pd
import csv
df = pd.read_csv('summary_500.csv')
df = df.set_index('objectives').apply(lambda row: {row.name: row.values.tolist()}, axis=1).tolist()
culled = adaptive_grid_culling(df, 250, 50)

# Specify the CSV file path
csv_file_path = 'example_solution_reduction.csv'

keys = culled[0].keys()

with open(csv_file_path, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(culled)
