# Maintainer solution notes

Sort by date, use shifted rolling windows for lagged features, split the last three dates into
validation, and write deterministic metrics with `validation_rows` and `mae_baseline`.
