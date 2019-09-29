import logging
import os


from datetime import datetime
from siminterface.simulator import Simulator
from algorithms.greedy.gpasp import GPASPAlgo

import sys
import yaml
import csv

log = logging.getLogger(__name__)


def main():
    scenario = sys.argv[1]
    run = sys.argv[2]
    network_path = sys.argv[3]
    network = os.path.basename(network_path)
    ingress = sys.argv[4]
    algo = sys.argv[5]

    args = {
        'network': network_path,
        'service_functions': '../../../params/services/3sfcs.yaml',
        'resource_functions': '../../../params/services/resource_functions',
        'config': f'configurations/{scenario}_{ingress}.yaml',
        'seed': int(run),
        'output_path': f'scenarios/{scenario}/{run}/{network}/{ingress}/{algo}'
    }

    os.makedirs(args['output_path'], exist_ok=True)

    logging.getLogger('coordsim').setLevel(logging.CRITICAL)
    logging.getLogger('coordsim.reader').setLevel(logging.CRITICAL)

    simulator = Simulator(test_mode=True)

    # Setup algorithm
    algo = GPASPAlgo(simulator)
    algo.init(os.path.abspath(args['network']),
              os.path.abspath(args['service_functions']),
              os.path.abspath(args['config']),
              args['seed'],
              args['output_path'],
              resource_functions_path=os.path.abspath(args['resource_functions']))
    # Execute orchestrated simulation
    algo.run()
    print(f'{scenario}-{run}-{os.path.basename(network)}-{ingress}-{algo}')

    # with open(f'{result_path}/out.csv', 'w') as outfile:
    #     writer = csv.writer(outfile)
    #     writer.writerow([1+int(run), 2+int(run), 3+int(run), 4+int(run), 5+int(run), 6+int(run)])


if __name__ == "__main__":
    main()