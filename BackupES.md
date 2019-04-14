# Elasticsearch Backup/Migragation

## Preparation
For both source and target ES, cd to \config\, open elasticsearch.yml. Add this (fix the url to your environment): 
```
# ----------------------------------- Paths ------------------------------------
#
# Path to directory where to store the data (separate multiple locations by comma):
#
#path.data: /path/to/data
#
# Path to log files:
#
#path.logs: /path/to/logs
#
path.repo: E:\CurrentProjects\forAllan\elasticsearch-6.4.3\backups
```
After changing the yml, restart ES instances.

## Create backup on source
On source’s kibana, create backup:
```
PUT /_snapshot/omnovos_backup
{
  "type": "fs",
  "settings": {
    "location": "my_backup_location"
  }
}
```

Create a snapshot in the backup:
```
PUT /_snapshot/omnovos_backup/snapshot_1?wait_for_completion=true
{
  "indices": "omnovos_shopper,omnovos_recipe",
  "ignore_unavailable": true,
  "include_global_state": false
}
```

For big datasets, it might not show any confirmation, or a timeout response. No problem. Instead, run this query to check its status:
```
GET /_snapshot/omnovos_backup/snapshot_1
```

You might get this result, it means the backup is in progress. 

```
{
  "snapshots": [
    {
      "snapshot": "snapshot_1",
      "uuid": "xKTJ0BxcRKW2z4zf9uytHQ",
      "version_id": 6040399,
      "version": "6.4.3",
      "indices": [
        "bookdb_index",
        "my_index_datetime",
        "omnovos_recipe",
        "omnovos_shopper",
        "log_test",
        "log_test2",
        "omnovos_transaction",
        "omnovos_question",
        "favorite_recipes",
        "test",
        "bookdb_index2",
        ".kibana",
        "shoppers"
      ],
      "include_global_state": true,
      "state": "IN_PROGRESS",
      "start_time": "2019-04-14T04:54:23.345Z",
      "start_time_in_millis": 1555217663345,
      "end_time": "1970-01-01T00:00:00.000Z",
      "end_time_in_millis": 0,
      "duration_in_millis": -1555217663345,
      "failures": [],
      "shards": {
        "total": 0,
        "failed": 0,
        "successful": 0
      }
    }
  ]
}
```
When it shows "SUCCESS", it's done.

## Restore data on target
Copy folder \backups\my_backup_location to the target \backups\
Now, start target ES instance.
Create the same backup:
```
PUT /_snapshot/omnovos_backup
{
  "type": "fs",
  "settings": {
    "location": "my_backup_location"
  }
}
```
Note that data has been transfer, so now we already have the previous snapshot, check by:
```
GET /_snapshot/omnovos_backup/snapshot_1
```
We should get SUCCESS response.
Restore by:
```
POST /_snapshot/omnovos_backup/snapshot_1/_restore
{
  "indices": "omnovos_shopper,omnovos_recipe",
  "ignore_unavailable": true,
  "include_global_state": true,
  "rename_pattern": "index_(.+)",
  "rename_replacement": "restored_index_$1"
}
```
We should get:
```
{
  "accepted": true
}
```

## Notes
Note that in the above example, two indexes chosen for migration are omnovos_shopper,omnovos_recipe. If none specified, ES will backup all indexes. 
The queries are simple:
```
PUT /_snapshot/omnovos_backup/snapshot_1?wait_for_completion=true
```
and 
```
POST /_snapshot/omnovos_backup/snapshot_1/_restore
```
