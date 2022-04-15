# terraform-cloud-trigger
Utility to trigger runs for workspaces in terraform cloud. This is useful if you have a private or public module and want to automatically kick off terraform builds when the module has been updated. 

## Usage
```
name: run terraform-cloud
on:
  push:
    branches:
      - main

jobs:
  trigger-tf-cloud:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Trigger TF Cloud Runs
        uses: flymachine-dev/terraform-cloud-trigger@0.0.5
        with:
          TFE_TOKEN: ${{ secrets.TFE_TOKEN }}
          type: apply
          workspace: your_workspace
          org: your_org
```

#### Options

- **TFE_TOKEN** (required): terraform api key, must be a user key and not an organization key.
- **workspace** (required): the terraform cloud workspace to initiate the run
- **org** (required): your terraform cloud organization
- **type** : the type of run options are plan/apply
- **target** : if you'd like to target a resource or module you can specify here. (resource.aws_s3_bucket.mybucket)
- **message** : message explaining what the run is for or where it's originating from
