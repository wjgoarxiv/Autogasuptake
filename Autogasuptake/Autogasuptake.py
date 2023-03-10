#!/usr/bin/env python3 

# Import libraries
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys 
from tabulate import tabulate
import glob
import pyfiglet
from scipy.optimize import newton
from uniplot import plot

# Print the title
os.system('cls' if os.name == 'nt' else 'clear')
title = pyfiglet.figlet_format('AutoGasUptake', font='small')
print('\n')
print(title+'\n')
print('\n')
print('------------------------------------------------')
print('If you have any questions, please send your questions to my email.')
print('\nOr, please suggest errors and areas that need updating.')
print('\n 📨 woo_go@yahoo.com')
print('\nVisit https://github.com/wjgoarxiv/autogasuptake for more information.')
print('------------------------------------------------')

def main():
    # Read the settings from `settings.txt` file
    try:
        with open('settings.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('#'):
                    continue
                else:
                    line = line.split('=')
                    if line[0].strip() == 'directory':
                        input_dirloc = line[1].strip()
                    elif line[0].strip() == 'frequency':
                        data_freq = int(line[1].strip())
                    elif line[0].strip() == 'temperature':
                        exp_temp = float(line[1].strip())
                    elif line[0].strip() == 'tc':
                        Tc = float(line[1].strip())
                    elif line[0].strip() == 'pc':
                        Pc = float(line[1].strip())
                    elif line[0].strip() == 'omega':
                        omega = float(line[1].strip())
                    elif line[0].strip() == 'tunit':
                        tunit = line[1].strip()
                    elif line[0].strip() == 'graph-decorate':
                        graph_decorate = line[1].strip()
                    elif line[0].strip() == 'plot-type':
                        plot_type = line[1].strip()
                    elif line[0].strip() == 'include-title':
                        include_title = line[1].strip()
                    elif line[0].strip() == 'output-file-type':
                        output_file_type = line[1].strip()
                    elif line[0].strip() == 'eos':
                        eos = line[1].strip()
                    elif line[0].strip() == 'water-mass':
                        water_mass = float(line[1].strip())
                    elif line[0].strip() == 'clathrate-type':
                        clath_type = line[1].strip()

        # Check the validity of the settings
        if not os.path.isdir(input_dirloc):
            print('ERROR The directory that you specified does not exist.')
            sys.exit()
        if data_freq <= 0:
            print('ERROR The data collection frequency must be positive.')
            sys.exit()
        if exp_temp <= 0:
            print('ERROR The experimental temperature must be positive.')
            sys.exit()
        if Tc <= 0:
            print('ERROR The critical temperature must be positive.')
            sys.exit()
        if Pc <= 0:
            print('ERROR The critical pressure must be positive.')
            sys.exit()
        if tunit not in ['h', 'm', 's']:
            print('ERROR The time unit must be either h, m, or s.')
            sys.exit()
        if graph_decorate not in ['y', 'n']:
            print('ERROR The graph decoration option must be either y or n.')
            sys.exit()
        if include_title not in ['y', 'n']:
            print('ERROR The include title option must be either y or n.')
            sys.exit()
        if output_file_type not in ['png', 'pdf', 'svg']:
            print('ERROR The output file type must be either png, pdf, or svg.')
            sys.exit()
        if eos not in ['rk', 'pr']:
            print('ERROR The equation of state model must be either rk or pr.')
            sys.exit()
        if water_mass <= 0:
            print('ERROR The mass of water must be positive.')
            sys.exit()

    except FileNotFoundError:
        print('ERROR There is no `settings.txt` file in the current directory. I will make a new `settings.txt` file for you.')
        with open('settings.txt', 'w') as f:
            f.write("###################################\n")
            f.write("############ SETTINGS.TXT #############\n")
            f.write("###################################\n")
            f.write("# NOTE: This file should be located in the directory where you are executing the program. This can be done by typing `pwd` in the terminal. Check your current location. \n")
            f.write("# NOTE: You can mark `#` in front of the lines you don't want to use. \n")
            f.write("# NOTE: This file should be named as `settings.txt`. If isn't, the program cannot load the settings. \n")
            f.write("\n")
            f.write("###########################################################")
            f.write("\n")
            f.write("# Target directory where the raw data files are located. \n")
            f.write("directory = ./ \n")
            f.write("\n")
            f.write("# Data collection frequency (in ms); the value when you set in the LabVIEW program. \n")
            f.write("frequency = 60000 \n")
            f.write("\n")
            f.write("# Experimental temperature (in K) \n")
            f.write("temperature = 276.3 \n")
            f.write("\n")
            f.write("# Critical temperature of your interested gas (in K) \n")
            f.write("tc = 304.1 \n")
            f.write("\n")
            f.write("# Critical pressure of your interested gas (in bar) \n")
            f.write("pc = 73.8 \n")
            f.write("\n")
            f.write("# Acentric factor of your interested gas \n")
            f.write("omega = 0.239 \n")
            f.write("\n")
            f.write("# Time unit (h, m, or s) \n")
            f.write("tunit = h \n")
            f.write("\n")
            f.write("# Whether to decorate the graph with research figure style (options: y, n) \n")
            f.write("graph-decorate = y \n")
            f.write("\n")
            f.write("# Plot type (options: line, scatter) \n")
            f.write("plot-type = line \n")
            f.write("\n")
            f.write("# Whether to include the title in the graph (options: y, n) \n")
            f.write("include-title = y \n")
            f.write("\n")
            f.write("# Output file type (options: png, pdf, svg) \n")
            f.write("output-file-type = png \n")
            f.write("\n")
            f.write("# Equation of state model (options: rk, pr) \n")
            f.write("eos = rk \n")
            f.write("\n")
            f.write("# Water mass you used in the experiment (in g) \n")
            f.write("water-mass = 30 \n")
            f.write("\n")
            f.write("# Type of the clathrate (options: sI, sII, sH, SCS-I, TS–I, HS-I, and none) \n")
            f.write("clathrate-type = sI \n")
            f.write("\n")
        print('INFO The `settings.txt` file has been created. Please edit the file and run the program again.')
        sys.exit()

    # Set variables here
    water_mol = 18.01528 # g/mol
    R = 0.083145 # L bar / K mol (gas constant)
    cal_water_mol = water_mass / water_mol # mol

    # Show options selected by the user
    print('\n')
    print('------------------------------------------------')
    print('INFO The options that you selected are as follows:')
    print('* Raw csv file directory location: ', input_dirloc)
    print('* Data collection frequency: ', data_freq, 'ms')
    print('* Experimental temperature condition: ', exp_temp, 'K')
    print('* Critical temperature of your interested gas: ', Tc, 'K')
    print('* Critical pressure of your intereted gas: ', Pc, 'bar')
    print('* Acentric factor: ', omega)
    print('* Time unit: ', tunit)
    print('* Graph decoration: ', graph_decorate)
    print('* Plot type: ', plot_type)
    print('* Include title: ', include_title)
    print('* Output file type: ', output_file_type)
    print('* Equation of state model: ', eos)
    print('* Water mass: ', water_mass, 'g')
    print('* Water mol number: ', cal_water_mol, 'mol')
    print('* Type of the clathrate: ', clath_type)

    print('---------------------------------------------------------')
    print('INFO If these options are not correct, please adjust them in the `settings.txt` file.')

    ###############EOS FUNCTIONS################
    # Peng-Robinson EOS
    # Reference: https://github.com/CorySimon/PREOS

    def preos(Tc, omega, Pc, T, P):

        # build params in PREOS
        Tr = T / Tc  # reduced temperature
        a = 0.457235 * R**2 * Tc**2 / Pc
        b = 0.0777961 * R * Tc / Pc
        kappa = 0.37464 + 1.54226 * omega - 0.26992 * omega**2
        alpha = (1 + kappa * (1 - np.sqrt(Tr)))**2

        A = a * alpha * P / R**2 / T**2
        B = b * P / R / T

        # build cubic polynomial
        def g(z):
            """
            Cubic polynomial in z from EOS. This should be zero.
            :param z: float compressibility factor
            """
            return z**3 - (1 - B) * z**2 + (A - 2*B - 3*B**2) * z - (
                    A * B - B**2 - B**3)

        # Solve cubic polynomial for the compressibility factor
        z = newton(g, 1.0)  # compressibility factor
        rho = P / (R * T * z)  # density

        # fugacity coefficient comes from an integration
        fugacity_coeff = np.exp(z - 1 - np.log(z - B) - A / np.sqrt(8) / B * np.log(
                    (z + (1 + np.sqrt(2)) * B) / (z + (1 - np.sqrt(2)) * B)))
        
        return z, rho, fugacity_coeff

    # Redlich-Kwong EOS
    # Reference: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/16%3A_The_Properties_of_Gases/16.02%3A_van_der_Waals_and_Redlich-Kwong_Equations_of_State

    def rkos(Tc, Pc, T, P):
        # build params in RKOS
        Tr = T / Tc  # reduced temperature
        a =  0.42780 * R**2 * Tc**2.5 / Pc
        b = 0.086640 * R * Tc / Pc

        A = a * P / R**2 / T**2.5
        B = b * P / R / T

        # build cubic polynomial
        def g(z): 
            """
            Cubic polynomial in z from EOS. This should be zero.
            :param z: float compressibility factor
            """
            return z**3 - z**2 + (A - B - B**2) * z - A * B
        
        # Solve cubic polynomial for the compressibility factor
        z = newton(g, 1.0)  # compressibility factor
        rho = P / (R * T * z)  # density

        return z, rho
    ###############EOS FUNCTIONS################

    # Show the list of files in the selected directory:
    file_list = glob.glob(input_dirloc + '*.csv')
    file_list.sort()
    try:
        if len(file_list) == 0:
            raise Exception
        else:
            pass
    except:
        print("\nINFO There is no csv file in your directory. Please check the directory location.")
        print("INFO The program will stop.")
        exit()

    ### Label file numbers and show all the files
    file_num = []
    for i in range(len(file_list)):
        file_num.append(i)
    print(tabulate({'File number': file_num, 'File name': file_list}, headers='keys', tablefmt='psql'))

    file_number = int(input('INFO These are the files that are in the folder. Please type the file number that you want to use: '))
    try:
        print("INFO The file name that would be utilized is", file_list[file_number])
    except IndexError:
        print("ERROR Your input number is out of range. Please check the file number again.")
        print("ERROR The program will stop.")
        exit()

    # Checking data type whether it is object or not. If it is float64, the delimiter is ','. If it is object, the delimiter is ' '.
    if pd.read_csv(file_list[file_number], header=None, names=['Pressure (psi)', 'Cylinder volume (mL)']).dtypes[0] == 'float64':
        df = pd.read_csv(file_list[file_number], header=None, sep=',', names=['Pressure (psi)', 'Cylinder volume (mL)'])
    elif pd.read_csv(file_list[file_number], header=None, names=['Pressure (psi)', 'Cylinder volume (mL)']).dtypes[0] == 'object':
        df = pd.read_csv(file_list[file_number], header=None, sep=' ', names=['Pressure (psi)', 'Cylinder volume (mL)'])

    # Pressure unit conversion 
    df['Pressure (bar)'] = df['Pressure (psi)'] * 0.0689475729
    exp_pres = float(df['Pressure (bar)'][0])
    print("INFO The experimental pressure (logged in ISCOPump) is", exp_pres, "bar. Check if it is your intended pressure.")

    # Cylinder volume unit conversion
    df['Cylinder volume (L)'] = df['Cylinder volume (mL)'] * 0.001

    # Run preos and get the values
    if eos == "pr":
        print("INFO The Peng-Robinson equation of state is selected.")
        z = preos(Tc, omega, Pc, exp_temp, exp_pres)[0]
        rho = preos(Tc, omega, Pc, exp_temp, exp_pres)[1]
        fugacity_coeff = preos(Tc, omega, Pc, exp_temp, exp_pres)[2]
        print("INFO The z value was successfully calculated!")
        print("INFO The calculated z value is", z)

    elif eos == "rk":
        print("INFO The Redlich-Kwong equation of state is selected.")
        z = rkos(Tc, Pc, exp_temp, exp_pres)[0]
        rho = rkos(Tc, Pc, exp_temp, exp_pres)[1]
        print("INFO The z value was successfully calculated!")
        print("INFO The calculated z value is", z)

    else: 
        print("ERROR The equation of state is not selected. Please check the input again.")
        print("ERROR The program will stop.")
        exit()

    ###############CALCULATION################
    # 1. x-axis: time (hours)

    # There is no time column in the csv file. 
    # The user initially defined the data collection frequency (data_freq). According to this, the time column can be generated.

    # The number of data points
    data_num = len(df)

    # Make a new time column here
    if tunit == 'h':
        time = np.arange(0, data_num * data_freq, data_freq) / 3600000
        df['Time (h)'] = time
    elif tunit == 'm':
        time = np.arange(0, data_num * data_freq, data_freq) / 60000
        df['Time (min)'] = time
    elif tunit == 's':
        time = np.arange(0, data_num * data_freq, data_freq) / 1000
        df['Time (s)'] = time

    # 2. y-axis: gas uptake (mol of gas / mol of water) -> delta_n
        # Equation: delta_n = P * Delta_V / (R * T * z)
        # Delta_V = V2 - V1; V2 is the first value of the cylinder volume column, V1 is the current value of the cylinder volume column
        # But in some case, the cylinder volume might be oscillating at the beginning of the experiment. Therefore, the program must initially identifies the first value of the cylinder volume column that is not oscillating. 

        # Criteria: Check that whether the cylinder volume is increased. If it IS, then the first value of the cylinder volume is NOT the V2. 
    if df['Cylinder volume (L)'][0] < df['Cylinder volume (L)'][1]:
        print("INFO Note that the cylinder volume is increasing at the beginning of the experiment. The program will identify the first value of the cylinder volume that is not oscillating.")
        for i in range(len(df)):
            if df['Cylinder volume (L)'][i] < df['Cylinder volume (L)'][i+1]:
                pass
            else:
                break
        print("INFO The oscillated parts were truncated. The plot starts from the", i+1, "th data point.")
        df = df[i+1:]
    else: 
        pass

    # 3. Outlier detection
        # Sometimes, LABView might not be able to record the data properly. In this case, the cylinder volume might be 0.0.
        # In this case, the program will remove that row. 
    if df['Cylinder volume (L)'].min() == 0.0:
        print("INFO Note that the cylinder volume is 0.0 at some point. The program will remove this outlier.")
        df.drop(df[df['Cylinder volume (L)'] == 0.0].index, inplace=True)
    else:
        pass

    df['Delta_V (L)'] = df['Cylinder volume (L)'].iloc[0] - df['Cylinder volume (L)']

    # Make a new column for delta_n
    df['Gas uptake (mol of gas)'] = df['Pressure (bar)'] * df['Delta_V (L)'] / (R * exp_temp * z)
    df['Gas uptake (mol of gas / mol of water)'] = df['Gas uptake (mol of gas)'] / cal_water_mol
    print("INFO The data was successfully treated!")
    ###############CALCULATION################

    ###############GRAPH PLOTTER################
    # 0. Ask user to trim the data if they want
    # But first, by executing uniplot to show the brief plot of the data, the user can see whether they want to trim the data or not.
    if tunit == "h":
        print("\nINFO Xlabel: Time (h), Ylabel: Gas uptake (mol of gas / mol of water)")
        plot(df['Gas uptake (mol of gas / mol of water)'], df['Time (h)'], interactive = True)
    elif tunit == "m":
        print("\nINFO Xlabel: Time (min), Ylabel: Gas uptake (mol of gas / mol of water)")
        plot(df['Gas uptake (mol of gas / mol of water)'], df['Time (min)'], interactive = True)
    elif tunit == "s":
        print("\nINFO Xlabel: Time (s), Ylabel: Gas uptake (mol of gas / mol of water)")
        plot(df['Gas uptake (mol of gas / mol of water)'], df['Time (s)'], interactive = True)
    else: 
        pass
             
    # Note that if user set the start time, the program will count that point as 0. For instance, if user enters start time as 50 and end time as 500, the program will start the x-axis from 0 to 450.
    ask_trim = input("INFO Do you want to trim the data? (y/n): ")
    if ask_trim == 'y' or ask_trim == 'Y':
        if tunit == "h": 
            trim_start = float(input("INFO What is the start time (in hours) that you want to trim? (e.g. 0.5): "))
            trim_end = float(input("INFO What is the end time (in hours) that you want to trim? (e.g. 5): "))
            df_trimmed = df[(df['Time (h)'] >= trim_start) & (df['Time (h)'] <= trim_end)]
            df_trimmed = df_trimmed.copy()
            df_trimmed['Time (h)'] = df_trimmed['Time (h)'] - trim_start
            print("INFO The data was successfully trimmed!")
        elif tunit == "m":
            trim_start = float(input("INFO What is the start time (in minutes) that you want to trim? (e.g. 30): "))
            trim_end = float(input("INFO What is the end time (in minutes) that you want to trim? (e.g. 300): "))
            df_trimmed = df[(df['Time (min)'] >= trim_start) & (df['Time (min)'] <= trim_end)]
            df_trimmed = df_trimmed.copy()
            df_trimmed['Time (min)'] = df_trimmed['Time (min)'] - trim_start
            print("INFO The data was successfully trimmed!")
        elif tunit == "s":
            trim_start = float(input("INFO What is the start time (in seconds) that you want to trim? (e.g. 30): "))
            trim_end = float(input("INFO What is the end time (in seconds) that you want to trim? (e.g. 300): "))
            df_trimmed = df[(df['Time (s)'] >= trim_start) & (df['Time (s)'] <= trim_end)]
            df_trimmed = df_trimmed.copy()
            df_trimmed['Time (s)'] = df_trimmed['Time (s)'] - trim_start
            print("INFO The data was successfully trimmed!")
        else:
            pass
    elif ask_trim == 'n' or ask_trim == 'N':
        print("INFO The data will not be trimmed. The program will be continued.")

    # 1. Plot type selection
    # The program will ask the user first which kinds of plot they want to see (options: scatter, line, bar)

    # 2. Plot settings
    if plot_type == 'scatter':
        scatter_num = int(input("INFO How many dots do you want to include in the scatter plot? (Recommended: 20): "))
        if ask_trim == 'y' or ask_trim == 'Y':
            if scatter_num > len(df_trimmed):
                print("ERROR The number of dots is larger than the number of data points. Please check the input again.")
                print("ERROR The program will stop.")
                exit()
            total_data_num = len(df_trimmed)
            interval = int(total_data_num / scatter_num)
            df_trimmed = df_trimmed.iloc[::interval, :]
            print("INFO The scatter plot will include" , scatter_num, "dots.")
        elif ask_trim == 'n' or ask_trim == 'N':
            if scatter_num > len(df):
                print("ERROR The number of dots is larger than the number of data points. Please check the input again.")
                print("ERROR The program will stop.")
                exit()
            total_data_num = len(df)
            interval = int(total_data_num / scatter_num)
            df = df.iloc[::interval, :]
            print("INFO The scatter plot will include" , scatter_num, "dots.") 
    else:
        pass

    # Ask line width & line style
    from matplotlib import rcParams
    if plot_type == 'line':
        line_width = float(input("INFO What is the line width? (Recommended: 1.5): "))
        rcParams['lines.linewidth'] = line_width
    else:
        pass

    # 3. Graph decoration for scatter & line plots (optional)
    if graph_decorate == 'y' or graph_decorate == 'Y':

        # Graph size settings
        rcParams['figure.figsize'] = 6, 6

        # Font settings
        rcParams['font.family'] = 'sans-serif'

        # Check whether Arial or SF Pro Display are installed in the computer
        try:
            rcParams['font.sans-serif'] = ['SF Pro Display']
        except:
            try:
                rcParams['font.sans-serif'] = ['Arial']
            except:
                print("ERROR Note that Arial and SF Pro are not installed in the computer. The program will use the default font.")
                pass
        
        rcParams['font.size'] = 14
        rcParams['axes.titlepad'] = 10
        rcParams['axes.titleweight'] = 'bold'
        rcParams['axes.titlesize'] = 18

        # Axes settings
        rcParams['axes.labelweight'] = 'bold'
        rcParams['xtick.labelsize'] = 12
        rcParams['ytick.labelsize'] = 12
        rcParams['axes.labelsize'] = 16
        rcParams['xtick.direction'] = 'in'
        rcParams['ytick.direction'] = 'in'

        # Label should be far away from the axes
        rcParams['axes.labelpad'] = 8
        rcParams['xtick.major.pad'] = 7
        rcParams['ytick.major.pad'] = 7

        # Add minor ticks
        rcParams['xtick.minor.visible'] = True
        rcParams['ytick.minor.visible'] = True

    elif graph_decorate == 'n' or graph_decorate == 'N':
        pass

    else: 
        print('ERROR Incorrect input. Please enter "y" or "n".')
        sys.exit()

    if plot_type == 'line':
        # Plotting
        if ask_trim == 'y' or ask_trim == 'Y':
            if tunit == 'h':
                plt.plot(df_trimmed['Time (h)'], df_trimmed['Gas uptake (mol of gas / mol of water)'], color='black')
                plt.xlim(df_trimmed['Time (h)'].iloc[0], df_trimmed['Time (h)'].iloc[-1])
                plt.xlabel('Time (h)')
            elif tunit == 'm':
                plt.plot(df_trimmed['Time (min)'], df_trimmed['Gas uptake (mol of gas / mol of water)'], color='black')
                plt.xlim(df_trimmed['Time (min)'].iloc[0], df_trimmed['Time (min)'].iloc[-1])
                plt.xlabel('Time (min)')
            elif tunit == 's':
                plt.plot(df_trimmed['Time (s)'], df_trimmed['Gas uptake (mol of gas / mol of water)'], color='black')
                plt.xlim(df_trimmed['Time (s)'].iloc[0], df_trimmed['Time (s)'].iloc[-1])
                plt.xlabel('Time (s)')
        elif ask_trim == 'n' or ask_trim == 'N':
            if tunit == 'h':
                plt.plot(df['Time (h)'], df['Gas uptake (mol of gas / mol of water)'], color='black')
                plt.xlim(df['Time (h)'].iloc[0], df['Time (h)'].iloc[-1])
                plt.xlabel('Time (h)')
            elif tunit == 'm':
                plt.plot(df['Time (min)'], df['Gas uptake (mol of gas / mol of water)'], color='black')
                plt.xlim(df['Time (min)'].iloc[0], df['Time (min)'].iloc[-1])
                plt.xlabel('Time (min)')
            elif tunit == 's':
                plt.plot(df['Time (s)'], df['Gas uptake (mol of gas / mol of water)'], color='black')
                plt.xlim(df['Time (s)'].iloc[0], df['Time (s)'].iloc[-1])
                plt.xlabel('Time (s)')
        else: 
            print('ERROR Incorrect input. Please enter "y" or "n".')
            sys.exit()
        plt.ylabel('Gas uptake (mol of gas / mol of water)')
        plt.tight_layout()

        if include_title == 'y' or include_title == 'Y':
            plt.title(str(file_list[file_number]))
        elif include_title == 'n' or include_title == 'N':
            pass
        else: 
            print('ERROR Incorrect input. Please enter "y" or "n".')
            sys.exit()

        if clath_type == 'sI':
            plt.axhline(y=0.1739, color='black', linestyle='--', linewidth=1.5)
            plt.text(3, 0.176, 'Theoretical maximum value of gas uptake', color='black', fontsize=10)
            plt.ylim(0, 0.19)
        elif clath_type == 'sII':
            plt.axhline(clath_typeclath_typey=0.1765, color='black', linestyle='--', linewidth=1.5)
            plt.text(3, 0.18, 'Theoretical maximum value of gas uptake', color='black', fontsize=10)
            plt.ylim(0, 0.194)
        elif clath_type == 'sH':
            plt.axhline(y=0.1765, color='black', linestyle='--', linewidth=1.5)
            plt.text(3, 0.18, 'Theoretical maximum value of gas uptake', color='black', fontsize=10)
            plt.ylim(0, 0.194)
        elif clath_type == 'SCS-I':
            plt.axhline(y=0.04368, color='black', linestyle='--', linewidth=1.5)
            plt.text(3, 0.046, 'Theoretical maximum value of gas uptake', color='black', fontsize=10)
            plt.ylim(0, 0.05)
        elif clath_type == 'TS-I':
            plt.axhline(y=0.05814, color='black', linestyle='--', linewidth=1.5)
            plt.text(3, 0.061, 'Theoretical maximum value of gas uptake', color='black', fontsize=10)
            plt.ylim(0, 0.065)
        elif clath_type == 'HS-I':
            plt.axhline(y=0.075, color='black', linestyle='--', linewidth=1.5)
            plt.text(3, 0.078, 'Theoretical maximum value of gas uptake', color='black', fontsize=10)
            plt.ylim(0, 0.085)
        elif clath_type == 'none':
            plt.ylim(0, round(df['Gas uptake (mol of gas / mol of water)'].max() + 0.4 * df['Gas uptake (mol of gas / mol of water)'].max(), 2))
        else: 
            print('ERROR Incorrect input. Please enter "sI", "sII", "sH", "SCS-I", "TS-I", "HS-I", or "none".')
            sys.exit()

        # Save figure
        if output_file_type == 'png':
            plt.savefig(str(file_list[file_number]).replace('.csv', '.png'), dpi=300, bbox_inches='tight')
        elif output_file_type == 'pdf':
            plt.savefig(str(file_list[file_number]).replace('.csv', '.pdf'), bbox_inches='tight')
        elif output_file_type == 'svg':
            plt.savefig(str(file_list[file_number]).replace('.csv', '.svg'), bbox_inches='tight')
        else:
            print('ERROR Incorrect input. Please enter "png", "pdf", or "svg".')
            sys.exit()

        print("INFO The line graph was successfully saved! Please check the target folder.")

    elif plot_type == 'scatter':
        # Plotting
        if ask_trim == 'y' or ask_trim == 'Y':
            if tunit == 'h':
                plt.scatter(df_trimmed['Time (h)'], df_trimmed['Gas uptake (mol of gas / mol of water)'], color='black')
                plt.xlim(df_trimmed['Time (h)'].iloc[0], df_trimmed['Time (h)'].iloc[-1])
                plt.xlabel('Time (h)')
            elif tunit == 'm':
                plt.scatter(df_trimmed['Time (min)'], df_trimmed['Gas uptake (mol of gas / mol of water)'], color='black')
                plt.xlim(df_trimmed['Time (min)'].iloc[0], df_trimmed['Time (min)'].iloc[-1])
                plt.xlabel('Time (min)')
            elif tunit == 's':
                plt.scatter(df_trimmed['Time (s)'], df_trimmed['Gas uptake (mol of gas / mol of water)'], color='black')
                plt.xlim(df_trimmed['Time (s)'].iloc[0], df_trimmed['Time (s)'].iloc[-1])
                plt.xlabel('Time (s)')
        elif ask_trim == 'n' or ask_trim == 'N':
            if tunit == 'h':
                plt.scatter(df['Time (h)'], df['Gas uptake (mol of gas / mol of water)'], color='black')
                plt.xlim(df['Time (h)'].iloc[0], df['Time (h)'].iloc[-1])
                plt.xlabel('Time (h)')
            elif tunit == 'm':
                plt.scatter(df['Time (min)'], df['Gas uptake (mol of gas / mol of water)'], color='black')
                plt.xlim(df['Time (min)'].iloc[0], df['Time (min)'].iloc[-1])
                plt.xlabel('Time (min)')
            elif tunit == 's':
                plt.scatter(df['Time (s)'], df['Gas uptake (mol of gas / mol of water)'], color='black')
                plt.xlim(df['Time (s)'].iloc[0], df['Time (s)'].iloc[-1])
            plt.xlabel('Time (s)')
        else: 
            print('ERROR Incorrect input. Please enter "y" or "n".')
            sys.exit()
        plt.ylabel('Gas uptake (mol of gas / mol of water)')
        plt.tight_layout()

        if include_title == 'y' or include_title == 'Y':
            plt.title(str(file_list[file_number]))
        elif include_title == 'n' or include_title == 'N':
            pass
        else:
            print('ERROR Incorrect input. Please enter "y" or "n".')
            sys.exit()

        if clath_type == 'sI':
            plt.axhline(y=0.1739, color='black', linestyle='--', linewidth=1.5)
            plt.text(3, 0.176, 'Theoretical maximum value of gas uptake', color='black', fontsize=10)
            plt.ylim(0, 0.19)
        elif clath_type == 'sII':
            plt.axhline(y=0.1765, color='black', linestyle='--', linewidth=1.5)
            plt.text(3, 0.18, 'Theoretical maximum value of gas uptake', color='black', fontsize=10)
            plt.ylim(0, 0.194)
        elif clath_type == 'sH':
            plt.axhline(y=0.1765, color='black', linestyle='--', linewidth=1.5)
            plt.text(3, 0.18, 'Theoretical maximum value of gas uptake', color='black', fontsize=10)
            plt.ylim(0, 0.194)
        elif clath_type == 'SCS-I':
            plt.axhline(y=0.04368, color='black', linestyle='--', linewidth=1.5)
            plt.text(3, 0.046, 'Theoretical maximum value of gas uptake', color='black', fontsize=10)
            plt.ylim(0, 0.05)
        elif clath_type == 'TS-I':
            plt.axhline(y=0.05814, color='black', linestyle='--', linewidth=1.5)
            plt.text(3, 0.061, 'Theoretical maximum value of gas uptake', color='black', fontsize=10)
            plt.ylim(0, 0.065)
        elif clath_type == 'HS-I':
            plt.axhline(y=0.075, color='black', linestyle='--', linewidth=1.5)
            plt.text(3, 0.078, 'Theoretical maximum value of gas uptake', color='black', fontsize=10)
            plt.ylim(0, 0.085)
        elif clath_type == 'none':
            plt.ylim(0, round(df['Gas uptake (mol of gas / mol of water)'].max() + 0.4 * df['Gas uptake (mol of gas / mol of water)'].max(), 2))
        else: 
            print('ERROR Incorrect input. Please enter "sI", "sII", "sH", "SCS-I", "TS-I", "HS-I", or "none".')
            sys.exit()

        # Save figure
        if output_file_type == 'png':
            plt.savefig(str(file_list[file_number]).replace('.csv', '.png'), dpi=300, bbox_inches='tight')
        elif output_file_type == 'pdf':
            plt.savefig(str(file_list[file_number]).replace('.csv', '.pdf'), bbox_inches='tight')
        elif output_file_type == 'svg':
            plt.savefig(str(file_list[file_number]).replace('.csv', '.svg'), bbox_inches='tight')
        else:
            print('ERROR Incorrect input. Please enter "png", "pdf", or "svg".')
            sys.exit()

        print("INFO The scatter graph was successfully saved! Please check the target folder.")

    else:
        print('ERROR Incorrect input. Please enter "line" or "scatter".')
        sys.exit()
    ###############GRAPH PLOTTER################

    ###############DATA EXPORTER################
    # Export gas uptake data & miscellaneous info. into a new csv file in the target folder
    def data_exporter():
        # Create a new csv file
        df.to_csv(str(file_list[file_number]).replace('.csv', '_OUTDATA.csv'), header=True, index=True)
        print("INFO The gas uptake data was successfully exported! Please check the target folder.")

    # Execute
    data_exporter()
    ###############DATA EXPORTER################

if __name__ == "__main__":
    main()
