import numpy as np
from .animation_utils import (
    update_line,
    update_text,
)
from .markers import RobotMarker, LanderMarker
from abc import ABC, abstractmethod
from ..__utilities import rc
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Dashboard(ABC):
    def __init__(self):
        self.artists = []

    @abstractmethod
    def init_dashboard(self):
        pass

    def perform_step_update(self):
        pass

    def perform_episodic_update(self):
        pass

    def perform_iterative_update(self):
        pass

    def update(self, update_variant):
        if update_variant == "step":
            self.perform_step_update()
        elif update_variant == "episode":
            self.perform_episodic_update()
        elif update_variant == "iteration":
            self.perform_iterative_update()


class DashboardEmpty(Dashboard):
    def __init__(self):
        super().__init__()

    def init_dashboard(self):
        self.axes_3wrobot = plt.gca()


class DefaultDashboardActionOrObservation(Dashboard):
    def __init__(
        self,
        time_start,
        time_final,
        datum_init,
        scenario,
        datum_namings,
        dashboard_type="observation",
        x_max=10,
        x_min=-10,
        y_max=10,
        y_min=-10,
    ):
        super().__init__()
        self.time_start = time_start
        self.time_final = time_final
        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min
        self.dashboard_type = dashboard_type
        self.datum_init = datum_init
        self.datum_namings = (
            datum_namings
            if datum_namings is not None
            else [
                f"{i}-th component"
                for i in range(len(datum_init))
                if i < min(len(datum_init), 5)
            ]
        )
        if len(self.datum_init) != self.datum_namings:
            self.datum_init = self.datum_init[: len(self.datum_namings)]
            print("Passed datum_namings are not consistent with datum_init. Truncated.")

        self.scenario = scenario
        self.observation_lines = []

    def init_dashboard(self):
        self.main_axis = plt.gca()

        self.main_axis.autoscale(False)
        self.main_axis.set_xlim(self.time_start, self.time_final)
        self.main_axis.set_ylim(
            np.min([self.x_min, self.y_min]),
            np.max([self.x_max, self.y_max]),
        )
        self.main_axis.set_xlabel("Time [s]")

        self.main_axis.plot([self.time_start, self.time_final], [0, 0], "k--", lw=0.75)

        for x, name in zip(self.datum_init, self.datum_namings):
            (observation_line,) = self.main_axis.plot(
                self.time_start, x, lw=1, label=name
            )
            self.observation_lines.append(observation_line)
            self.artists.append(observation_line)

        self.main_axis.legend(fancybox=True, loc="upper right")

    def perform_step_update(self):
        data = (
            self.scenario.state_full
            if self.dashboard_type == "observation"
            else self.scenario.action
        )

        time = self.scenario.time

        for x, line in zip(
            data[: len(self.datum_namings)],
            self.observation_lines,
        ):
            update_line(line, time, x, axis_handle=self.main_axis)


class DefaultDashboardObjectives(Dashboard):
    def __init__(self, time_start, time_final, scenario):
        super().__init__()
        self.time_start = time_start
        self.time_final = time_final
        self.running_objective_init = 0
        self.total_objective_init = 0
        self.scenario = scenario

    def init_dashboard(self):
        self.axes_cost = plt.gca()

        self.axes_cost.set_xlim(self.time_start, self.time_final)
        self.axes_cost.set_ylim(0, 1e4)
        self.axes_cost.set_yscale("symlog")
        self.axes_cost.set_xlabel("Time [s]")
        self.axes_cost.autoscale(False)

        text_total_objective = r"""$\int \mathrm{{running\,obj.}} 
        \,\mathrm{{d}}t$ = {total_objective:2.3f}""".format(
            total_objective=0
        )
        self.text_total_objective_handle = self.axes_cost.text(
            0.05,
            0.5,
            text_total_objective,
            horizontalalignment="left",
            verticalalignment="center",
        )
        (self.line_running_obj,) = self.axes_cost.plot(
            self.time_start,
            self.running_objective_init,
            "r-",
            lw=0.5,
            label="Running obj.",
        )
        (self.line_total_objective,) = self.axes_cost.plot(
            self.time_start,
            0,
            "g-",
            lw=0.5,
            label=r"$\int \mathrm{running\,obj.} \,\mathrm{d}t$",
        )
        self.artists.append(self.line_running_obj)
        self.artists.append(self.line_total_objective)
        self.axes_cost.legend(fancybox=True, loc="upper right")

    def perform_step_update(self):
        time = self.scenario.time
        running_objective_value = np.squeeze(self.scenario.running_objective_value)
        total_objective = self.scenario.total_objective

        update_line(
            self.line_running_obj,
            time,
            running_objective_value,
            axis_handle=self.axes_cost,
        )
        update_line(
            self.line_total_objective, time, total_objective, axis_handle=self.axes_cost
        )
        text_total_objective = r"""$\int \mathrm{{running\,obj.}} \,\mathrm{{d}}t$ = {total_objective:2.1f}""".format(
            total_objective=np.squeeze(np.array(total_objective))
        )
        update_text(self.text_total_objective_handle, text_total_objective)


class RobotTrackingDasboard(Dashboard):
    def __init__(self, time_start, x_max, x_min, y_max, y_min, scenario):
        super().__init__()
        self.time_start = time_start
        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min
        state_init = scenario.state_init
        self.xCoord0, self.yCoord0, self.angle_deg0 = state_init[:3]
        self.scenario = scenario

    def init_dashboard(self):
        self.axes_3wrobot = plt.gca()

        self.axes_3wrobot.set_xlim(self.x_min, self.x_max)
        self.axes_3wrobot.set_ylim(self.y_min, self.y_max)
        self.axes_3wrobot.set_xlabel("x [m]")
        self.axes_3wrobot.set_ylabel("y [m]")
        self.axes_3wrobot.set_title("Pause - space, q - quit, click - data cursor")

        self.axes_3wrobot.set_aspect("equal", adjustable="box")
        self.axes_3wrobot.plot(
            [self.x_min, self.x_max], [0, 0], "k--", lw=0.75
        )  # Help line
        self.axes_3wrobot.plot(
            [0, 0], [self.y_min, self.y_max], "k--", lw=0.75
        )  # Help line
        (self.line_trajectory,) = self.axes_3wrobot.plot(
            self.xCoord0, self.yCoord0, "b--", lw=0.5
        )
        self.artists.append(self.line_trajectory)
        self.robot_marker = RobotMarker(angle=self.angle_deg0)
        text_time = f"Time = {self.time_start:2.3f}"
        self.text_time_handle = self.axes_3wrobot.text(
            0.05,
            0.95,
            text_time,
            horizontalalignment="left",
            verticalalignment="center",
            transform=self.axes_3wrobot.transAxes,
        )
        self.artists.append(self.text_time_handle)

        self.axes_3wrobot.format_coord = lambda state, observation: "%2.2f, %2.2f" % (
            state,
            observation,
        )
        self.scatter_sol = self.axes_3wrobot.scatter(
            self.xCoord0, self.yCoord0, marker=self.robot_marker.marker, s=400, c="b"
        )

    def perform_step_update(self):
        state = self.scenario.state_full
        time = self.scenario.time

        xCoord = state[0]
        yCoord = state[1]
        angle = state[2]
        angle_deg = angle / np.pi * 180
        text_time = f"Time = {time:2.3f}"

        update_text(self.text_time_handle, text_time)
        update_line(self.line_trajectory, xCoord, yCoord, axis_handle=self.axes_3wrobot)
        self.scatter_sol.remove()
        self.robot_marker.rotate(angle_deg)  # Rotate the robot on the plot
        self.scatter_sol = self.axes_3wrobot.scatter(
            xCoord, yCoord, marker=self.robot_marker.marker, s=400, c="b"
        )


class CartpoleTrackingDashboard(Dashboard):
    def __init__(self, time_start, rod_length, scenario):
        super().__init__()
        self.time_start = time_start
        self.rod_length = rod_length
        self.scenario = scenario
        self.state_init = scenario.state_init

    def init_dashboard(self):
        self.axes_rotating_pendulum = plt.gca()

        x_from = -self.rod_length - 0.2
        x_to = self.rod_length + 0.2
        y_from = x_from
        y_to = x_to
        self.axes_rotating_pendulum.autoscale(False)
        self.axes_rotating_pendulum.set_xlim(x_from, x_to)
        self.axes_rotating_pendulum.set_ylim(y_from, y_to)
        self.axes_rotating_pendulum.set_xlabel("x [m]")
        self.axes_rotating_pendulum.set_ylabel("y [m]")
        self.axes_rotating_pendulum.set_title(
            "Pause - space, q - quit, click - data cursor"
        )
        self.axes_rotating_pendulum.set_aspect("equal", adjustable="box")
        self.axes_rotating_pendulum.plot(
            [x_from - 1000, x_to + 1000], [0, 0], "k--", lw=0.75
        )  # Help line
        self.axes_rotating_pendulum.plot(
            [0, 0], [y_from, y_to], "k-", lw=0.75
        )  # Help line
        text_time = f"Time = {self.time_start:2.3f}"
        self.text_time_handle = self.axes_rotating_pendulum.text(
            0.05,
            0.95,
            text_time,
            horizontalalignment="left",
            verticalalignment="center",
            transform=self.axes_rotating_pendulum.transAxes,
        )
        self.axes_rotating_pendulum.format_coord = (
            lambda state, observation: "%2.2f, %2.2f"
            % (
                state,
                observation,
            )
        )

        angle, xCoord0_cart = self.state_init[:2]
        angle += np.pi

        xCoord0_pole = self.rod_length * rc.sin(angle) + xCoord0_cart
        yCoord0_pole = self.rod_length * rc.cos(angle)

        self.scatter_sol = self.axes_rotating_pendulum.scatter(
            xCoord0_pole, yCoord0_pole, marker="o", s=400, c="b"
        )
        (self.line_rod,) = self.axes_rotating_pendulum.plot(
            [0, xCoord0_pole],
            [0, yCoord0_pole],
            "b",
            lw=1.5,
        )
        self.artists.append(self.line_rod)
        self.artists.append(self.text_time_handle)
        self.cart_patch_handle = patches.Rectangle(
            (xCoord0_cart - 0.25, -0.125),
            0.5,
            0.25,
            linewidth=2,
            edgecolor="g",
            facecolor="brown",
        )
        self.axes_rotating_pendulum.add_patch(self.cart_patch_handle)

    def perform_step_update(self):
        state_full = self.scenario.observation
        angle, x_cart = state_full[:2]

        xCoord = self.rod_length * rc.sin(angle) + x_cart
        yCoord = self.rod_length * rc.cos(angle)

        text_time = f"Time = {self.scenario.time:2.3f}"
        update_text(self.text_time_handle, text_time)
        cur_lims = self.axes_rotating_pendulum.get_xlim()
        if max(xCoord, x_cart) > cur_lims[1]:
            self.axes_rotating_pendulum.set_xlim(
                max(xCoord, x_cart) - 1.2, max(xCoord, x_cart) + 1.2
            )
        elif min(xCoord, x_cart) < cur_lims[0]:
            self.axes_rotating_pendulum.set_xlim(
                min(xCoord, x_cart) - 1.2, min(xCoord, x_cart) + 1.2
            )

        self.axes_rotating_pendulum.set_aspect("equal", adjustable="box")
        self.scatter_sol.remove()
        self.scatter_sol = self.axes_rotating_pendulum.scatter(
            xCoord, yCoord, marker="o", s=400, c="b"
        )

        self.line_rod.set_xdata([x_cart, xCoord])
        self.line_rod.set_ydata([0, yCoord])
        self.cart_patch_handle.set_xy((x_cart - 0.25, -0.125))


class InvPendulumTrackingDashboard(Dashboard):
    def __init__(self, time_start, rod_length, scenario):
        super().__init__()
        self.time_start = time_start
        self.rod_length = rod_length
        self.scenario = scenario
        self.state_init = scenario.state_init

    def init_dashboard(self):
        self.axes_rotating_pendulum = plt.gca()

        x_from = -self.rod_length - 0.2
        x_to = self.rod_length + 0.2
        y_from = x_from
        y_to = x_to
        self.axes_rotating_pendulum.autoscale(False)
        self.axes_rotating_pendulum.set_xlim(x_from, x_to)
        self.axes_rotating_pendulum.set_ylim(y_from, y_to)
        self.axes_rotating_pendulum.set_xlabel("x [m]")
        self.axes_rotating_pendulum.set_ylabel("y [m]")
        self.axes_rotating_pendulum.set_title(
            "Pause - space, q - quit, click - data cursor"
        )
        self.axes_rotating_pendulum.set_aspect("equal", adjustable="box")
        self.axes_rotating_pendulum.plot(
            [x_from, x_to], [0, 0], "k--", lw=0.75
        )  # Help line
        self.axes_rotating_pendulum.plot(
            [0, 0], [y_from, y_to], "k-", lw=0.75
        )  # Help line
        text_time = f"Time = {self.time_start:2.3f}"
        self.text_time_handle = self.axes_rotating_pendulum.text(
            0.05,
            0.95,
            text_time,
            horizontalalignment="left",
            verticalalignment="center",
            transform=self.axes_rotating_pendulum.transAxes,
        )
        self.axes_rotating_pendulum.format_coord = (
            lambda state, observation: "%2.2f, %2.2f"
            % (
                state,
                observation,
            )
        )

        xCoord0 = self.rod_length * rc.sin(self.state_init[0])
        yCoord0 = self.rod_length * rc.cos(self.state_init[0])

        self.scatter_sol = self.axes_rotating_pendulum.scatter(
            xCoord0, yCoord0, marker="o", s=400, c="b"
        )
        (self.line_rod,) = self.axes_rotating_pendulum.plot(
            [0, xCoord0],
            [0, yCoord0],
            "b",
            lw=1.5,
        )

        self.artists.append(self.text_time_handle)
        self.artists.append(self.line_rod)

    def perform_step_update(self):
        state_full = self.scenario.observation
        angle = state_full[0]

        xCoord = self.rod_length * rc.sin(angle)
        yCoord = self.rod_length * rc.cos(angle)

        text_time = f"Time = {self.scenario.time:2.3f}"
        update_text(self.text_time_handle, text_time)

        self.line_rod.set_xdata([0, xCoord])
        self.line_rod.set_ydata([0, yCoord])

        self.scatter_sol.remove()
        self.scatter_sol = self.axes_rotating_pendulum.scatter(
            xCoord, yCoord, marker="o", s=400, c="b"
        )


class LanderTrackingDasboard(Dashboard):
    def __init__(
        self,
        time_start,
        scenario,
        x_max=10,
        x_min=-10,
        y_max=10,
        y_min=-2,
    ):
        super().__init__()
        self.time_start = time_start
        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min
        self.scenario = scenario
        self.xCoord0, self.yCoord0, self.angle_deg0 = scenario.state_init[:3]
        self.marker = LanderMarker(angle=self.angle_deg0)

    def init_dashboard(self):
        self.axes_lander = plt.gca()

        self.axes_lander.set_xlim(self.x_min, self.x_max)
        self.axes_lander.set_ylim(self.y_min, self.y_max)
        self.axes_lander.set_xlabel("x [m]")
        self.axes_lander.set_ylabel("y [m]")
        self.axes_lander.set_title("Pause - space, q - quit, click - data cursor")

        self.axes_lander.set_aspect("equal", adjustable="box")
        self.axes_lander.plot(
            [self.x_min, self.x_max], [0, 0], "k--", lw=0.75
        )  # Help line
        self.axes_lander.plot(
            [0, 0], [self.y_min, self.y_max], "k--", lw=0.75
        )  # Help line
        (self.line_trajectory,) = self.axes_lander.plot(
            self.xCoord0, self.yCoord0, "b--", lw=0.5
        )
        self.lander_plot = self.axes_lander.scatter(
            self.xCoord0, self.yCoord0, marker=self.marker.marker, s=600, c="g"
        )
        self.artists.append(self.lander_plot)
        self.artists.append(self.line_trajectory)

        text_time = f"Time = {self.time_start:2.3f}"
        self.text_time_handle = self.axes_lander.text(
            0.05,
            0.95,
            text_time,
            horizontalalignment="left",
            verticalalignment="center",
            transform=self.axes_lander.transAxes,
        )
        self.artists.append(self.text_time_handle)

        self.axes_lander.format_coord = lambda state, observation: "%2.2f, %2.2f" % (
            state,
            observation,
        )

        xi = np.array([self.xCoord0, self.yCoord0])
        xi_2, xi_3 = self.scenario.simulator.system.compute_supports_geometry(
            xi, self.angle_deg0 * 2 * np.pi / 360.0
        )

        self.scatter_sol = self.axes_lander.scatter(
            [xi[0], xi_2[0], xi_3[0]], [xi[1], xi_2[1], xi_3[1]], s=40, c="b"
        )
        self.artists.append(self.scatter_sol)

    def perform_step_update(self):
        state = self.scenario.state_full
        time = self.scenario.time

        xCoord = state[0]
        yCoord = state[1]
        angle = state[2]
        text_time = f"Time = {time:2.3f}"

        update_text(self.text_time_handle, text_time)
        update_line(self.line_trajectory, xCoord, yCoord, axis_handle=self.axes_lander)
        self.scatter_sol.remove()
        self.lander_plot.remove()

        self.marker.rotate(angle / np.pi * 180)
        xi = np.array([xCoord, yCoord])
        xi_2, xi_3 = self.scenario.simulator.system.compute_supports_geometry(xi, angle)

        self.scatter_sol = self.axes_lander.scatter(
            [xi[0], xi_2[0], xi_3[0]], [xi[1], xi_2[1], xi_3[1]], s=40, c="b"
        )
        self.lander_plot = self.axes_lander.scatter(
            xCoord, yCoord, marker=self.marker.marker, s=600, c="g"
        )
