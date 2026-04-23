# order_submit

Finalizes the procurement process by submitting the order to the vendor's API.

## Parameters

- `part_id`: (string) Unique identifier for the item.
- `vendor_name`: (string) Target vendor.
- `quantity`: (integer) Number of units to order.

## Returns

- `transaction_id`: (string) The unique ID for the submitted order.
- `estimated_delivery`: (string) ISO date for expected arrival.

## Errors

- `SUBMISSION_FAILED`: If the vendor API rejects the order.
- `AUTH_ERROR`: If credentials for the vendor portal are invalid.