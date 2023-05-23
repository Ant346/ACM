#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains an interface class `animator` along with concrete realizations, each of which is associated with a corresponding system.

Remarks: 

- All vectors are treated as of type [n,]
- All buffers are treated as of type [L, n] where each row is a vector
- Buffers are updated from bottom to top

"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter
from ..__init__ import ANIMATION_TYPES_SAVE_FORMATS

# !pip install svgpath2mpl matplotlib <-- to install this

from itertools import product
import mlflow
from matplotlib import animation
from rcognita.__utilities import on_key_press, on_close
from rcognita.visualization.dashboards import DashboardEmpty


class Animator:
    """
    Interface class of visualization machinery for simulation of system-controller loops.
    To design a concrete animator: inherit this class, override:
        | :func:`~animators.Animator.__init__` :
        | define necessary visual elements (required)
        | :func:`~animators.Animator.init_anim` :
        | initialize necessary visual elements (required)
        | :func:`~animators.Animator.animate` :
        | animate visual elements (required)

    Attributes
    ----------
    objects : : tuple
        Objects to be updated within animation cycle
    pars : : tuple
        Fixed parameters of objects and visual elements

    """

    def __init__(
        self,
        observation_dashboard,
        action_dashboard,
        objective_dashboard,
        system_visualization_dashboard=None,
        scenario=None,
        fps=50,
        max_video_length=20,
        subplot_grid_size=[2, 2],
        animation_max_size_mb=200,
    ):
        if system_visualization_dashboard is None:
            system_visualization_dashboard = DashboardEmpty()
        self.system_visualization_dashboard = system_visualization_dashboard
        self.observation_dashboard = observation_dashboard
        self.action_dashboard = action_dashboard
        self.objective_dashboard = objective_dashboard
        self.scenario = scenario
        self.subplot_grid_size = subplot_grid_size
        self.artists = []
        self.fps = fps
        self.max_video_length = max_video_length

        if scenario is not None and hasattr(scenario, "howanim"):
            self.animation_type = scenario.howanim
        else:
            self.animation_type = "live"

        self.animation_max_size_mb = animation_max_size_mb

        self.collect_dashboards(
            self.system_visualization_dashboard,
            self.observation_dashboard,
            self.objective_dashboard,
            self.action_dashboard,
        )

    def init_anim(self):
        # clear matplotlib cache
        plt.clf()
        plt.cla()
        plt.close()
        self.main_figure = plt.figure(figsize=(10, 10))
        self.axes_array = self.main_figure.subplots(*self.subplot_grid_size)
        if self.subplot_grid_size == [1, 1]:
            self.axes_array = np.array([[self.axes_array]])
        for r, c in product(
            range(self.subplot_grid_size[0]), range(self.subplot_grid_size[1])
        ):
            plt.sca(self.axes_array[r, c])  ####---Set current axes
            self.dashboards[self.get_index(r, c)].init_dashboard()

        return self.artists

    def update_dashboards(self, update_variant):
        for r, c in product(
            range(self.subplot_grid_size[0]), range(self.subplot_grid_size[1])
        ):
            self.dashboards[self.get_index(r, c)].update(update_variant)

        return self.artists

    def animate(self, frame_index):
        # for initital frame no simulation steps needed
        if frame_index == 0:
            return self.artists

        sim_status = self.scenario.step()
        SIMULATION_ENDED = sim_status == "simulation_ended"
        EPISODE_ENDED = sim_status == "episode_ended"
        ITERATION_ENDED = sim_status == "iteration_ended"

        if SIMULATION_ENDED:
            print("Simulation ended")
            self.anm.event_source.stop()

        elif EPISODE_ENDED:
            self.update_dashboards("episode")
        elif ITERATION_ENDED:
            self.update_dashboards("iteration")
        else:
            self.update_dashboards("step")

        return self.artists

    def connect_events(self):
        self.main_figure.canvas.mpl_connect(
            "key_press_event", lambda event: on_key_press(event, self.anm)
        )

        self.main_figure.canvas.mpl_connect("close_event", on_close)

    def play_live(self):
        self.init_anim()
        self.anm = animation.FuncAnimation(
            self.main_figure,
            self.animate_live,
            blit=True,
            interval=0,  # Interval in FuncAnimation is miliseconds between frames
            repeat=False,
        )

        self.connect_events()

        self.anm.running = True

        plt.show()

    def get_animation(self):
        estimated_n_frames_in_video = int(
            min(self.max_video_length, self.scenario.time_final) * self.fps
        )
        scenario_speedup = max(
            self.scenario.get_cache_len() // estimated_n_frames_in_video, 1
        )
        self.scenario.set_speedup(scenario_speedup)

        self.init_anim()
        self.anm = animation.FuncAnimation(
            self.main_figure,
            self.animate,
            blit=True,
            interval=round(
                1000 / self.fps
            ),  # Interval in FuncAnimation is miliseconds between frames
            repeat=False,
            frames=self.scenario.get_speeduped_cache_len(),
        )

        # if self.animation_type not in ANIMATION_TYPES_SAVE_FORMATS:
        #     self.connect_events()

        return self.anm

    def animate_live(self, frame_index):
        if frame_index == 0:
            return self.artists

        start_time = self.scenario.time
        while self.scenario.time - start_time < 1 / self.fps:
            sim_status = self.scenario.step()
            SIMULATION_ENDED = sim_status == "simulation_ended"
            EPISODE_ENDED = sim_status == "episode_ended"
            ITERATION_ENDED = sim_status == "iteration_ended"
            if SIMULATION_ENDED:
                print("Simulation ended")
                self.anm.event_source.stop()
            elif EPISODE_ENDED:
                self.update_dashboards("episode")
            elif ITERATION_ENDED:
                self.update_dashboards("iteration")

            if SIMULATION_ENDED or EPISODE_ENDED or ITERATION_ENDED:
                self.scenario.reload_pipeline()
                return self.artists

        self.update_dashboards("step")
        return self.artists

    def set_sim_data(self, **kwargs):
        """
        This function is needed for playback purposes when simulation data were generated elsewhere.
        It feeds data into the animator from outside.
        """
        self.__dict__.update(kwargs)

    def collect_dashboards(self, *dashboards):
        self.dashboards = dashboards
        for dashboard in self.dashboards:
            self.artists.extend(dashboard.artists)

    def get_index(self, r, c):
        return r * self.subplot_grid_size[1] + c

    def playback(self):
        estimated_n_frames_in_video = int(
            min(self.max_video_length, self.scenario.time_final) * self.fps
        )
        scenario_speedup = max(
            self.scenario.get_cache_len() // estimated_n_frames_in_video, 1
        )
        self.scenario.set_speedup(scenario_speedup)

        self.init_anim()
        self.anm = animation.FuncAnimation(
            self.main_figure,
            self.animate,
            blit=True,
            interval=round(
                1000 / self.fps
            ),  # Interval in FuncAnimation is miliseconds between frames
            repeat=False,
            frames=self.scenario.get_speeduped_cache_len(),
        )

        if self.animation_type not in ANIMATION_TYPES_SAVE_FORMATS:
            self.connect_events()

        self.anm.running = True

        if self.animation_type in ANIMATION_TYPES_SAVE_FORMATS:
            self.save_animation()
        else:
            plt.show()

    def save_animation(self):
        if self.animation_type == "html":
            plt.rcParams["animation.frame_format"] = "svg"
            plt.rcParams["animation.embed_limit"] = self.animation_max_size_mb
            with open(
                "animation.html",
                "w",
            ) as f:
                f.write(
                    f"<html><head><title>{self.__class__.__name__}</title></head><body>{self.anm.to_jshtml()}</body></html>"
                )
            mlflow.log_artifact("animation.html")
        elif self.animation_type == "mp4":
            writer = FFMpegWriter(
                fps=self.fps,
                codec="libx264",
                extra_args=["-crf", "27", "-preset", "ultrafast"],
            )
            self.anm.save(
                "animation.mp4",
                writer=writer,
            )
            mlflow.log_artifact("animation.mp4")
