# encoding: utf8

"""
TESLA: A Tool for automatic Earthquake low‐frequency Spectral Level estimAtion

This script is part of the TESLA package, which stands for "Tool for automatic Earthquake low‐frequency Spectral Level estimAtion."
TESLA is designed to process seismic data and estimate low-frequency spectral levels of earthquake signals.

The package consists of several modules and functions that perform different processing steps, including waveform processing,
spectral selection, plotting, and saving results.

This script contains the main function that orchestrates the processing steps for different seismic phases and stations.

EUROPEAN UNION PUBLIC LICENCE v. 1.2
EUPL © the European Union 2007, 2016

Copyright (C) 2023 Guido Maria Adinolfi, University of Turin, Turin, Italy. For inquiries, contact: guidomaria.adinolfi@unito.it

Dependencies:
- argparse
- rich
- sys
- time
- yaml
"""


# Import necessary modules
from rich.console import Console
from rich.theme import Theme
from rich.markdown import Markdown
from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.traceback import install
from rich import inspect
from rich.table import Table
from rich.progress import Progress
import time
import sys
import yaml
import argparse
from tesla.calc_travel_time import *
from tesla.class_spectra import *
from tesla.curve_fitting import *
from tesla.load_object import *
from tesla.plot_spectra import *
from tesla.read_config import *
from tesla.save_object import *
from tesla.smooth import *
from tesla.source_spectrum_function import *
from tesla.spectra_processing import *
from tesla.spectra_selection import *
from tesla.waveform_processing import *

# Install the Rich traceback handler
from rich.traceback import install
install()

# Define a custom theme for the console
custom_theme = Theme({
    "info": "bold blue",
    "warning": "bold red",
    "danger": "bold black on red",
    "normal": "white"
})

# Create a Rich console instance with the custom theme
console = Console(theme=custom_theme, record=True, log_time_format='%Y-%m-%d %H:%M:%S.%f', file="")

# Define the main function that processes the data
def RunTesla(Event_id, Configuration_file):


    working_dir=os.getcwd()

    path_event_id=os.path.abspath(Event_id)

    Config_file=os.path.abspath(Configuration_file)

    os.chdir(path_event_id)

    # Display start processing message using Markdown
    MARKDOWN = """
# START PROCESSING
"""
    md = Markdown(MARKDOWN, justify="center", style="bold green blink")
    console.print(md)

    # Calculate the start time
    from time import process_time
    t1_start = process_time()

    # Import configuration file
    console.log("[info]INFO:[/info]     [normal]Importing Configuration File")
    try:
        config = import_config(Config_file, print_cfg=False)
    except:
        console.print_exception()
        console.save_html("logfile")
        

    console.print(" ")
    time.sleep(1) 
    
    # Calculate total tasks
    tot1 = len(config["SourceSpectra"]["Phase"]) * len(config["Files"]["stations"])
    tot2 = len(config["Files"]["stations"])
    
    # Initialize progress bar
    with Progress(auto_refresh=False, expand=True, speed_estimate_period=100) as progress:

        # Add tasks for progress tracking
        task1 = progress.add_task("[bold bright_red on grey3]OVERALL PROCESSING...", total=tot1)
        task2 = progress.add_task("[bold orange1]P Spectra Processing...", total=tot2)
        task3 = progress.add_task("[bold orange1]S Spectra Processing...", total=tot2)
        
        # Loop over phases and stations
        for phase in config["SourceSpectra"]["Phase"]:
            
            # Display phase information
            console.print(" ")
            console.rule("[bold magenta]" + phase + " Spectra", style="dim")
            console.log("[info]INFO:[/info]     [normal]Calculating " + phase + " Spectra")
            console.print(" ")

            for sta in config["Files"]["stations"]:
                if phase == "P":
                    progress.update(task1, advance=1)   
                    progress.update(task2, advance=1)   
                else:
                    progress.update(task1, advance=1)   
                    progress.update(task3, advance=1)

                console.print(" ")
                console.print(" ")
                console.print(" ")
                progress.refresh()
                console.print(" ")
                console.print(" ")
                
                console.print(Panel(Text(sta, justify="center",style="bold yellow"), title="Calculating "+phase+" Spectra for station", subtitle="Seismic Event: [bold grey50]"+Event_id))
                
                # Waveform Processing
                console.log("[info]INFO:[/info]     [normal]Waveform Processing")
                try:
                    SpectraList, Wvfrms, Consol = WaveformProcessing(config, sta, phase, console)
                    Consol = console
                except:
                    console.print_exception()
                    console.save_html("logfile")

                if not SpectraList:
                    continue

                # Spectra Selection
                console.log("[info]INFO:[/info]     [normal]Spectra Selection")
                try:
                    SpectraSelList, SpectraNotSelList = SpectraSelection(SpectraList, config, phase, show_table=False)
                except:
                    console.print_exception()
                    console.save_html("logfile")

                if not SpectraSelList:
                    console.log("[warning]WARNING:[/warning]  [normal]No Spectra for station %s" % (sta))
                    #time.sleep(1)


                # Plotting Selected Spectra
                if config["PlotFigure"]["OnlySpectraSel"]:
                    if SpectraSelList:
                        # Display selected spectra information
                        table = Table(title="Selected Spectrum", expand=True)
                        spectrum = SpectraSelList[0]
                        table.add_column("Id.", justify="center", style="magenta", no_wrap=True)
                        table.add_column("Sig Lenght", justify="center", style="green")
                        table.add_column("Perc SNR", justify="center", style="green")
                        table.add_column("Cost Function", justify="center", style="green")
                        table.add_column("Norm RMS", justify="center", style="green")
                        table.add_row(str(spectrum.id), str("%.2f" % (float((spectrum.SigWindTimes[1] - spectrum.SigWindTimes[0])))),
                                      str("%02d%%" % (spectrum.SnrPerc)), str("%.3f" % (spectrum.CostFunction)),
                                      str("%.3e" % (spectrum.CurveFit['Rms2'])))
                        console.print(table)
                        console.print("  ")

                        if config["PlotFigure"]["ShowFigure"] or config["PlotFigure"]["SaveFigure"]:
                            console.log("[info]INFO:[/info]     [normal]Plotting Selected Spectra ")
                            try:
                                PlotSpectraLoop(SpectraSelList, Wvfrms, config, sta, phase, console)
                            except:
                                console.print_exception()
                                console.save_html("logfile")

                            for png_file in glob.glob("*.png"):
                                shutil.move(png_file, phase + '/' + sta + '/sel_spectra')

                # Plotting Not Selected Spectra
                else:
                    if SpectraSelList:
                        # Display selected spectra information
                        table = Table(title="Selected Spectrum", expand=True)
                        spectrum = SpectraSelList[0]
                        table.add_column("Id.", justify="center", style="magenta", no_wrap=True)
                        table.add_column("Sig Lenght", justify="center", style="green")
                        table.add_column("Perc SNR", justify="center", style="green")
                        table.add_column("Cost Function", justify="center", style="green")
                        table.add_column("Norm RMS", justify="center", style="green")
                        table.add_row(str(spectrum.id), str("%.2f" % (float((spectrum.SigWindTimes[1] - spectrum.SigWindTimes[0])))),
                                      str("%02d%%" % (spectrum.SnrPerc)), str("%.3f" % (spectrum.CostFunction)),
                                      str("%.3e" % (spectrum.CurveFit['Rms2'])))
                        console.print(table)
                        console.print("  ")

                        # Plotting Selected Spectra
                        if config["PlotFigure"]["ShowFigure"] or config["PlotFigure"]["SaveFigure"]:
                            console.log("[info]INFO:[/info]     [normal]Plotting Selected Spectra ")
                            try:
                                PlotSpectraLoop(SpectraSelList, Wvfrms, config, sta, phase, console)
                            except:
                                console.print_exception()
                                console.save_html("logfile")

                            for png_file in glob.glob("*.png"):
                                shutil.move(png_file, phase + '/' + sta + '/sel_spectra')

                    if SpectraNotSelList:
                        # Plotting Not Selected Spectra
                        if config["PlotFigure"]["ShowFigure"] or config["PlotFigure"]["SaveFigure"]:
                            console.log("[info]INFO:[/info]     [normal]Plotting Not Selected Spectra ")
                            try:
                                PlotSpectraLoop(SpectraNotSelList, Wvfrms, config, sta, phase, console)
                            except:
                                console.print_exception()
                                console.save_html("logfile")

                            for png_file in glob.glob("*.png"):
                                shutil.move(png_file, phase + '/' + sta + '/not_sel_spectra')

                # Saving Spectra Objects (if configured)
                if config["SaveResult"]["SaveObject"]:
                    console.log("[info]INFO:[/info]     [normal]Saving Spectra Objects")
                    try:
                        SaveObject(SpectraNotSelList, phase + '/' + sta + '/sel_spectra/SpectraSelList.pkl')
                        SaveObject(SpectraNotSelList, phase + '/' + sta + '/not_sel_spectra/SpectraNotSelList.pkl')
                    except:
                        console.print_exception()
                        console.save_html("logfile")
        
        time.sleep(3)
        console.print(" ")
        console.print(" ")
        console.print(" ")
    console.print(" ")
    
    # Calculate end time and display end processing message
    t1_stop = process_time()
    MARKDOWN = """
# END PROCESSING
"""
    md = Markdown(MARKDOWN, justify="center", style="bold green blink")
    console.print(md)
    console.save_html("logfile")

    os.chdir(working_dir)

# # Entry point for the script
# if __name__ == '__main__':
#     # Get Event_id from command-line arguments
#     if len(sys.argv) < 2:
#         print("Usage: python main.py Event_id")
#         sys.exit(1)
#     Event_id = sys.argv[1]

#     # Call the main function with Event_id
#     main(Event_id)

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('-e', '--earthquake_id', action="store", help='Provide Earthquake Id', required=True)
        parser.add_argument('-c', '--configuration_file', action="store", help='Provide Configuration File', required=True)
        args = parser.parse_args()

        RunTesla(args.earthquake_id, args.configuration_file)


if __name__ == ' __main__':
          main()