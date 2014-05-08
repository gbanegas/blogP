# -*- coding: utf-8 -*-

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""

# Import your model modules here.
from cryptos.model.auth import User, Group, Permission
from cryptos.model.page import Page