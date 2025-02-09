with state_daily_cases as (
    select
        state_id,
        date,
        cases_total
    from
        {{ ref('fct_state_daily_cases') }} 

),

state_population as (
    select
        state_code,
        state_population
    from
        {{ ref('dim_states_and_territories') }} 
)

select
    sdc.state_id,
    sdc.date,
    sdc.cases_total,
    sp.state_population,
    round((sdc.cases_total * 100.0) / sp.state_population, 2) AS percent_infected
from
    state_daily_cases sdc
JOIN
    state_population sp
ON
    sdc.state_id = sp.state_code
ORDER BY
    sdc.state_id,
    sdc.date
