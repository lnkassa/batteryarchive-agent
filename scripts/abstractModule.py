# coding: utf-8
# Copyright 2025 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

from abc import ABC, abstractmethod

class AbstractModule(ABC):
    def __init__():
        pass

    def set_tester(self):
        pass
        
    def set_path(self, path):
        pass
    
    def set_file_id(self):
        pass
    
    def set_file_type(self):
        pass

    def populate_metadata(self):
        return
    
    def create_cell_df(self, path, row):
        return