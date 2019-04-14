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
On source’s kibana:
Create backup:
```
PUT /_snapshot/omnovos_backup
{
  "type": "fs",
  "settings": {
    "location": "my_backup_location"
  }
}
```

Create a snapshot of all data in the backup:
```
PUT /_snapshot/omnovos_backup/snapshot_1?wait_for_completion=true
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

Copy folder \backups\my_backup_location to the target \backups\
Now, start target ES instance.

