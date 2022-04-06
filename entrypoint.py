import os
import requests
import json
import time

org_name = os.environ.get('org_id')
workspace_name = os.environ.get('workspace_id')
TFE_TOKEN = os.environ.get('TFE_TOKEN')
auto_apply_bool = os.environ.get('auto_apply')

tf_url = "https://app.terraform.io/api/v2/organizations/%s/workspaces/%s" % (org_name, workspace_name)
headers = {"Content-Type": "application/vnd.api+json", "Authorization": "Bearer %s" % TFE_TOKEN}
try:
    r = requests.get(tf_url, headers=headers)
    r.raise_for_status()

    response = json.loads(r.text)
    workspace_id = response["data"]["id"]
    print("Acquired workspace id")

except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

tf_payload = {"data": {
    "attributes": {
      "message": "Terraform Plan via Api",
      "auto-apply": "%s" % auto_apply_bool
    },
    "type": "runs",
    "relationships": {
      "workspace": {
        "data": {
          "type": "workspaces",
          "id": "%s" % workspace_id
        }
      }
    }
  }
}
data=json.dumps(tf_payload)
tf_post_url = "https://app.terraform.io/api/v2/runs"
print("Executing Run...")
try:
    r_post = requests.post(tf_post_url, headers=headers, data=data)
    r_post.raise_for_status()
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

response = json.loads(r_post.text)
run_id = response["data"]["id"]
run_finished = False
while not run_finished:
    r_run = requests.get("https://app.terraform.io/api/v2/runs/%s" % run_id, headers=headers)
    response = json.loads(r_run.text)
    run_status = response["data"]["attributes"]["status"]
    if auto_apply_bool == "true":
        if run_status == "errored":
            err = "Terraform Run Failed"
            raise SystemExit(err)
        elif run_status == "applied":
            run_finished = True
    elif auto_apply_bool == "false":
        if run_status == "planned_and_finished" or run_status == "planned":
            run_finished = True

    if run_status == "discarded":
        print("run has been discarded")
        exit()

    time.sleep(60)

print("%s was successful!" % run_id)
