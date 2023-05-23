import numbers

# !pip install mpldatacursor <-- to install this
from mpldatacursor import datacursor

from ..__utilities import rc


def rescale_axis_if_needed(matplotlib_handle, x_current, y_current, offset=0.2):
    x_max = matplotlib_handle.get_xlim()[1]
    x_min = matplotlib_handle.get_xlim()[0]
    y_max = matplotlib_handle.get_ylim()[1]
    y_min = matplotlib_handle.get_ylim()[0]
    if x_current > x_max - offset:
        matplotlib_handle.set_xlim(x_min, x_current + offset)
    if x_current < x_min + offset:
        matplotlib_handle.set_xlim(x_current - offset, x_max)
    if y_current > y_max - offset:
        matplotlib_handle.set_ylim(y_min, y_current + offset)
    if y_current < y_min + offset:
        matplotlib_handle.set_ylim(y_current - offset, y_max)


def update_line(matplotlib_handle, newX, newY, axis_handle=None):
    old_xdata = matplotlib_handle.get_xdata()
    old_ydata = matplotlib_handle.get_ydata()
    if any(isinstance(coord, numbers.Number) for coord in [newX, newY]):
        new_xdata = rc.append(old_xdata, newX)
        new_ydata = rc.append(old_ydata, newY)
    else:
        new_xdata = rc.concatenate((old_xdata, newX))
        new_ydata = rc.concatenate((old_ydata, newY))

    matplotlib_handle.set_xdata(new_xdata)
    matplotlib_handle.set_ydata(new_ydata)
    if axis_handle is not None:
        rescale_axis_if_needed(axis_handle, newX, newY)


def reset_line(matplotlib_handle):
    matplotlib_handle.set_data([], [])


def update_text(matplotlib_handle, new_text):
    matplotlib_handle.set_text(new_text)


def update_patch_color(matplotlib_handle, new_color):
    matplotlib_handle.set_color(str(new_color))


def init_data_cursor(matplotlib_handle):
    datacursor(matplotlib_handle)
