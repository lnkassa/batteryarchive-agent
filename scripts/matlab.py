# coding: utf-8
# Copyright 2025 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

import numpy as np

from abstractFileType import AbstractFileType

class Matlab(AbstractFileType):

    def file_to_df():
        num_cells = batch['summary'].shape[0]
        bat_dict = {}
        for i in range(num_cells):
            cycle_dataframes = []
            cl = f[batch['cycle_life'][i,0]][()]
            summary_CY = np.hstack(f[batch['summary'][i,0]]['cycle'][0,:].tolist())
            cycles = f[batch['cycles'][i,0]]
            cycle_dict = {}
            no_cycles = cycles['I'].shape[0]
            for j in range(no_cycles):
                I = np.hstack((f[cycles['I'][j,0]][()]))
                Qc = np.hstack((f[cycles['Qc'][j,0]][()]))
                Qd = np.hstack((f[cycles['Qd'][j,0]][()]))
                T = np.hstack((f[cycles['T'][j,0]][()]))
                V = np.hstack((f[cycles['V'][j,0]][()]))
                #dQdV = np.hstack((f[cycles['discharge_dQdV'][j,0]][()]))
                t = np.hstack((f[cycles['t'][j,0]][()]))
                cd = {'I': I, 'Qc': Qc, 'Qd': Qd, 'T': T, 'V':V, 't':t}
                cycle_dict[str(j)] = cd
                df_cycle = pd.DataFrame(cd)
                df_cycle['cycle_number'] = summary_CY[j]
                cycle_dataframes.append(df_cycle)
        
            df_battery = pd.concat(cycle_dataframes)

            cell_dict = {'cycle_life': cl, 'summary': summary_CY, 'cycles': cycle_dict}
            key = 'b3c' + str(i)
            bat_dict[key] = cell_dict
            
        print(df_battery)
        return df_battery