{{ config(materialized='table') }}

with sales as (
    select * from {{ ref('stg_sales') }}
),

final as (
    select distinct
        -- Surrogate Key
        farm_fingerprint(store_id) as store_key,
        
        -- Attributes
        store_id as store,
        state_id as state
    from sales
)

select * from final
