import json
import math
import multiprocessing
import os
import random
from collections import defaultdict
from pprint import pprint

import numpy as np

import processing


def fitness_worker(task_queue, result_queue, fitness_function, data, actions, temp_actions_path=None):
    while True:
        item = task_queue.get()
        if item is None:
            break

        j, vector, iterations, validation_penalty, force_write = item
        result = fitness_function(vector, data, actions, iterations=iterations, validation_penalty=validation_penalty,
                                  force_write=force_write, temp_actions_path=temp_actions_path)
        result_queue.put((j, result, iterations))
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
    def __init__(self, data, fitness_function, num_workers=2, output_dir='output'):
        self.data = data
        self.fitness_function = fitness_function
        self.num_workers = num_workers
        self.task_queue = None
        self.result_queue = None

        # Optimization Parameters
        self.num_iterations = 500
        self.population_size = 200
        self.selection_size = 40
        self.validation_penalty = 1
        self.gradient_update_frequency = 100
        self.initial_iterations = 2
        self.recurrent_iterations = 50
        self.max_iterations = 1000
        self.gradient_iterations = 1000
        self.final_iterations = 1000

        self.generation_method = 'gradient'
        self.selection_method = 'roulette'
        self.crossover_method = 'character'
        self.mutation_method = 'character'

        self.character_length = 6

        # Cache Data
        self.stats_dict = dict()
        self.sum_cache = defaultdict(float)
        self.sum_sq_cache = defaultdict(float)
        self.runs_cache = defaultdict(int)
        self.fitness_cache = defaultdict(float)

        # Final results
        self.best_key = ()
        self.best_fitness = 0
        self.best_dev = 0

        # Final Stats
        self.overrun_count = 0
        self.non_competitive_count = 0
        self.repeated_count = 0
        self.initial_fitness_count = 0
        self.normal_fitness_count = 0

        # Historical Data
        self.top_individuals_hist = []
        self.top_fitness_hist = []
        self.top_error_hist = []
        self.top_runs_hist = []
        self.overrun_hist = []
        self.non_competitive_hist = []
        self.repeated_hist = []
        self.initial_fitness_hist = []
        self.normal_fitness_hist = []

        # State Variables
        self.quant_options = None
        self.base_team = None
        self.fixed_equipments = None
        self.equipment_restriction_mask = None
        self.team_gradient = None
        self.equipments_score = None

        # Output Variables
        self.output_dir = output_dir
        self.temp_actions_path = os.path.join(self.output_dir, 'temp_gcsim')

        self.summary_size = 10

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['task_queue']
        del state['result_queue']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.task_queue = None
        self.result_queue = None

    def get_deviation_cache(self, key):
        variance = (self.sum_sq_cache[key] / self.runs_cache[key]) - (self.sum_cache[key] / self.runs_cache[key]) ** 2
        return math.sqrt(variance)

    def generate_deviation_cache(self):
        return {key: self.get_deviation_cache(key) for key in self.runs_cache.keys()}

    def get_error_cache(self, key):
        return self.get_deviation_cache(key) / math.sqrt(self.runs_cache[key])

    def generate_error_cache(self):
        return {key: self.get_error_cache(key) for key in self.runs_cache.keys()}

    def get_stats(self, key):
        return self.fitness_cache[key], self.get_error_cache(key), self.runs_cache[key]

    def get_top_keys(self, quant, sort=False):
        all_keys = list(self.fitness_cache.keys())
        all_fitness = list(self.fitness_cache.values())

        top_fitness_index = np.argpartition(all_fitness, -quant)[-quant:]
        if sort:
            top_fitness = np.array(all_fitness)[top_fitness_index]
            top_fitness_order = np.argsort(top_fitness)[::-1]
            top_fitness_index = top_fitness_index[top_fitness_order]

        top_keys = np.array(all_keys)[top_fitness_index]

        return top_keys

    @staticmethod
    def generate_individual(weights):
        individual = np.array([random.choices(range(len(weight)), weight, k=1)[0] for weight in weights])
        return individual

    def generate_population(self):
        vector_length = len(self.quant_options)
        population = np.empty((self.population_size, vector_length), dtype=int)
        population[0] = self.base_team

        if self.selection_method == 'uniform':
            population[1:] = [[random.randrange(quant) for quant in self.quant_options]
                              for _ in range(1, self.population_size)]

        else:  # self.selection_method == 'gradient'
            population[1:] = [self.generate_individual(self.equipments_score)
                              for _ in range(1, self.population_size)]

        population = np.choose(self.equipment_restriction_mask, [population, self.fixed_equipments])
        return population

    def calculate_population_fitness(self, population):
        cache_lock = set()

        fitness = np.empty((population.shape[0],))
        for i, individual in enumerate(population):
            cache_key = tuple(population[i])
            if cache_key in cache_lock:
                self.repeated_count += 1
                continue
            cache_lock.add(cache_key)

            if self.runs_cache[cache_key] > self.max_iterations:
                self.overrun_count += 1
                continue

            if self.runs_cache[cache_key] < self.initial_iterations:
                self.task_queue.put((i, individual, self.initial_iterations, self.validation_penalty, True))
                self.initial_fitness_count += 1
                continue

            mean = self.fitness_cache[cache_key]
            dev = self.get_deviation_cache(cache_key)
            if mean + dev < self.best_fitness - self.best_dev:
                self.non_competitive_count += 1
                continue

            self.task_queue.put((i, individual, self.recurrent_iterations, self.validation_penalty, True))
            self.normal_fitness_count += 1

        self.task_queue.join()
        while not self.result_queue.empty():
            i, result, iterations = self.result_queue.get()
            mean = float(result['mean'])
            dev = float(result['std'])

            # Reference: https://math.stackexchange.com/a/1379804
            cache_key = tuple(population[i])
            self.sum_cache[cache_key] += mean * iterations
            self.sum_sq_cache[cache_key] += (dev ** 2 + mean ** 2) * iterations
            self.runs_cache[cache_key] += iterations
            self.fitness_cache[cache_key] = self.sum_cache[cache_key] / self.runs_cache[cache_key]

        self.best_key, self.best_fitness = max(self.fitness_cache.items(), key=lambda obj: obj[1])
        self.best_dev = self.get_deviation_cache(self.best_key)

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

        # TODO(rodrigo): Add mutation_chance as a parameter
        if self.mutation_method == 'random':
            mutation_chance = 0.025
            mutation_mask = (np.random.rand(vector_length) < mutation_chance)
            new_individual = np.choose(mutation_mask, [individual, mutation])

        else:  # self.mutation_method == 'character'
            c = random.randrange(quant_characters)
            character_mask = np.logical_and((r >= c * self.character_length), (r < (c + 1) * self.character_length))
            mutation_chance = 0.1
            mutation_mask = np.logical_and(np.random.rand(vector_length) < mutation_chance, character_mask)
            mutation_mask = np.logical_and(~self.equipment_restriction_mask, mutation_mask)
            new_individual = np.choose(mutation_mask, [individual, mutation])

        return new_individual

    def run(self, actions, restrictions=None):
        os.makedirs(self.temp_actions_path, exist_ok=True)
        map_slots = {
            'flower': 0,
            'plume': 1,
            'sands': 2,
            'goblet': 3,
            'circlet': 4,
        }
        current_team = self.data.get_team_vector(actions['team'])
        self.fixed_equipments = np.full((24,), -1, dtype=int)
        for character, slots in restrictions['strict'].items():
            for slot in slots:
                char_index = actions['team'].index(character)
                slot_index = map_slots[slot] + 1  # weapon shift
                equip_index = self.character_length * char_index + slot_index
                self.fixed_equipments[equip_index] = current_team[equip_index]

        self.equipment_restriction_mask = self.fixed_equipments >= 0

        self.task_queue, self.result_queue = create_fitness_queue(self.fitness_function, self.data, actions,
                                                                  num_workers=self.num_workers,
                                                                  temp_actions_path=self.temp_actions_path)

        self.quant_options = self.data.get_equipment_vector_quant_options(actions['team'])
        self.base_team = np.choose(
            self.equipment_restriction_mask,
            [current_team, self.fixed_equipments]
        )
        print('Calculating team gradient...')
        self.team_gradient = processing.sub_stats_gradient(self.data, actions, self.base_team,
                                                           iterations=self.gradient_iterations,
                                                           output_dir=self.output_dir)

        # TODO(rodrigo): Save last gradient instead of first
        with open(os.path.join(self.output_dir, 'gradient.json'), 'w') as gradient_file:
            gradient_data = dict(zip(actions['team'], self.team_gradient))
            json_object = json.dumps(gradient_data, indent=4)
            gradient_file.write(json_object)

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
                self.team_gradient = processing.sub_stats_gradient(self.data, actions, population[0],
                                                                   iterations=self.gradient_iterations,
                                                                   output_dir=self.output_dir)
                pprint(self.team_gradient)
                self.equipments_score = self.data.get_equipment_vector_weighted_options(actions, self.team_gradient)

            new_population = population.copy()
            new_population[:self.selection_size] = self.get_top_keys(self.selection_size)

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

            top_keys = self.get_top_keys(self.summary_size, sort=True)
            self.top_individuals_hist.append(top_keys)
            self.top_fitness_hist.append([self.fitness_cache[tuple(key)] for key in top_keys])
            self.top_error_hist.append([self.get_error_cache(tuple(key)) for key in top_keys])
            self.top_runs_hist.append([self.runs_cache[tuple(key)] for key in top_keys])

            self.overrun_hist.append(self.overrun_count)
            self.non_competitive_hist.append(self.non_competitive_count)
            self.repeated_hist.append(self.repeated_count)
            self.initial_fitness_hist.append(self.initial_fitness_count)
            self.normal_fitness_hist.append(self.normal_fitness_count)

            population = new_population
            fitness = new_fitness
            # print('Quant evaluations:', stats_dict.get('evaluation', 0))
            # print('Quant invalid:', stats_dict.get('invalid', 0))
            print(f'Partial Fitness: {fitness[0]} (runs: {self.runs_cache[tuple(population[0])]})')
            print(f'Partial Build: {population[0]}')
            print(f'Top {self.summary_size}:')
            for key in top_keys:
                dps, dev, runs = self.get_stats(tuple(key))
                print(f'- DPS[id={sum(key):04d}]: {dps:.2f} +- {dev:.2f} (runs: {runs})')

        final_fitness = np.empty_like(fitness)
        for j in range(self.population_size):
            self.task_queue.put((j, population[j], self.final_iterations, 1, True))

        self.task_queue.join()
        while not self.result_queue.empty():
            j, result, _ = self.result_queue.get()
            final_fitness[j] = float(result['mean'])

        population_order = final_fitness.argsort()[::-1]
        population = population[population_order]
        final_fitness = final_fitness[population_order]

        self.best_key = tuple(population[0])
        self.best_fitness = final_fitness[0]
        self.best_dev = self.get_deviation_cache(self.best_key)
        print('Final Fitness:', final_fitness[0])
        print('Final Build:', population[0])

        total_runs = 0
        above_100_runs = 0
        above_1000_runs = 0
        for runs in self.runs_cache.values():
            total_runs += runs
            above_100_runs += max(runs - 100, 0)
            above_1000_runs += max(runs - 1000, 0)

        print('Total runs:', total_runs)
        print('Runs above 100:', above_100_runs)
        print('Runs above 1000:', above_1000_runs)

        # Kill all process
        # TODO(andre): Organize better when process are created and destroyed
        #  Right now the processes are left alive if the code breaks
        for i in range(self.num_workers):
            self.task_queue.put(None)

        return population[0], final_fitness[0]
