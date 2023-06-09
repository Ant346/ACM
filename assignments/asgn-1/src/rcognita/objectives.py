"""
Module that contains general objectives functions that can be used by various entities of the framework.
For instance, a running objective can be used commonly by a generic optimal controller, an actor, a critic, a logger, an animator, a pipeline etc.

"""

from abc import ABC, abstractmethod

import rcognita.base


def inject_observation_target(observation_target):
    def decorator(objective):
        def wrapper(self, observation, action):
            observation -= observation_target
            return objective(self, observation, action)

        return wrapper

    return decorator


class Objective(rcognita.base.RcognitaBase, ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self):
        pass


class RunningObjective(Objective):
    """
    This is what is usually treated as reward or unitlity in maximization problems.
    In minimzations problems, it is called cost or loss, say.
    """

    def __init__(self, model):
        """
        Initialize a RunningObjective instance.

        :param model: function that calculates the running objective for a given observation and action.
        :type model: function
        """
        self.model = model

    def __call__(self, observation, action):
        """
        Calculate the running objective for a given observation and action.

        :param observation: current observation.
        :type observation: numpy array
        :param action: current action.
        :type action: numpy array
        :return: running objective value.
        :rtype: float
        """

        if hasattr(self, "observation_target"):
            observation_new = observation - self.observation_target
            running_objective = self.model(observation_new, action)
        else:
            running_objective = self.model(observation, action)

        return running_objective
