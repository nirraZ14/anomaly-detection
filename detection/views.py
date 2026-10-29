from django.shortcuts import render
import pandas as pd
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from main.plotting import Plotter
import ast  # Importing ast for safely evaluating strings containing Python literals

logger = logging.getLogger('main')

def determine_anomaly_class(n_predicted_anoms):
    if n_predicted_anoms == 0:
        return 'none'
    elif n_predicted_anoms > 1:
        return 'contextual'
    else:
        return 'point'

def index(request):
    
    results_path = 'F:\\project-A\\results\\2018-05-19_15.00.10.csv' 
    df = pd.read_csv(results_path)
    '''if not os.path.exists('plots'):
        os.makedirs('plots')'''
    plotter=Plotter(run_id="2018-05-19_15.00.10")
    graph_files={}
    for index, row in df.iterrows():
        # Generate the plot for each channel
        graph_file = plotter.plot_channel(row['chan_id'])  
        graph_files[row['chan_id']] = graph_file  # Store the plot
    results = []
 
    for index, row in df.iterrows():
        result = {
            'chan_id': row['chan_id'],
            'graph_file':graph_files[row["chan_id"]],
            'normalized_prediction_error': row['normalized_pred_error'],
            'n_predicted_anoms': row['n_predicted_anoms'],
            'num_test_values': row['num_test_values'],
            'anomaly_classes': determine_anomaly_class(row['n_predicted_anoms']), 
            'anom_scores':row['anom_scores'],
            'anomaly_sequences':row["anomaly_sequences"]
        }
        results.append(result)

    
    context = {
        'results': results
    }
    return render(request, 'detection/results.html', context)
'''
SMAP Channels
P-1, P-2, P-3, P-4, P-7, P-11, P-14

Likely related to the Passive Microwave Radiometer measurements, which are used to observe soil moisture.
S-1

Likely related to Soil Moisture Active Passive operations or specific sensors for monitoring soil moisture.
E-1 through E-13

These channels might be Electromagnetic sensors or data related to electromagnetic measurements or environmental observations.
A-1 through A-9

These could represent Anomaly detection channels or sensors related to detecting anomalies in the data.
D-1 through D-16

These channels may relate to Diagnostic measurements or data used for diagnosing the system's status and performance.
G-1 through G-7

These channels could represent General observations or measurements that don't fall into other categories, possibly related to various sensors on the satellite.
F-1 through F-5

Likely Flux measurements, related to the observation of various fluxes of energy or particles.
T-1 through T-13

These channels might be related to Thermal measurements, such as temperature or thermal emissions.
B-1

This could represent a specific Baseline or reference measurement.
MSL Channels (Curiosity Rover)
M-1 through M-7

These might represent Mars related measurements, such as atmospheric composition, radiation levels, or other Martian environmental data.
S-2

Likely related to Science experiments or sensors for scientific observations on Mars.
P-10, P-15

Could relate to specific Planetary measurements or observations related to Martian surface or atmospheric properties.
T-4 through T-13

Similar to SMAP, these channels might be related to Thermal measurements on Mars.
F-4 through F-8

These could represent different Flux measurements or other related observations.
C-1, C-2

These might be related to Camera data or Calibration measurements for imaging sensors.
D-14 through D-16

These channels could relate to specific Diagnostic measurements or data for analyzing rover systems.
def results(request):
    results_path = 'F:\\project-A\\results\\2018-05-19_15.00.10.csv'  # Adjust the path and filename as needed
    try:
        # Load results from the CSV file
        data = pd.read_csv(results_path)

        # Example of mapping channels to descriptions
        channel_descriptions = {
            'A-1': 'Temperature',
            'A-2': 'Pressure',
            'B-1': 'Humidity',
            "P-1, P-2, P-3, P-4, P-7, P-11, P-14":Passive Microwave Radiometer,

        }

        # Add descriptions to the DataFrame
        data['Description'] = data['chan_id'].map(channel_descriptions)

        # Collect true positives, false positives, and false negatives
        tp = data['true_positives'].sum()
        fp = data['false_positives'].sum()
        fn = data['false_negatives'].sum()

        # Log the final totals
        logger.info('Final Totals:')
        logger.info('True Positives: {}'.format(tp))
        logger.info('False Positives: {}'.format(fp))
        logger.info('False Negatives: {}'.format(fn))

        # Calculate precision and recall
        try:
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            logger.info('Precision: {0:.2f}'.format(precision))
            logger.info('Recall: {0:.2f}'.format(recall))
        except ZeroDivisionError:
            precision = recall = 0

        # Prepare context for rendering
        context = {
            'results': data.to_html(classes='table table-striped'),  # Convert DataFrame to HTML
            'tp': tp,
            'fp': fp,
            'fn': fn,
            'precision': precision,
            'recall': recall,
        }
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        context = {
            'error': str(e),
        }

    return render(request, 'detection/results.html', context)
    '''