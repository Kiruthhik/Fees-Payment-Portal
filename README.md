# Azure template

## Parameters

Parameter name | Required | Description
-------------- | -------- | -----------
vulnerabilityAssessments_Default_storageContainerPath | Yes      |
servers_rec_server_name | No       |
sites_rec_student_fee_portal_name | No       |
serverfarms_ASP_studentfeeportal_a966_name | No       |
components_rec_student_fee_portal_name | No       |
registries_studentfeeportalacr_name | No       |
userAssignedIdentities_oidc_msi_948f_name | No       |
actionGroups_Application_Insights_Smart_Detection_name | No       |
workspaces_DefaultWorkspace_af67fa2a_b0a8_489b_aeb7_6046c2e64cf0_CID_externalid | No       |

### vulnerabilityAssessments_Default_storageContainerPath

![Parameter Setting](https://img.shields.io/badge/parameter-required-orange?style=flat-square)



### servers_rec_server_name

![Parameter Setting](https://img.shields.io/badge/parameter-optional-green?style=flat-square)



- Default value: `rec-server`

### sites_rec_student_fee_portal_name

![Parameter Setting](https://img.shields.io/badge/parameter-optional-green?style=flat-square)



- Default value: `rec-student-fee-portal`

### serverfarms_ASP_studentfeeportal_a966_name

![Parameter Setting](https://img.shields.io/badge/parameter-optional-green?style=flat-square)



- Default value: `ASP-studentfeeportal-a966`

### components_rec_student_fee_portal_name

![Parameter Setting](https://img.shields.io/badge/parameter-optional-green?style=flat-square)



- Default value: `rec-student-fee-portal`

### registries_studentfeeportalacr_name

![Parameter Setting](https://img.shields.io/badge/parameter-optional-green?style=flat-square)



- Default value: `studentfeeportalacr`

### userAssignedIdentities_oidc_msi_948f_name

![Parameter Setting](https://img.shields.io/badge/parameter-optional-green?style=flat-square)



- Default value: `oidc-msi-948f`

### actionGroups_Application_Insights_Smart_Detection_name

![Parameter Setting](https://img.shields.io/badge/parameter-optional-green?style=flat-square)



- Default value: `Application Insights Smart Detection`

### workspaces_DefaultWorkspace_af67fa2a_b0a8_489b_aeb7_6046c2e64cf0_CID_externalid

![Parameter Setting](https://img.shields.io/badge/parameter-optional-green?style=flat-square)



- Default value: `/subscriptions/af67fa2a-b0a8-489b-aeb7-6046c2e64cf0/resourceGroups/DefaultResourceGroup-CID/providers/Microsoft.OperationalInsights/workspaces/DefaultWorkspace-af67fa2a-b0a8-489b-aeb7-6046c2e64cf0-CID`

## Snippets

### Parameter file

```json
{
    "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
    "contentVersion": "1.0.0.0",
    "metadata": {
        "template": "Documents/clg notes/sem7/cloud/ExportedTemplate-student-fee-portal/template.json"
    },
    "parameters": {
        "vulnerabilityAssessments_Default_storageContainerPath": {
            "reference": {
                "keyVault": {
                    "id": ""
                },
                "secretName": ""
            }
        },
        "servers_rec_server_name": {
            "value": "rec-server"
        },
        "sites_rec_student_fee_portal_name": {
            "value": "rec-student-fee-portal"
        },
        "serverfarms_ASP_studentfeeportal_a966_name": {
            "value": "ASP-studentfeeportal-a966"
        },
        "components_rec_student_fee_portal_name": {
            "value": "rec-student-fee-portal"
        },
        "registries_studentfeeportalacr_name": {
            "value": "studentfeeportalacr"
        },
        "userAssignedIdentities_oidc_msi_948f_name": {
            "value": "oidc-msi-948f"
        },
        "actionGroups_Application_Insights_Smart_Detection_name": {
            "value": "Application Insights Smart Detection"
        },
        "workspaces_DefaultWorkspace_af67fa2a_b0a8_489b_aeb7_6046c2e64cf0_CID_externalid": {
            "value": "/subscriptions/af67fa2a-b0a8-489b-aeb7-6046c2e64cf0/resourceGroups/DefaultResourceGroup-CID/providers/Microsoft.OperationalInsights/workspaces/DefaultWorkspace-af67fa2a-b0a8-489b-aeb7-6046c2e64cf0-CID"
        }
    }
}
```
