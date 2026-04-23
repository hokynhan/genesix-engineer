# contract_validator

Validates a proposed purchase against Master Service Agreements (MSAs) and agent spending limits.

## Parameters

- `total_cost`: (number) The total value of the order.
- `vendor_name`: (string) The name of the vendor being used.

## Returns

- `status`: (string) "VALIDATED" or "REJECTED".
- `message`: (string) Reasoning for the validation status.

## Errors

- `VALIDATION_TIMEOUT`: If the legal engine takes too long to respond.
- `LIMIT_EXCEEDED`: If the cost exceeds the hard ceiling of the organization.