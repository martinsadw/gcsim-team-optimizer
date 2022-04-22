import multiprocessing
import os
import random
from collections import defaultdict
from pprint import pprint

import numpy as np

import stats


def fitness_worker(task_queue, result_queue, fitness_function, data, actions, temp_actions_path=None):
    while True:
        item = task_queue.get()
        if item is None:
            break

        j, vector, iterations, validation_penalty, force_write = item
        result = fitness_function(vector, data, actions, iterations=iterations, validation_penalty=validation_penalty,
                                  force_write=force_write, temp_actions_path=temp_actions_path)
        result_queue.put((j, result))
        task_queue.task_done()


def create_fitness_queue(fitness_function, data, actions, num_workers=1, temp_actions_path=None):
    task_queue = multiprocessing.JoinableQueue()
    result_queue = multiprocessing.Queue()

    for i in range(num_workers):
        process_args = (task_queue, result_queue, fitness_function, data, actions, temp_actions_path)
        process = multiprocessing.Process(target=fitness_worker, args=process_args)
        process.start()

    return task_queue, result_queue


class GeneticAlgorithm:
    def __init__(self, data, fitness_function, num_workers=2):
        self.data = data
        self.fitness_function = fitness_function
        self.num_workers = num_workers
        self.task_queue = None
        self.result_queue = None

        self.num_iterations = 500
        self.population_size = 200
        self.selection_size = 40
        self.validation_penalty = 1
        self.gradient_update_frequency = 50
        self.evaluation_iterations = 10
        self.gradient_iterations = 1000
        self.final_iterations = 1000

        self.generation_method = 'gradient'
        self.selection_method = 'roulette'
        self.crossover_method = 'character'
        self.mutation_method = 'character'

        self.character_length = 6

        self.stats_dict = dict()
        self.fitness_cache = defaultdict(int)
        self.runs_cache = defaultdict(int)

        self.quant_options = None
        self.current_team = None
        self.team_gradient = None
        self.equipments_score = None

        self.temp_actions_path = os.path.join('actions', 'temp_gcsim')

    @staticmethod
    def generate_individual(weights):
        individual = np.array([random.choices(range(len(weight)), weight, k=1)[0] for weight in weights])
        return individual

    def generate_population(self):
        vector_length = len(self.quant_options)
        population = np.empty((self.population_size, vector_length), dtype=int)
        population[0] = self.current_team

        if self.selection_method == 'uniform':
            population[1:] = [[random.randrange(quant) for quant in self.quant_options]
                              for _ in range(1, self.population_size)]

        else:  # self.selection_method == 'gradient'
            population[1:] = [self.generate_individual(self.equipments_score)
                              for _ in range(1, self.population_size)]

        return population

    def calculate_population_fitness(self, population):
        fitness = np.empty((population.shape[0],))
        for i, individual in enumerate(population):
            self.task_queue.put((i, individual, self.evaluation_iterations, self.validation_penalty, False))

        self.task_queue.join()
        while not self.result_queue.empty():
            i, result = self.result_queue.get()

            cache_key = tuple(population[i])
            weight = self.runs_cache[cache_key] / (self.runs_cache[cache_key] + self.evaluation_iterations)
            self.fitness_cache[cache_key] = self.fitness_cache[cache_key] * weight + result * (1 - weight)
            self.runs_cache[cache_key] += self.evaluation_iterations

        for i, individual in enumerate(population):
            fitness[i] = int(self.fitness_cache[tuple(individual)])

        return fitness

    def selection(self, population, fitness):
        if self.selection_method == 'random':
            parent_1 = population[random.randrange(self.population_size)]
            parent_2 = population[random.randrange(self.population_size)]

        else:  # self.selection_method == 'roulette'
            parents = random.choices(range(len(fitness)), fitness, k=2)
            parent_1 = population[parents[0]]
            parent_2 = population[parents[1]]

        return parent_1, parent_2

    def crossover(self, parents):
        vector_length = len(parents[0])
        quant_characters = int(vector_length / self.character_length)
        r = np.arange(vector_length)

        if self.crossover_method == 'two_point':
            cut_point1 = random.randrange(vector_length)
            cut_point2 = random.randrange(vector_length)

            mask1 = r < cut_point1
            mask2 = r < cut_point2
            crossover_mask = mask1 ^ mask2

            new_individual = np.choose(crossover_mask, parents)

        else:  # self.crossover_method == 'character'
            c = random.randrange(quant_characters)
            character_mask = (r >= c * self.character_length) & (r < (c + 1) * self.character_length)

            new_individual = np.choose(character_mask, parents)

        return new_individual

    def mutation(self, individual):
        vector_length = len(individual)
        quant_characters = int(vector_length / self.character_length)
        r = np.arange(vector_length)

        # mutation = np.array([random.randrange(quant) for quant in self.quant_options])
        mutation = self.generate_individual(self.equipments_score)

        if self.mutation_method == 'random':
            mutation_chance = 0.025
            mutation_mask = (np.random.rand(vector_length) < mutation_chance)
            new_individual = np.choose(mutation_mask, [individual, mutation])

        else:  # self.mutation_method == 'character'
            c = random.randrange(quant_characters)
            character_mask = (r >= c * self.character_length) & (r < (c + 1) * self.character_length)
            mutation_chance = 0.1
            mutation_mask = (np.random.rand(vector_length) < mutation_chance) & character_mask
            new_individual = np.choose(mutation_mask, [individual, mutation])

        return new_individual

    def run(self, actions):
        os.makedirs(self.temp_actions_path, exist_ok=True)
        self.task_queue, self.result_queue = create_fitness_queue(self.fitness_function, self.data, actions,
                                                                  num_workers=self.num_workers,
                                                                  temp_actions_path=self.temp_actions_path)

        self.quant_options = self.data.get_equipment_vector_quant_options(actions['team'])
        self.current_team = self.data.get_team_vector(actions['team'])
        print('Calculating team gradient...')
        self.team_gradient = stats.sub_stats_gradient(self.data, actions, self.current_team,
                                                      iterations=self.gradient_iterations)
        pprint(self.team_gradient)
        self.equipments_score = self.data.get_equipment_vector_weighted_options(actions, self.team_gradient)

        population = self.generate_population()
        fitness = self.calculate_population_fitness(population)

        # Sort the population using the fitness
        population_order = fitness.argsort()[::-1]
        population = population[population_order]
        fitness = fitness[population_order]
        print(fitness)

        for i in range(self.num_iterations):
            print('Iteration {i}/{max} ({percent:.2f}%)'
                  .format(i=i, max=self.num_iterations, percent=(i / self.num_iterations) * 100))

            if (i + 1) % self.gradient_update_frequency == 0:
                print('Recalculating team gradient...')
                self.team_gradient = stats.sub_stats_gradient(self.data, actions, population[0],
                                                              iterations=self.gradient_iterations)
                pprint(self.team_gradient)
                self.equipments_score = self.data.get_equipment_vector_weighted_options(actions, self.team_gradient)

            new_population = population.copy()
            for j in range(self.selection_size, self.population_size):
                parents = self.selection(population, fitness)
                new_individual = self.crossover(parents)
                new_individual = self.mutation(new_individual)
                new_population[j] = new_individual

            new_fitness = self.calculate_population_fitness(new_population)

            # Sort the population using the fitness
            population_order = new_fitness.argsort()[::-1]
            new_population = new_population[population_order]
            new_fitness = new_fitness[population_order]

            population = new_population
            fitness = new_fitness
            # print('Quant evaluations:', stats_dict.get('evaluation', 0))
            # print('Quant invalid:', stats_dict.get('invalid', 0))
            print(f'Partial Fitness: {fitness[0]} (runs: {self.runs_cache[tuple(population[0])]})')
            print(f'Partial Build: {population[0]}')
            print(fitness)

        final_fitness = np.empty_like(fitness)
        for j in range(self.population_size):
            self.task_queue.put((j, population[j], self.final_iterations, 1, True))

        self.task_queue.join()
        while not self.result_queue.empty():
            j, result = self.result_queue.get()
            final_fitness[j] = result

        population_order = final_fitness.argsort()[::-1]
        population = population[population_order]
        final_fitness = final_fitness[population_order]

        print('Final Fitness:', final_fitness)
        print('Final Build:', population[0])

        # Kill all process
        # TODO(andre): Organize better when process are created and destroyed
        #  Right now the processes are left alive if the code breaks
        for i in range(self.num_workers):
            self.task_queue.put(None)

        return population[0], final_fitness[0]
