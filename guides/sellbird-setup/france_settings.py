"""Apply France defaults to Sellbird's sellbird.local.yaml.

Run from the Sellbird folder, with its venv active, BEFORE `sellbird train`:

    python /path/to/france_settings.py

Creates sellbird.local.yaml from sellbird.yaml if needed. Training keeps these
settings (it only replaces product, company and targeting fields), but it
overwrites icp.geography, so run this script again after training.
Comments from sellbird.yaml are not kept in the new file.
"""
import pathlib
import shutil

import yaml

p = pathlib.Path("sellbird.local.yaml")
if not p.exists():
    shutil.copy("sellbird.yaml", p)
c = yaml.safe_load(p.read_text(encoding="utf-8"))

# Quiet hours on Paris time, not New York time.
c["usage"]["quiet_hours"]["timezone"] = "Europe/Paris"

email = c["channels"]["email"]
email["require_approval"] = True  # every email waits for you in the Outbox
email["send_window"] = {  # cold email only in office hours, Monday to Friday
    "start": "09:00",
    "end": "18:00",
    "weekdays_only": True,
    "recipient_timezone": True,
}

comp = c["compliance"]
comp["opt_out_line"] = "Pas intéressé ? Répondez-moi simplement et je ne vous écrirai plus."
comp["precleared"].update({"sender_country": "FR", "prospect_country": "FR"})

c["icp"]["geography"] = ["France"]

p.write_text(yaml.safe_dump(c, allow_unicode=True, sort_keys=False), encoding="utf-8")
print("sellbird.local.yaml: France settings applied")
