# Maintainer solution notes

Deduplicate attribution to one selected row per order before joining, preferably the highest priority
then latest touch. Join on `order_id`, keep all orders, and reconcile order revenue exactly.
