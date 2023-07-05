from pyiceberg.catalog import Catalog
from .client import NessieClient


def create_nessie_iceberg_catalog(config: dict):
    class NessieCatalog(Catalog):
        def __init__(self):
            self.client = NessieClient(config)
    
    return NessieCatalog()