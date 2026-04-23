# check_stock

Accesses the internal ERP system to retrieve real-time inventory data for a specific part.

## Parameters

- `part_id`: (string) The unique identifier for the inventory item (e.g., "PART_77A").

## Returns

- `stock`: (integer) Current quantity on hand.
- `min_threshold`: (integer) The reorder point for this item.
- `location`: (string) The warehouse or bin location.

## Errors

- `ITEM_NOT_FOUND`: If the provided part_id does not exist in the ERP.
- `ERP_OFFLINE`: If the connection to the ERP system fails.