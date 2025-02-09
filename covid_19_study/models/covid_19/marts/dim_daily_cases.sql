select
    date
    , cases_total
from 
    {{ ref('stg_daily_cases') }} 