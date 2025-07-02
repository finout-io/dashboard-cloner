import requests
import copy
import pdb;

# === CONFIGURATION ===
BASE_URL = "http://finout-app.prod.internal.finout.io/dashboard-service"

def sanitize_for_post(data, fields_to_remove=None):
    if fields_to_remove is None:
        fields_to_remove = {"id", "widgetId", "createdAt", "updatedAt", "uuid", "_id", "accountId", "createdBy"}

    if isinstance(data, dict):
        return {
            k: sanitize_for_post(v, fields_to_remove)
            for k, v in data.items()
            if k not in fields_to_remove
        }
    elif isinstance(data, list):
        return [sanitize_for_post(item, fields_to_remove) for item in data]
    else:
        return data

# === STEP 1: Get the source dashboard ===
def get_dashboard(account_id, dashboard_id):
    headers = {
        "authorized-user-roles": "sysAdmin",
        "authorized-account-id": account_id,
        "Content-Type": "application/json",
    }
    url = f"{BASE_URL}/dashboard/{dashboard_id}"
    response = requests.get(url, headers=headers)
    print('dashboard retrieved ✅', response)
    response.raise_for_status()
    return response.json()

# === STEP 2: Create a new dashboard with same metadata in target account ===
def create_dashboard(account_id, name, description, tags):
    headers = {
        "authorized-user-roles": "sysAdmin",
        "authorized-account-id": account_id,
        "Content-Type": "application/json",
    }
    payload = {
        "name": name,
        "description": description,
        "tags": tags
    }
    url = f"{BASE_URL}/dashboard"
    response = requests.post(url, headers=headers, json=payload)
    print('dashboard created ✅', response)
    response.raise_for_status()
    return response.json()["id"]

# === STEP 3: Take all widgets from the source dashboard, get the original widget object and use that as the payload to and create new widget objects ===
def create_widgets(account_id, widgets):
    headers = {
        "authorized-user-roles": "sysAdmin",
        "authorized-account-id": account_id,
        "Content-Type": "application/json",
    }
    # widgets = [w for w in widgets if w.get("dashboardId") == dashboard_id]
    detailed_widgets = []
    print(widgets)
    for w in widgets:
        wid = w["widgetId"]
        existing_widget = requests.get(f"{BASE_URL}/widget/{wid}", headers=headers).json()
        sanitized_widget = sanitize_for_post(existing_widget)
        response = requests.post(f"{BASE_URL}/widget", headers=headers, json=sanitized_widget)
        response.raise_for_status()
        new_widget = response.json()
        w['widgetId'] = new_widget['id']
        detailed_widgets.append(w)
    print('widgets created ✅', detailed_widgets)
    return detailed_widgets

# === STEP 4: Updated the widgets in the new dashboard in target account ===
def update_new_dashboard(source_widgets, account_id, new_dashboard_id):
    headers = {
        "authorized-user-roles": "sysAdmin",
        "authorized-account-id": account_id,
        "Content-Type": "application/json",
    }

    #== iterate thru original widgets and update widget id

    url = f"{BASE_URL}/dashboard/{new_dashboard_id}"
    payload = {
        "id": new_dashboard_id,
        "widgets": source_widgets
    }
    response = requests.put(url, headers=headers, json=payload)
    print('dashboard updated ✅', response)
    response.raise_for_status()

# === MAIN ===
def clone_dashboard(source_account_id, source_dashboard_id, target_account_id, new_dashboard_name):
    source_dashboard = get_dashboard(source_account_id, source_dashboard_id)
    new_dashboard_id = create_dashboard(
        target_account_id,
        name=new_dashboard_name,
        description=source_dashboard.get("description", ""),
        tags=source_dashboard.get("tags", [])
    )
    widgets = create_widgets(source_account_id, source_dashboard['widgets'])
    update_new_dashboard(widgets, target_account_id, new_dashboard_id)
    return new_dashboard_id
