import requests
import copy

def clone_dashboard(api_token, source_dashboard_id, new_dashboard_name):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    base_url = "https://api.finout.io"

    res = requests.get(f"{base_url}/dashboards/{source_dashboard_id}", headers=headers)
    res.raise_for_status()
    source_dashboard = res.json()

    payload = {
        "name": new_dashboard_name,
        "description": source_dashboard.get("description", ""),
        "tags": source_dashboard.get("tags", [])
    }
    res = requests.post(f"{base_url}/dashboards", headers=headers, json=payload)
    res.raise_for_status()
    new_dashboard_id = res.json()["id"]

    res = requests.get(f"{base_url}/dashboards/{source_dashboard_id}/widgets", headers=headers)
    res.raise_for_status()
    widgets = res.json()

    for widget in widgets:
        widget_copy = copy.deepcopy(widget)
        widget_copy.pop("id", None)
        widget_copy["dashboardId"] = new_dashboard_id

        if "layout" in widget_copy:
            layout = widget_copy["layout"]
            layout["x"] += 0
            layout["y"] += 0

        res = requests.post(f"{base_url}/dashboards/{new_dashboard_id}/widgets", headers=headers, json=widget_copy)
        res.raise_for_status()

    return new_dashboard_id