#!/usr/bin/python
# -*- coding: utf-8 -*-

from model import Model
from view import View


class App:
    def __init__(self,
                 qApp
                 ):
        self.model = Model(self)
        self.view = View(self, qApp)
        while not self.model.check_workspace():
            self.view.show_error('Mauvais espace de travail',
                                 'Veuillez selectionner un espace de travail ou des donnees GTFS sont presentes')
            workspace = self.model.get_conf('WORKSPACE')
            workspace = self.view.open_workspace_selector(workspace)
            self.model.set_conf('WORKSPACE', workspace)
        if not self.model.check_workspace_ready():
            self.view.inform("Espace de travail non initialise",
                             "Votre espace de travail n'est pas initialise. Cette procedure dure environ 15 minutes. Validez pour continuer")
            lat = self.model.get_conf('CENTER_LAT')
            lon = self.model.get_conf('CENTER_LON')
            r = self.model.get_conf('RADIUS')
            self.view.ask_reduce_stops(lat, lon, r)

        default_config = 'stops-metro-train-bus'
        self.ask_plot_xy(default_config)
        self.refresh_stops(default_config)

    def build(self, lat, lon, r):
        if r > 0:
            self.model.set_conf('CENTER_LAT', lat)
            self.model.set_conf('CENTER_LON', lon)
            self.model.set_conf('RADIUS', r)
            self.model.reduce_stops()
        else:
            self.model.remove_csv('stops-reduced')
        self.model.build_time_expanded_model()
        self.model.build_condensed_model_from_time_expanded_model()
        self.model.build_alpha_beta_from_condensed_model()
        self.model.build_cuboid_from_model('time_expanded')
        self.model.build_cuboid_from_model('condensed')
        # self.model.build_cuboid_from_model('alphabeta')
        self.model.build_stops()

    def ask_plot_xy(self, filename):
        x, y = self.model.get_stops_xy(filename)
        self.view.plot_xy(x, y)

    def refresh_stops(self, filename):
        stops = self.model.get_stops_iterator(filename)
        self.view.fill_stops(stops)

    def bellman(self, mode_prefix, start_node, end_node, start_time='None'):
        self.model.bellman(mode_prefix, start_node, end_node, start_time)

    def show_result(self, results):
        self.view.show_result(results)

    def highlight_stops(self, stops):
        x, y = self.model.get_stops_xy(stop_ids=stops)
        self.view.draw_path(x, y, True)
