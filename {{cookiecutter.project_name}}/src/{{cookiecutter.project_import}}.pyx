{% if cookiecutter.require_numpy == 'y' -%}
cimport numpy
import numpy

{%- endif %}
cimport {{cookiecutter.project_import}}

include "version.pxi"
