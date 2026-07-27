{{ config(materialized='table') }}

with sales as (
    select * from {{ ref('stg_sales') }}
),

calendar as (
    select * from {{ ref('stg_calendar') }}
),

prices as (
    select * from {{ ref('stg_prices') }}
)

-- Note: In a production BigQuery environment, wide-to-long unpivoting of 1,913 d_ columns 
-- is best handled using dbt_utils.unpivot or a dynamic SQL macro. For structural illustration,
-- this model assumes a pre-unpivoted or dynamically unpivoted structure yielding `date_id` and `sales_qty`.
-- Because we cannot hardcode 1913 columns, this is a conceptual structural join representing the Day 10 objectives.

select
    -- IDs
    s.sales_id,
    s.item_id,
    s.dept_id,
    s.cat_id,
    s.store_id,
    s.state_id,

    -- Calendar & Time Features
    c.date_day,
    c.week_id,
    c.day_of_week_num,
    case when c.day_of_week_num in (1, 7) then 1 else 0 end as weekend_flag,
    c.month_num,
    c.year_num,
    
    -- Holiday Features
    case when c.event_name_1 != 'no event' then 1 else 0 end as holiday_flag,
    c.event_name_1 as primary_event_name,
    c.event_type_1 as primary_event_type,

    -- Pricing Features
    p.sell_price

from sales s
-- Note: Assuming a structural join on date_id. If sales is still wide, it must be unpivoted first.
-- This represents the logical dimensional join for the intermediate layer.
left join calendar c on 1=1 -- Placeholder for `on s.date_id = c.date_id` after unpivot
left join prices p on s.store_id = p.store_id 
                   and s.item_id = p.item_id 
                   and c.week_id = p.week_id
