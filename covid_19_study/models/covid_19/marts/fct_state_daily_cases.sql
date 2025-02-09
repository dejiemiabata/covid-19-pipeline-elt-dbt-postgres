select
    {{ dbt_utils.generate_surrogate_key(['date','state_id']) }} as id
    , date
    , state_id
    , cases_total
from 
    {{ ref('stg_state_daily_cases') }} 