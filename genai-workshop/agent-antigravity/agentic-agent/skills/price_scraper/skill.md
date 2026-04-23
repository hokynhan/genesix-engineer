# price_scraper

Aggregates real-time market pricing and lead times from approved B2B vendor portals.

## Parameters

- `item_name`: (string) The common name or category of the item to search for.

## Returns

- `vendors`: (array) A list of objects containing:
    - `name`: (string) Vendor name.
    - `price`: (number) Unit price in USD.
    - `lead_time_days`: (integer) Estimated delivery time.

## Errors

- `NO_VENDORS_FOUND`: If the search returns no results for the item.
- `SCRAPE_FAILED`: If the external portal is unreachable.