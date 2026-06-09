# Maintainer solution notes

Read all partitions, align schemas by name, preserve `account_tier`, coerce `account_id` to integer,
`balance` to float, `is_active` to boolean, `opened_at` to datetime, fill missing `account_tier` with
`unknown`, and sort by `account_id`.
