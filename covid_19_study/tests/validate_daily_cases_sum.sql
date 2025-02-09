with state_daily_sum as (
    select
        date
        , sum(cases_total) AS state_cases_sum
    from
        {{ ref('fct_state_daily_cases') }}
    group by
        date
),

daily_cases as (
    select
        date
        , cases_total AS daily_total_cases
    from
        {{ ref('dim_daily_cases') }}
)

select
    s.date
    , s.state_cases_sum
    , d.daily_total_cases
from
    state_daily_sum s
inner join
    daily_cases d
on
    s.date = d.date
where
    s.state_cases_sum != d.daily_total_cases
