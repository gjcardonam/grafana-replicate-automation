import json
import os
from deepdiff import DeepDiff

DEV_PATH = "grafana-sync/dashboards/dev"
REPL_PATH = "grafana-sync/dashboards/replicate"

def load_dashboard(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def sync_dashboards():
    general_path = "dashboards/general"
    dev_dir = os.path.join(DEV_PATH, general_path)
    rep_dir = os.path.join(REPL_PATH, general_path)

    for filename in os.listdir(dev_dir):
        if not filename.endswith(".json"):
            continue

        dev_file = os.path.join(dev_dir, filename)
        rep_file = os.path.join(rep_dir, filename)

        if not os.path.exists(rep_file):
            print(f"Dashboard {filename} not found in replicate, skipping")
            continue

        dev_dash = load_dashboard(dev_file)
        rep_dash = load_dashboard(rep_file)

        updated = False

        dev_panels = {p["id"]: p for p in dev_dash["spec"]["panels"]}
        rep_panels = {p["id"]: p for p in rep_dash["spec"]["panels"]}

        for pid, dev_panel in dev_panels.items():
            if pid in rep_panels:
                # Ignorar gridPos
                dev_panel_cp = {k: v for k, v in dev_panel.items() if k != "gridPos"}
                rep_panel_cp = {k: v for k, v in rep_panels[pid].items() if k != "gridPos"}

                diff = DeepDiff(rep_panel_cp, dev_panel_cp, ignore_order=True)
                if diff:
                    print(f"[CHANGED] Panel ID {pid} in {filename}")
                    for key in dev_panel_cp:
                        if key != "gridPos":
                            rep_panels[pid][key] = dev_panel_cp[key]
                    updated = True

        if updated:
            rep_dash["spec"]["panels"] = list(rep_panels.values())
            with open(rep_file, "w", encoding="utf-8") as f:
                json.dump(rep_dash, f, indent=2)
            print(f"[UPDATED] {rep_file} updated.")

if __name__ == "__main__":
    sync_dashboards()