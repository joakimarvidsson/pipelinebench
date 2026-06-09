# Maintainer solution notes

Sort by `event_ts`, `event_sequence`, and input order, drop exact duplicate events, keep the final
event per `customer_id`, remove final deletes, assert primary key uniqueness, and sort by
`customer_id`.
