{{ config(
    materialized='table',
    partition_by={
      "field": "date",
      "data_type": "date",
      "granularity": "day"
    },
    cluster_by=["store_key", "product_key"]
) }}

with int_sales as (
    select * from {{ ref('int_sales') }}
),

final as (
    select
        -- Surrogate Keys
        farm_fingerprint(cast(date_day as string)) as date_key,
        farm_fingerprint(store_id) as store_key,
        farm_fingerprint(item_id) as product_key,
        
        -- Degenerate Dimensions
        date_day as date,
        store_id,
        item_id,
        
        -- Facts
        -- Note: using `1 as sales_qty` as a placeholder for the unpivoted metric
        1 as sales_qty,
        sell_price
        
    from int_sales
)

select * from final
