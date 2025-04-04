# coding: utf-8
# Copyright 2025 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.
from abc import ABC, abstractmethod

class abstractCell(ABC):
    def __init__(self):
        self.cell_metadata_table = ''
        self.cycle_metadata_table = ''
        self.timeseries_table = ''
        self.buffer_table = ''
        self.stats_table = ''

    @abstractmethod
    def set_md(self, md, ind):
        pass

    @abstractmethod
    def set_path(self, path):
        pass

    @abstractmethod
    def get_cell_id(self):
        return
    
    @abstractmethod
    def get_file_id(self):
        return
    
    @abstractmethod
    def get_file_type(self):
        return
   
    @abstractmethod
    def calc_timeseries(self):
        pass
    
    @abstractmethod
    def calc_stats(self):
        pass
    
    @abstractmethod
    def calc_cycle_quantities(self):
        pass
    
    @abstractmethod
    def populate_metadata(self): 
        return
