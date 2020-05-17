#!/usr/bin/env python3
from jinja2 import Template
import json
from core.basic.report import template


def render(path):
    with open(f'{path}/hydra_report/session.json', 'r') as session:
        hosts = json.load(session)
        render_tmpl = Template(template.template)
        with open(f'{path}/hydra_report/hydra_report.html', 'w') as hydra_report:
            hydra_report.write(render_tmpl.render(hosts=hosts, home_path=f'{path}'))