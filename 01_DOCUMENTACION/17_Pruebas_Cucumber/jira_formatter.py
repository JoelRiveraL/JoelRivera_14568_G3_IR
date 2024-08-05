# features/formatters/jira_formatter.py

from behave.formatter.base import Formatter
import json

class JIRAFormatter(Formatter):
    def __init__(self, stream, config):
        super().__init__(stream, config)
        self.results = []

    def feature(self, feature):
        self.current_feature = {
            "uri": feature.filename,
            "id": feature.name.replace(" ", "-").lower(),
            "line": feature.line,
            "keyword": feature.keyword,
            "name": feature.name,
            "elements": []
        }

    def scenario(self, scenario):
        current_scenario = {
            "line": scenario.line,
            "id": scenario.name.replace(" ", "-").lower(),
            "type": "scenario",
            "keyword": scenario.keyword,
            "name": scenario.name,
            "steps": []
        }

        for step in scenario.steps:
            current_step = {
                "keyword": step.keyword,
                "line": step.line,
                "name": step.name,
                "match": {
                    "location": step.step_type
                },
                "result": {
                    "duration": getattr(step, 'duration', 0),
                    "status": step.status.name
                }
            }
            current_scenario["steps"].append(current_step)

        self.current_feature["elements"].append(current_scenario)

    def end_feature(self, feature):
        self.results.append(self.current_feature)

    def close(self):
        json.dump(self.results, self.stream, indent=4)
