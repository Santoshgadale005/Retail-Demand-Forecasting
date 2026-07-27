{{ config(materialized='table') }}

with calendar as (
    select * from {{ ref('stg_calendar') }}
),

final as (
    select distinct
        -- Surrogate Key
        farm_fingerprint(cast(date_day as string)) as date_key,
        
        -- Attributes
        date_day as date,
        day_of_week_num as day,
        week_id as week,
        month_num as month,
        extract(quarter from date_day) as quarter,
        year_num as year,
        case when event_name_1 != 'no event' then 1 else 0 end as holiday_flag,
        event_name_1 as holiday_name
    from calendar
)

select * from final
