import multiprocessing
import os
import random

import numpy as np

import reader


def fitness_worker(task_queue, result_queue, fitness_function, data):
    while True:
        item = task_queue.get()
        if item is None:
            break

        j, vector, iterations, validation_penalty, force_write = item
        result = fitness_function(vector, data, iterations=iterations,
                                  validation_penalty=validation_penalty, force_write=force_write)
        result_queue.put((j, result))
        task_queue.task_done()


def create_fitness_queue(fitness_function, data, num_workers=1):
    task_queue = multiprocessing.JoinableQueue()
    result_queue = multiprocessing.Queue()

    for i in range(num_workers):
        multiprocessing.Process(target=fitness_worker, args=(task_queue, result_queue, fitness_function, data)).start()

    return task_queue, result_queue


def genetic_algorithm(data, fitness_function, num_workers=2):
    stats = dict()

    characters_data, weapons_data, artifacts_data, actions = data

    temp_gcsim_path = os.path.join('actions', 'temp_gcsim')
    os.makedirs(temp_gcsim_path, exist_ok=True)

    fitness_cache = dict()
    task_queue, result_queue = create_fitness_queue(fitness_function, data, num_workers=num_workers)

    quant_options = reader.get_equipment_vector_quant_options(weapons_data, artifacts_data, actions['team'])
    vector_length = len(quant_options)
    character_length = 6
    quant_characters = int(vector_length / character_length)

    best_fitness = -1
    best_vector = []

    num_iterations = 500
    population_size = 200
    selection_size = 40
    validation_penalty = 1

    population = np.array([[random.randrange(quant) for quant in quant_options] for i in range(population_size)])
    population[0] = reader.get_team_vector(characters_data, weapons_data, artifacts_data, actions['team'])

    fitness = np.empty((population_size,))
    for j in range(population_size):
        cache_key = tuple(population[j])
        if cache_key in fitness_cache:
            fitness[j] = fitness_cache[cache_key]
        else:
            task_queue.put((j, population[j], 10, validation_penalty, False))

    task_queue.join()
    while not result_queue.empty():
        j, result = result_queue.get()
        fitness[j] = result
        fitness_cache[tuple(population[j])] = result

    # Sort the population using the fitness
    population_order = fitness.argsort()[::-1]
    population = population[population_order]
    fitness = fitness[population_order]

    for i in range(num_iterations):
        print('Iteration {i}/{max} ({percent:.2f}%)'
              .format(i=i, max=num_iterations, percent=(i / num_iterations) * 100))

        new_population = population.copy()
        new_fitness = fitness.copy()
        # new_population[selection_size:] = 0
        # new_fitness[selection_size:] = 0

        print(fitness)
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

            # # Random mutation
            # mutation_chance = 0.025
            # mutation_mask = (np.random.rand(vector_length) < mutation_chance)
            # mutation = np.array([random.randrange(quant) for quant in quant_options])
            #
            # new_individual = np.choose(mutation_mask, [new_individual, mutation])

            # Per character mutation
            c = random.randrange(quant_characters)
            character_mask = (r >= c * character_length) & (r < (c + 1) * character_length)
            mutation_chance = 0.1
            mutation_mask = (np.random.rand(vector_length) < mutation_chance) & character_mask
            mutation = np.array([random.randrange(quant) for quant in quant_options])

            new_individual = np.choose(mutation_mask, [new_individual, mutation])

            new_population[j] = new_individual

            new_fitness[j] = 0
            cache_key = tuple(new_individual)
            if cache_key in fitness_cache:
                new_fitness[j] = fitness_cache[cache_key]
            else:
                task_queue.put((j, new_individual, 10, validation_penalty, False))

        # Calculate the new population fitness
        task_queue.join()
        while not result_queue.empty():
            j, result = result_queue.get()
            new_fitness[j] = result
            fitness_cache[tuple(new_population[j])] = result

        # Sort the population using the fitness
        population_order = new_fitness.argsort()[::-1]
        new_population = new_population[population_order]
        new_fitness = new_fitness[population_order]

        if best_fitness < new_fitness[0]:
            best_fitness = new_fitness[0]
            best_vector = new_population[0]

        population = new_population
        fitness = new_fitness
        # print('Quant evaluations:', stats.get('evaluation', 0))
        # print('Quant invalid:', stats.get('invalid', 0))
        print('Partial Fitness:', best_fitness)
        print('Partial Build:', best_vector)

    final_fitness = np.empty_like(fitness)
    for j in range(population_size):
        task_queue.put((j, population[j], 1000, 1, True))

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
    for i in range(num_workers):
        task_queue.put(None)

    # return best_vector, best_fitness
    return population[0], final_fitness[0]