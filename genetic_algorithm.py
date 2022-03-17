import os
import random

import numpy as np

import reader


def genetic_algorithm(data, fitness_function):
    stats = dict()

    characters_data, weapons_data, artifacts_data, actions = data

    temp_gcsim_path = os.path.join('actions', 'temp_gcsim')
    os.makedirs(temp_gcsim_path, exist_ok=True)

    fitness_cache = dict()

    quant_options = reader.get_equipment_vector_quant_options(weapons_data, artifacts_data, actions['team'])
    vector_length = len(quant_options)
    character_length = 6
    quant_characters = int(vector_length / character_length)

    best_fitness = -1
    best_vector = []

    num_iterations = 100
    population_size = 50
    selection_size = 20
    validation_penalty = 1

    population = np.array([[random.randrange(quant) for quant in quant_options] for i in range(population_size)])
    population[0] = reader.get_team_vector(characters_data, weapons_data, artifacts_data, actions['team'])
    fitness = np.apply_along_axis(fitness_function, 1, population, data,
                                  validation_penalty=validation_penalty, fitness_cache=fitness_cache, stats=stats)

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

        # Calculate the new population fitness
        new_fitness[selection_size:] = np.apply_along_axis(fitness_function, 1, new_population[selection_size:], data,
                                                           validation_penalty=validation_penalty,
                                                           fitness_cache=fitness_cache, stats=stats)

        # Sort the population using the fitness
        population_order = new_fitness.argsort()[::-1]
        new_population = new_population[population_order]
        new_fitness = new_fitness[population_order]

        if best_fitness < new_fitness[0]:
            best_fitness = new_fitness[0]
            best_vector = new_population[0]

        population = new_population
        fitness = new_fitness
        print('Quant evaluations:', stats.get('evaluation', 0))
        print('Quant invalid:', stats.get('invalid', 0))
        print('Partial Fitness:', best_fitness)
        print('Partial Build:', best_vector)

    final_fitness = np.apply_along_axis(fitness_function, 1, population, data,
                                        iterations=1000, force_write=True, stats=stats)
    population_order = final_fitness.argsort()[::-1]
    population = population[population_order]
    final_fitness = final_fitness[population_order]

    print('Final Fitness:', final_fitness)
    print('Final Build:', population[0])

    # return best_vector, best_fitness
    return population[0], final_fitness[0]