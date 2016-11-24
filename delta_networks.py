#!/usr/bin/env python

from natsort import natsorted

import numpy as np
import matplotlib.pyplot as plt

import os, sys, argparse, itertools



def plot(num_plots, plot_num, data, data_std, initial_x, title, x_label, y_label):
    y_ticks = data.shape[0]
    num_nodes = data.shape[1]
    
    plt.subplot(num_plots * 2, 1, plot_num * 2 - 1)
    plt.imshow(data, cmap='hot', interpolation='nearest', extent=[initial_x, initial_x + num_nodes, y_ticks, 1])
    
    plt.title("%s" % title, fontsize=18)
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16)  
    plt.colorbar()
    
    plt.subplot(num_plots * 2, 1, plot_num * 2)
    plt.imshow(data_std, cmap='hot', interpolation='nearest', extent=[initial_x, initial_x + num_nodes, y_ticks, 1])
    
    plt.title("%s (Std Dev)" % title, fontsize=18)
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16) 
    plt.colorbar()


def main(args):
    reference = np.loadtxt(args.reference)
    reference_std = np.loadtxt(args.reference_std)
    alternatives = natsorted(args.alternatives)
    alternatives_std = natsorted(args.alternatives_std)
    
    assert len(alternatives) == len(alternatives_std), "The number of files supplied to the --alternatives argument differs from the number supplied to --alternatives-std"
    
    num_nodes = reference.shape[0]
    min_nodes = num_nodes
    
    y_ticks = []
    y_data = np.zeros((len(alternatives), num_nodes))
    y_data_std = np.zeros((len(alternatives), num_nodes))
    
    for i, a in enumerate(alternatives):
        alternative = np.loadtxt(a)
        alternative_std = np.loadtxt(alternatives_std[i])
        
        alt_nodes = alternative.shape[0]
        if alt_nodes != num_nodes:
            num_nodes = min(alt_nodes, num_nodes)
            log("Trimming data to %d nodes per network" % num_nodes)
            
            y_data = y_data[:,:num_nodes]
            y_data_std = y_data_std[:,:num_nodes]
            
            reference = reference[:num_nodes]
            alternative = alternative[:num_nodes]
            
            reference_std = reference[:num_nodes]
            alternative_std = alternative[:num_nodes]
        
        difference = alternative - reference
        difference_std = alternative_std - reference_std
        
        if args.absolute:
            difference = np.absolute(difference)
            difference_std = np.absolute(difference_std)
        
        y_data[i,:] = difference
        y_data_std[i,:] = difference_std
        
        y_ticks.append(".".join(os.path.basename(a).split(".")[:-1]))
    
    log("Plotting heat map: %s.png" % args.prefix)
    
    if args.split_pos:
        plt.subplots(figsize=(30, 16))
        plot(2, 1, y_data[:,:args.split_pos], y_data_std[:,:args.split_pos], args.initial_x_1, args.title_1, args.x_label, args.y_label)
        plot(2, 2, y_data[:,args.split_pos:], y_data_std[:,args.split_pos:], args.initial_x_2, args.title_2, args.x_label, args.y_label)
    else:
        plt.subplots(figsize=(30, 3))
        plot(1, 1, y_data, y_data_std, args.initial_x, args.title, args.x_label, args.y_label)
    
    plt.savefig("%s.png" % args.prefix, dpi=300, bbox_inches='tight')
    plt.close()   
    
    log("\n".join(y_ticks))



silent = False
stream = sys.stdout

def log(message):
    global silent
    global stream
    
    if not silent:
        print >> stream, message
    

if __name__ == "__main__":
    
    #parse cmd arguments
    parser = argparse.ArgumentParser()
    
    #standard arguments for logging
    parser.add_argument("--silent", help="Turn off logging", action='store_true', default=False)
    parser.add_argument("--log-file", help="Output log file (default: standard output)", default=None)
    
    #custom arguments
    parser.add_argument("--reference", help="The reference network (.dat)")
    parser.add_argument("--reference-std", help="The reference standard deviation network (.dat)")
    parser.add_argument("--alternatives", help="The alternative networks (.dat)", nargs="*")
    parser.add_argument("--alternatives-std", help="The alternative standard deviation networks (.dat) - should be in identical order as alternative networks", nargs="*", default=None)
    
    parser.add_argument("--title", help="Plot title")
    parser.add_argument("--x-label", help="Label for x-axis")
    parser.add_argument("--y-label", help="Label for y-axis")
    
    parser.add_argument("--initial-x", type=int, help="Start value for x-axis", default=1)
    
    parser.add_argument("--split-pos", type=int, help="Position to split the network at (for large networks)", default=None)
    parser.add_argument("--initial-x-1", type=int, help="Start value for x-axis on first graph", default=1)
    parser.add_argument("--initial-x-2", type=int, help="Start value for x-axis on second graph", default=1)
    parser.add_argument("--title-1", help="Title for first graph")
    parser.add_argument("--title-2", help="Title for second graph")
    
    parser.add_argument("--absolute", help="Set this flag to use absolute values in the heat map", action='store_true', default=False)
    
    parser.add_argument("--prefix", help="Prefix for output file", default="output")
    
    args = parser.parse_args()
    
    #set up logging
    silent = args.silent
    
    if args.log_file:
        stream = open(args.log_file, 'w')
    
    #run script
    main(args)
    
    #close logging stream
    stream.close()
    
 