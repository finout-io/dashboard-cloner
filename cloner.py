import requests
import copy
import pdb;

# === CONFIGURATION ===
BASE_URL = "http://finout-app.prod.internal.finout.io/dashboard-service"


def sanitize_for_post(data, fields_to_remove=None):
    if fields_to_remove is None:
        fields_to_remove = {
            "id", "widgetId", "createdAt", "updatedAt", "uuid", "_id", "accountId", "createdBy"
        }

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
    print("✅ Retrieved source dashboard:", response.status_code)
    response.raise_for_status()
    return response.json()


# === STEP 2: Create a new dashboard ===
def create_dashboard(account_id, name, description, tags):
    headers = {
        "authorized-user-roles": "sysAdmin",
        "authorized-account-id": account_id,
        "Content-Type": "application/json",
    }
    payload = {
        "isActive": True,
        "acl": {
            "read": {"type": "public", "users": [], "groups": []},
            "write": {"type": "public", "users": [], "groups": []},
        },
        "name": name,
        "description": description,
        "tags": tags,
    }
    url = f"{BASE_URL}/dashboard"
    response = requests.post(url, headers=headers, json=payload)
    print("✅ Created new dashboard:", response.status_code)
    response.raise_for_status()
    return response.json()["id"]


# === STEP 3: Clone widgets ===
def create_widgets(account_id, source_widgets):
    headers = {
        "authorized-user-roles": "sysAdmin",
        "authorized-account-id": account_id,
        "Content-Type": "application/json",
    }

    new_widgets_layout = []

    for w in source_widgets:
        old_widget_id = w["widgetId"]

        # Get full widget definition
        existing_widget = requests.get(f"{BASE_URL}/widget/{old_widget_id}", headers=headers).json()
        sanitized_widget = sanitize_for_post(existing_widget)

        # Create new widget
        response = requests.post(f"{BASE_URL}/widget", headers=headers, json=sanitized_widget)
        response.raise_for_status()
        new_widget = response.json()
        new_widget_id = new_widget["id"]

        # Update layout with new widget ID
        widget_layout = copy.deepcopy(w)
        widget_layout["widgetId"] = new_widget_id
        widget_layout["configuration"].update({
            "minW": 82,
            "minH": 82,
            "static": True
        })
        new_widgets_layout.append(widget_layout)

    print("✅ Created and mapped widgets")
    return new_widgets_layout


# === STEP 4: Patch dashboard layout ===
def update_dashboard_layout(account_id, dashboard_id, widgets_layout):
    headers = {
        "authorized-user-roles": "sysAdmin",
        "authorized-account-id": account_id,
        "Content-Type": "application/json",
    }
    url = f"{BASE_URL}/dashboard/{dashboard_id}"
    payload = {
        "widgets": widgets_layout
    }
    response = requests.put(url, headers=headers, json=payload)
    print("✅ Patched dashboard layout:", response.status_code)
    response.raise_for_status()


# === CLEANUP: Delete dashboard on failure ===
def delete_dashboard(account_id, dashboard_id):
    headers = {
        "authorized-user-roles": "sysAdmin",
        "authorized-account-id": account_id,
        "Content-Type": "application/json",
    }
    url = f"{BASE_URL}/dashboard/{dashboard_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"🗑️ Deleted dashboard {dashboard_id} due to error cleanup")
    else:
        print(f"⚠️ Failed to delete dashboard {dashboard_id}. Status: {response.status_code}")


# === MAIN CLONING FUNCTION ===
def clone_dashboard(source_account_id, source_dashboard_id, target_account_id, new_dashboard_name):
    new_dashboard_id = None
    # Get source dashboard
    source_dashboard = get_dashboard(source_account_id, source_dashboard_id)

    # Create dashboard in target account
    new_dashboard_id = create_dashboard(
        target_account_id,
        name=new_dashboard_name,
        description=source_dashboard.get("description", ""),
        tags=source_dashboard.get("tags", []),
    )

    # Clone widgets and attach
    new_widgets_layout = create_widgets(target_account_id, source_dashboard["widgets"])

    # Patch dashboard with new widgets
    update_dashboard_layout(target_account_id, new_dashboard_id, new_widgets_layout)

    print(f"🎉 Dashboard cloned successfully! New Dashboard ID: {new_dashboard_id}")
    return new_dashboard_id

    