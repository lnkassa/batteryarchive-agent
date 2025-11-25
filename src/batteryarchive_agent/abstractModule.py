# coding: utf-8
# Copyright 2025 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

from abc import ABC, abstractmethod

class AbstractModule(ABC):
    def __init__():
        pass

    @abstractmethod
    def set_tester(self):
        pass
        
    @abstractmethod
    def set_path(self, path):
        pass
    
    @abstractmethod
    def set_file_id(self):
        pass
    
    @abstractmethod
    def set_file_type(self):
        pass

    @abstractmethod
    def calc_timeseries(self):
        return

    @abstractmethod
    def calc_cycle(self):
        return
    
    @abstractmethod
    def calc_cycle_quantities(self):
        return 
    
    @abstractmethod
    def populate_metadata(self):
        return
    
    @abstractmethod
    def create_df(self, path, row):
        return