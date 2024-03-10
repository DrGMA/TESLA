# encoding: utf8
"""
This function is part of TESLA (Tool for automatic Earthquake low‐frequency Spectral Level estimAtion).

EUROPEAN UNION PUBLIC LICENCE v. 1.2
EUPL © the European Union 2007, 2016

Copyright (C) 2023 Guido Maria Adinolfi, University of Turin, Turin, Italy. For inquiries, contact: guidomaria.adinolfi@unito.it

Dependencies:
- numpy
- os
- pandas
- shutil
"""

import numpy as np
import pandas as pd
from tesla.class_spectra import Spectra
import os
import shutil


def SpectraSelection(SpectraList,cfg,phase,show_table=False):
    """
    Perform Spectra Selection based on specified criteria.

    Parameters:
        SpectraList (list): List of Spectra objects.
        cfg (dict): Configuration settings.
        phase (str): Seismic phase ('P' or 'S').
        show_table (bool): Whether to show the selection summary table.

    Returns:
        Spectra_sel (dict): Dictionary of selected Spectra objects.
        Spectra_not_sel (dict): Dictionary of rejected Spectra objects.

    Notes:
        - This function performs Spectra Selection on a list of Spectra objects based on specified criteria in the configuration file.
        - Selected and rejected Spectra objects are returned as separate dictionaries.
    """


    numb=[]
    id=[]
    dur_sig=[]
    len_sig_prePick=[]
    len_sig_afterPick=[]
    omega0=[]
    omega0_err=[]
    corn_frq=[]
    corn_frq_err=[]
    q_val=[]
    q_val_err=[]
    snr_perc=[]
    delta_omega=[]
    rms_fit=[]
    cost_func=[]
    rms_norm=[]

    for Spectra in SpectraList:


        if phase=='P':

            Pick=Spectra.Ppick
        else:

            Pick=Spectra.Spick

        numb.append(int(str(Spectra.id).split('.')[0]))
        sta=(str(Spectra.station))
        id.append(str(Spectra.id))
        dur_sig.append(float(Spectra.SigWindTimes[1]-Spectra.SigWindTimes[0]))
        len_sig_prePick.append(float(Pick-Spectra.SigWindTimes[0]))
        len_sig_afterPick.append(float(Spectra.SigWindTimes[1]-Pick))
        omega0.append(float(Spectra.CurveFit['Omega0']))
        omega0_err.append(float(Spectra.CurveFit['Omega0Err']))
        corn_frq.append(float(Spectra.CurveFit['Fc']))
        corn_frq_err.append(float(Spectra.CurveFit['FcErr']))
        q_val.append(float(Spectra.CurveFit['Q']))
        q_val_err.append(float(Spectra.CurveFit['QErr']))
        snr_perc.append(int(Spectra.SnrPerc))
        delta_omega.append(float(Spectra.CurveFit['DeltaOmega']))
        rms_fit.append(float(Spectra.CurveFit['Rms1']))
        cost_func.append(float(0))
        rms_norm.append(float(Spectra.CurveFit['Rms2']))

        

    #-----------------------------------------------------------------------------#
    #---Write the DataFrame---#


    #---Set the option to display the table, if show_table is True
    #pd.set_option('display.width', 100)
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    data = {'No.': numb  ,
    #           'Station': sta,
            'Signal_Window_Duration': dur_sig,
            'Len_Sig_PrePick': len_sig_prePick,
            'Len_Sig_AfterPick': len_sig_afterPick, 
            'Omega0': omega0,
            'Omega0_Error': omega0_err,
            'Corner_Frequency': corn_frq,
            'Corner_Frequency_Error': corn_frq_err,
            'Q': q_val,
            'Q_Error': q_val_err,
            'SNR_Percentage': snr_perc,
            'Delta_Omega': delta_omega,
            'RMS_CurveFit': rms_fit,
            'Cost_Function': cost_func,
            'RMS_Normalized': rms_norm}



    df = pd.DataFrame (data, columns = ['No.','Signal_Window_Duration', 'Len_Sig_PrePick',
        'Len_Sig_AfterPick','Omega0','Omega0_Error','Corner_Frequency','Corner_Frequency_Error',
        'Q', 'Q_Error', 'SNR_Percentage', 'Delta_Omega','RMS_CurveFit','Cost_Function',
        'RMS_Normalized'])

    #print("    ")


    #-----------------------------------------------------------------------------#
    #---Throw out the trash---#


    if cfg["SpectraSelection"]["CostFunctionClass"]:

        #---Remove results with any value equal to infinite (inf)---# 
        df = df[np.isfinite(df).all(1)]
        #print(df)

        #---Remove results with irrealistic values---# 
        frq_pre_fc = cfg["CurveFitting"]["PreFc"] * (1/cfg["SourceSpectra"]["Padding"])

        #df_=df
        df_=df.loc[(df['Corner_Frequency'] > frq_pre_fc + (1/df['Len_Sig_AfterPick'])) & (df['Corner_Frequency'] > cfg["SourceSpectra"]["Fmin"] ) & (df['Corner_Frequency'] < cfg["SourceSpectra"]["Fmax"] ) 
            & (df['Q'] > 0) & (df['Q'] < 1500) & (df['Delta_Omega'] > cfg["SpectraSelection"]["DeltaOmegaThr"])] 

        df__=df_.copy()

        #---Remove results with low SNR value---#
        df_snr=df_.loc[(df_['SNR_Percentage'] >= cfg["SourceSpectra"]["SnrPerc"])]

        if df_snr.empty:
            df_sel=df_snr.copy()
            df_all=df_snr.copy()

            #print('DataFrame is empty!')

        elif df_snr.shape[0]==1 :

            df_snr.loc[:, ['Cost_Function']]= 0.0
            df_all=df_snr.copy()
            df_sel=df_snr.loc[(df_snr['RMS_Normalized'] <= cfg["SpectraSelection"]["RmsNormThr"])]


        else:

            #---Calculate the Cost Function---#
            rms_fit_max=df_snr['RMS_CurveFit'].max()
            omega0_err_max=df_snr['Omega0_Error'].max()
            corn_frq_err_max=df_snr['Corner_Frequency_Error'].max()
            q_val_err_max=df_snr['Q_Error'].max()
            df_snr.eval("Cost_Function=(((RMS_CurveFit/@rms_fit_max)*1)+((Omega0_Error/@omega0_err_max)*1)+((Corner_Frequency_Error/@corn_frq_err_max)*1)+((Q_Error/@q_val_err_max)*1))/4",inplace=True)

            #---Sort the results in a ascending order according to Cost Function and RMS normalized values---#
            df_snr=df_snr.sort_values(['Cost_Function','RMS_Normalized'], ascending = (True,True))

            #---Normalize the Cost function values---#
            norm_cost_func=(df_snr['Cost_Function']-df_snr['Cost_Function'].min())/(df_snr['Cost_Function'].max()-df_snr['Cost_Function'].min())
            
            df_snr.loc[:, ['Cost_Function']]=norm_cost_func

            df_all=df_snr.copy()

            #---Select the best spectra according to the first quartile of Cost Function and to the value of SNR and normalized RMS---#
            q1=df_snr['Cost_Function'].quantile(cfg["SpectraSelection"]["Quant"])

            #df_sel=df_.loc[(df_['Cost_Function'] <= q1) & (df_['SNR_Percentage'] >= cfg["SourceSpectra"]["SnrPerc"]) & 
            #       (df_['RMS_Normalized'] <= cfg["SpectraSelection"]["RmsNormThr"]) ]
            df_sel=df_snr.loc[(df_snr['Cost_Function'] <= q1) & (df_snr['RMS_Normalized'] <= cfg["SpectraSelection"]["RmsNormThr"]) ]

    else:

        #---Remove results with any value equal to infinite (inf)---# 

        #---Remove results with irrealistic values---# 
        frq_pre_fc = cfg["CurveFitting"]["PreFc"] * (1/cfg["SourceSpectra"]["Padding"])

        #df_=df
        df_snr=df.loc[(df['Corner_Frequency'] > frq_pre_fc + (1/df['Len_Sig_AfterPick'])) & (df['SNR_Percentage'] >= cfg["SourceSpectra"]["SnrPerc"])]  


        if df_snr.empty:
            df_sel=df_snr.copy()
            df_all=df_snr.copy()

            #print('DataFrame is empty!')

        elif df_snr.shape[0]==1 :

            df_all=df_snr.copy()
            df_sel=df_snr.loc[(df_snr['RMS_Normalized'] <= cfg["SpectraSelection"]["RmsNormThr"])]

        else:

            #---Sort the results in a ascending order according only to RMS normalized values---#
            df_snr=df_snr.sort_values(['RMS_Normalized'], ascending = (True))


            df_snr.loc[:, ['Cost_Function']]= -999.0

            df_all=df_snr.copy()

            df_sel_=df_snr.loc[(df_snr['RMS_Normalized'] <= cfg["SpectraSelection"]["RmsNormThr"]) ]

            #---Select the best spectra according to the first quartile of Cost Function and to the value of SNR and normalized RMS---#
            q1=df_sel_['RMS_Normalized'].quantile(cfg["SpectraSelection"]["Quant"])

            df_sel=df_sel_.loc[(df_sel_['RMS_Normalized'] <= q1)]




    #---Clean the Spectra object list---#

    Spectra_sel=[]
    Spectra_not_sel=[]

    for num, Spectra in enumerate(SpectraList, start=0):

        if numb[num] in df_sel['No.'].tolist():

            index1=df_sel['No.'].tolist().index(numb[num])
            Spectra.CostFunction=df_sel["Cost_Function"].iloc[index1]
            Spectra.id=id[num]
            
            Spectra_sel.append(Spectra)
        
        if (numb[num] in df_all['No.'].tolist()) & (numb[num] not in df_sel['No.'].tolist()):

            index2=df_all['No.'].tolist().index(numb[num])
            Spectra.CostFunction=df_all["Cost_Function"].iloc[index2]
            Spectra.id=id[num]
            
            Spectra_not_sel.append(Spectra)

    #---Sort the Spectra object list in ascendig order according to the Cost Function value---#

    Spectra_sel.sort(key=lambda x: x.CostFunction)
    Spectra_not_sel.sort(key=lambda x: x.CostFunction)


    #---Make directories and save the results as csv files---#

    if not os.path.exists(phase):
        os.mkdir(phase)

    if os.path.exists(phase+'/'+sta+'/sel_spectra'):
        shutil.rmtree(phase+'/'+sta+'/sel_spectra')

    if os.path.exists(phase+'/'+sta+'/not_sel_spectra'):
        shutil.rmtree(phase+'/'+sta+'/not_sel_spectra')


    if not os.path.exists(phase+'/'+sta):
        os.mkdir(phase+'/'+sta)

    if not os.path.exists(phase+'/'+sta+'/not_sel_spectra'):
        os.mkdir(phase+'/'+sta+'/not_sel_spectra')

    if not os.path.exists(phase+'/'+sta+'/sel_spectra'):
        os.mkdir(phase+'/'+sta+'/sel_spectra')





    df_sel.to_csv(phase+'/'+sta+"/sel_spectra/Source_Spectra.best."+sta+".csv", index=False)
    df_all.to_csv(phase+'/'+sta+"/sel_spectra/Source_Spectra.all."+sta+".csv", index=False)


    if show_table:

        #print(df_sel.to_string(index=False))
        print(" ")
        print(df_sel)



    return Spectra_sel, Spectra_not_sel