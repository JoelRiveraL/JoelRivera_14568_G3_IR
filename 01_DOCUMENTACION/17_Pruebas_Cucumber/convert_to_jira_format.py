import json


def adapt_behave_to_cucumberjs(behave_json):
    cucumber_js_json = []

    for feature in behave_json:
        feature_item = {
            "uri": feature["location"].split(":")[0],
            "id": feature["name"].replace(" ", "-").lower(),  # Genera un id simple
            "line": 1,  # Asigna una línea ficticia, puedes ajustar esto según sea necesario
            "keyword": "Feature",
            "name": feature["name"],
            "description": "",
            "elements": []
        }

        for scenario in feature.get("elements", []):
            scenario_item = {
                "id": scenario["name"].replace(" ", "-").lower(),  # Genera un id simple
                "line": int(scenario["location"].split(":")[1]),
                "type": "scenario",
                "keyword": "Scenario",
                "name": scenario["name"],
                "description": "",
                "steps": []
            }

            for step in scenario.get("steps", []):
                step_item = {
                    "arguments": [],
                    "keyword": step["keyword"],
                    "line": int(step["location"].split(":")[1]),
                    "name": step["name"],
                    "result": {}
                }

                # Manejo seguro del campo 'result'
                if "result" in step:
                    result = step["result"]
                    step_item["result"] = {
                        "status": result.get("status", "undefined"),
                        "duration": result.get("duration", 0)
                    }
                else:
                    step_item["result"] = {
                        "status": "undefined",
                        "duration": 0
                    }

                scenario_item["steps"].append(step_item)

            feature_item["elements"].append(scenario_item)

        cucumber_js_json.append(feature_item)

    return cucumber_js_json

# Ejemplo de uso
with open('results.json', 'r') as file:
    behave_json = json.load(file)

cucumber_js_json = adapt_behave_to_cucumberjs(behave_json)

with open('cucumber_results.json', 'w') as file:
    json.dump(cucumber_js_json,file, indent = 2)
