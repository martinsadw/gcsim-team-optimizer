import json
import multiprocessing
import os
import random
from collections import defaultdict
from pprint import pprint

import numpy as np

import reader
import stats


def fitness_worker(task_queue, result_queue, fitness_function, data, temp_actions_path=None):
    while True:
        item = task_queue.get()
        if item is None:
            break

        j, vector, iterations, validation_penalty, force_write = item
        result = fitness_function(vector, data, iterations=iterations, validation_penalty=validation_penalty,
                                  force_write=force_write, temp_actions_path=temp_actions_path)
        result_queue.put((j, result))
        task_queue.task_done()


def create_fitness_queue(fitness_function, data, num_workers=1, temp_actions_path=None):
    task_queue = multiprocessing.JoinableQueue()
    result_queue = multiprocessing.Queue()

    for i in range(num_workers):
        process = multiprocessing.Process(target=fitness_worker,
                                          args=(task_queue, result_queue, fitness_function, data, temp_actions_path))
        process.start()

    return task_queue, result_queue


def generate_individual(weights):
    individual = np.array([random.choices(range(len(weight)), weight, k=1)[0] for weight in weights])
    return individual


def genetic_algorithm(data, fitness_function, num_workers=2, output_dir='output'):
    stats_dict = dict()

    characters_data, weapons_data, artifacts_data, actions = data

    temp_actions_path = os.path.join(output_dir, 'temp_gcsim')
    os.makedirs(temp_actions_path, exist_ok=True)

    fitness_cache = defaultdict(int)
    runs_cache = defaultdict(int)
    task_queue, result_queue = create_fitness_queue(fitness_function, data, num_workers=num_workers,
                                                    temp_actions_path=temp_actions_path)

    quant_options = reader.get_equipment_vector_quant_options(weapons_data, artifacts_data, actions['team'])
    vector_length = len(quant_options)
    character_length = 6
    quant_characters = int(vector_length / character_length)

    num_iterations = 500
    population_size = 200
    selection_size = 40
    validation_penalty = 1
    gradient_update_frequency = 50
    evaluation_iterations = 10
    gradient_iterations = 1000
    final_iterations = 1000

    #############

    # # Generate population uniformly
    # population = np.array([[random.randrange(quant) for quant in quant_options] for i in range(population_size)])
    # population[0] = reader.get_team_vector(characters_data, weapons_data, artifacts_data, actions['team'])

    # Generate population with gradient
    population = np.empty((population_size, len(quant_options)), dtype=int)
    population[0] = reader.get_team_vector(characters_data, weapons_data, artifacts_data, actions['team'])
    print('Calculating team gradient...')
    team_gradient = stats.sub_stats_gradient(data, population[0], iterations=gradient_iterations, output_dir=output_dir)

    with open(os.path.join(output_dir, 'gradient.json'), 'w') as gradient_file:
        gradient_data = dict(zip(actions['team'], team_gradient))
        json_object = json.dumps(gradient_data, indent=4)
        gradient_file.write(json_object)

    equipments_score = reader.get_equipment_vector_weighted_options(data, team_gradient)
    population[1:] = [generate_individual(equipments_score) for _ in range(1, population_size)]

    #############

    fitness = np.empty((population_size,))
    for j in range(population_size):
        task_queue.put((j, population[j], evaluation_iterations, validation_penalty, False))

    task_queue.join()
    while not result_queue.empty():
        j, result = result_queue.get()

        cache_key = tuple(population[j])
        average_weight = runs_cache[cache_key] / (runs_cache[cache_key] + evaluation_iterations)
        fitness_cache[cache_key] = fitness_cache[cache_key] * average_weight + result * (1 - average_weight)
        runs_cache[cache_key] += evaluation_iterations

    for j in range(population_size):
        fitness[j] = int(fitness_cache[tuple(population[j])])

    # Sort the population using the fitness
    population_order = fitness.argsort()[::-1]
    population = population[population_order]
    fitness = fitness[population_order]
    print(fitness)

    for i in range(num_iterations):
        print('Iteration {i}/{max} ({percent:.2f}%)'
              .format(i=i, max=num_iterations, percent=(i / num_iterations) * 100))

        if (i + 1) % gradient_update_frequency == 0:
            print('Recalculating team gradient...')
            team_gradient = stats.sub_stats_gradient(data, population[0], iterations=gradient_iterations, output_dir=output_dir)
            pprint(team_gradient)
            equipments_score = reader.get_equipment_vector_weighted_options(data, team_gradient)

        new_population = population.copy()
        new_fitness = fitness.copy()
        # new_population[selection_size:] = 0
        # new_fitness[selection_size:] = 0

        for j in range(selection_size):
            task_queue.put((j, population[j], evaluation_iterations, validation_penalty, False))

        for j in range(selection_size, population_size):
            r = np.arange(vector_length)

            # # Random selection
            # parent_1 = population[random.randrange(population_size)]
            # parent_2 = population[random.randrange(population_size)]

            # Roulette selection
            parents = random.choices(range(len(fitness)), fitness, k=2)
            parent_1 = population[parents[0]]
            parent_2 = population[parents[1]]

            #############

            # # Two points crossover
            # cut_point1 = random.randrange(vector_length)
            # cut_point2 = random.randrange(vector_length)
            #
            # mask1 = r < cut_point1
            # mask2 = r < cut_point2
            # crossover_mask = mask1 ^ mask2
            #
            # new_individual = np.choose(crossover_mask, [parent_1, parent_2])

            # Character crossover
            c = random.randrange(quant_characters)
            character_mask = (r >= c * character_length) & (r < (c + 1) * character_length)

            new_individual = np.choose(character_mask, [parent_1, parent_2])

            #############

            # mutation = np.array([random.randrange(quant) for quant in quant_options])
            mutation = generate_individual(equipments_score)

            # # Random mutation
            # mutation_chance = 0.025
            # mutation_mask = (np.random.rand(vector_length) < mutation_chance)
            # new_individual = np.choose(mutation_mask, [new_individual, mutation])

            # Per character mutation
            c = random.randrange(quant_characters)
            character_mask = (r >= c * character_length) & (r < (c + 1) * character_length)
            mutation_chance = 0.1
            mutation_mask = (np.random.rand(vector_length) < mutation_chance) & character_mask
            new_individual = np.choose(mutation_mask, [new_individual, mutation])

            #############

            new_population[j] = new_individual

            task_queue.put((j, new_population[j], evaluation_iterations, validation_penalty, False))

        # Calculate the new population fitness
        task_queue.join()
        while not result_queue.empty():
            j, result = result_queue.get()

            cache_key = tuple(new_population[j])
            average_weight = runs_cache[cache_key] / (runs_cache[cache_key] + evaluation_iterations)
            fitness_cache[cache_key] = fitness_cache[cache_key] * average_weight + result * (1 - average_weight)
            runs_cache[cache_key] += evaluation_iterations

        for j in range(population_size):
            new_fitness[j] = int(fitness_cache[tuple(new_population[j])])

        # Sort the population using the fitness
        population_order = new_fitness.argsort()[::-1]
        new_population = new_population[population_order]
        new_fitness = new_fitness[population_order]

        population = new_population
        fitness = new_fitness
        # print('Quant evaluations:', stats_dict.get('evaluation', 0))
        # print('Quant invalid:', stats_dict.get('invalid', 0))
        print(f'Partial Fitness: {fitness[0]} (runs: {runs_cache[tuple(population[0])]})')
        print(f'Partial Build: {population[0]}')
        print(fitness)

    final_fitness = np.empty_like(fitness)
    for j in range(population_size):
        task_queue.put((j, population[j], final_iterations, 1, True))

    task_queue.join()
    while not result_queue.empty():
        j, result = result_queue.get()
        final_fitness[j] = result

    population_order = final_fitness.argsort()[::-1]
    population = population[population_order]
    final_fitness = final_fitness[population_order]

    print('Final Fitness:', final_fitness)
    print('Final Build:', population[0])

    # Kill all process
    # TODO(andre): Organize better when process are created and destroyed
    #  Right now the processes are left alive if the code breaks
    for i in range(num_workers):
        task_queue.put(None)

    return population[0], final_fitness[0]