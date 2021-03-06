from collections import OrderedDict
from enum import Enum
from textwrap import dedent

from rv.controller import Controller
from rv.modules import MODULE_CLASSES
from rv.option import Option


class ModuleMeta(type):
    """Ensures controllers are set up in the order they are defined."""

    def __init__(cls, class_name, bases, class_dict):
        type.__init__(cls, class_name, bases, class_dict)
        cls.__init_registry(class_dict)
        cls.__init_controllers(class_dict)
        cls.__init_options(class_dict)
        cls.__init_docstring(class_dict)
        cls.__init_enum_docstrings(class_dict)

    def __init_registry(cls, class_dict):
        if class_dict.get("mtype") is not None:
            MODULE_CLASSES[class_dict["mtype"]] = cls

    def __init_controllers(cls, class_dict):
        ordered_controllers = [
            (k, v) for k, v in class_dict.items() if isinstance(v, Controller)
        ]
        ordered_controllers.sort(key=lambda x: x[1]._order)
        cls.controllers = OrderedDict()
        for i, (k, v) in enumerate(ordered_controllers, 1):
            v.label = k.replace("_", " ").title()
            v.name = k
            v.number = i
            cls.controllers[k] = v

    def __init_options(cls, class_dict):
        ordered_options = [
            (k, v) for k, v in class_dict.items() if isinstance(v, Option)
        ]
        if ordered_options:
            ordered_options.sort(key=lambda x: x[1]._order)
            cls.options = OrderedDict()
            for i, (k, v) in enumerate(ordered_options):
                v.label = k.replace("_", " ").title()
                v.name = k
                v.index = i
                cls.options[k] = v

    def __init_docstring(cls, class_dict):
        lines = ['"{mtype}" SunVox {mgroup} Module'.format(**class_dict), ""]
        if getattr(cls, "__doc__"):
            lines.append(dedent(cls.__doc__))
        lines += ["", "Behaviors:", ""]
        for b in sorted(cls.behaviors):
            lines += ["- {}".format(b.name)]
        if len(cls.controllers) > 0:
            lines += [
                "",
                "Controllers:",
                "",
                "=" * 40 + " " + "=" * 40 + " " + "=" * 40 + " " + "=" * 40,
                "{:40s} {:40s} {:40s} {:40s}".format(
                    "Number", "Name", "Type", "Default"
                ),
                "=" * 40 + " " + "=" * 40 + " " + "=" * 40 + " " + "=" * 40,
            ]
            for i, c in enumerate(cls.controllers.values(), 1):
                number = "``{0:02x}`` ({0:d})".format(i)
                lines.append(
                    "{number:40s} {c.name:40s} "
                    "{c.value_type!r:40s} {c.default!r:40s}".format(number=number, c=c)
                )
            lines.append("=" * 40 + " " + "=" * 40 + " " + "=" * 40 + " " + "=" * 40)
            lines.append("")
        else:
            lines.append("This module has no controllers.")
        cls.__doc__ = "\n".join(lines)

    def __init_enum_docstrings(cls, class_dict):
        # readthedocs.org doesn't correctly list out enumerator values,
        # so we generate our own table here.
        for e in class_dict.values():
            if isinstance(e, type) and issubclass(e, Enum):
                lines = [
                    "An enumeration.",
                    "",
                    "=" * 40 + " " + "=" * 40,
                    "{:40s} {:40s}".format("Name", "Value"),
                    "=" * 40 + " " + "=" * 40,
                ]
                for v in e:
                    lines.append("{:40s} {:40d}".format(v.name, v.value))
                lines.append("=" * 40 + " " + "=" * 40)
                e.__doc__ = "\n".join(lines)
