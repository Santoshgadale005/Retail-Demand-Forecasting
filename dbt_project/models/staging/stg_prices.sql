with source as (
    select * from {{ source('retail_forecasting', 'stg_prices') }}
),

renamed as (
    select
        store_id,
        item_id,
        cast(wm_yr_wk as int64) as week_id,
        cast(sell_price as float64) as sell_price
    from source
)

select * from renamed
