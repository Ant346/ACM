from rcognita.objectives import RunningObjective
from rcognita.simulator import Simulator
from rcognita.scenarios import OnlineScenario
from rcognita.visualization import dashboards
from rcognita.visualization.animator import Animator


def create_testing_pipeline(
    system,
    controller,
    state_init,
    action_init,
    model_of_running_objective,
    observation_namings,
    action_namings,
    system_visualization_dashboard,
    system_visualization_dashboard_params,
    time_final=15,
    fps=10,
):
    running_objective = RunningObjective(model=model_of_running_objective)

    simulator = Simulator(
        system=system,
        time_final=time_final,
        sys_type=system.sys_type,
        state_init=state_init,
        action_init=action_init,
        disturb_init=None,
        time_start=0,
        sampling_time=0.01,
        max_step=0.001,
        first_step=1.0e-6,
        atol=1.0e-5,
        rtol=1.0e-3,
        ode_backend="SCIPY",
    )

    scenario = OnlineScenario(
        running_objective=running_objective,
        simulator=simulator,
        is_log=False,
        howanim="html",
        state_init=state_init,
        action_init=action_init,
        N_episodes=1,
        N_iterations=1,
        speedup=75,
        controller=controller,
        observation_target=[],
    )

    observation_dashboard = dashboards.DefaultDashboardActionOrObservation(
        0,
        simulator.time_final,
        datum_init=state_init,
        scenario=scenario,
        datum_namings=observation_namings,
        dashboard_type="observation",
    )
    action_dashboard = dashboards.DefaultDashboardActionOrObservation(
        0,
        simulator.time_final,
        datum_init=action_init,
        scenario=scenario,
        datum_namings=action_namings,
        dashboard_type="action",
    )
    objective_dashboard = dashboards.DefaultDashboardObjectives(
        0,
        simulator.time_final,
        scenario=scenario,
    )
    system_dashboard = system_visualization_dashboard(
        scenario=scenario, **system_visualization_dashboard_params
    )
    animator = Animator(
        observation_dashboard=observation_dashboard,
        action_dashboard=action_dashboard,
        objective_dashboard=objective_dashboard,
        system_visualization_dashboard=system_dashboard,
        scenario=scenario,
        fps=fps,
    )
    return scenario, animator
