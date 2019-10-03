import csv
import os
import sys

import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters


# Pretty print
pp_metrics = {'total_flows': 'Total', 'successful_flows': 'Successful', 'dropped_flows': 'Dropped',
              'in_network_flows': 'In network',
              'avg_path_delay_of_processed_flows' :'Avg path delay processed',
              'avg_ingress_2_egress_path_delay_of_processed_flows': 'Avg i2e path delay processed',
              'avg_end2end_delay_of_processed_flows':'Avg e2e path delay processed',
              'avg_node_load': 'Avg node load', 'avg_link_load': 'Avg link load'}
pp_yaxis = {'flow': 'Flows', 'delay': 'Delay', 'load': 'Load %'}
pp_algo = {'gpasp': 'GPASP', 'spr1': 'SP1', 'spr2': 'SPR2'}
pp_network = {'bics_34.graphml': 'BICS', 'dfn_58.graphml': 'DFN', 'intellifiber_73.graphml': 'Intellifiber'}


def get_data(data_path, metric_set_id):
    table = []
    with open(data_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            table.append(row)

    data = {'Ingress node percentage': [], pp_yaxis[metric_set_id]: [], 'Metrics': [], 'Algorithms': []}
    for row in table:
        data['Ingress node percentage'].append(float(row[0]))
        data[pp_yaxis[metric_set_id]].append(float(row[1]))
        data['Metrics'].append(pp_metrics[row[2]])
        data['Algorithms'].append(pp_algo[row[3]])
    return data


def main():
    scenario = sys.argv[1]
    network = sys.argv[2]
    metric_set_id = sys.argv[3]

    register_matplotlib_converters()
    sns.set(style="whitegrid")

    input_path = f'transformed/{scenario}/{network}/{metric_set_id}'
    output_path = f'plotted/{scenario}/{network}/{metric_set_id}'

    data = get_data(f'{input_path}/t-metrics.csv', metric_set_id)
    df = pd.DataFrame(data=data)
    sns_plot = sns.lineplot(x='Ingress node percentage', y=pp_yaxis[metric_set_id], hue='Metrics', style='Algorithms',
                            data=df)
    sns_plot.set_title(f'{pp_network[network]}')

    sns_plot.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    fig = sns_plot.get_figure()
    os.makedirs(f'{output_path}', exist_ok=True)
    fig.savefig(f'{output_path}/output.png', bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":
    main()