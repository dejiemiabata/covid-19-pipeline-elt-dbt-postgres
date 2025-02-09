with source_data as (
    select 
        data__date as date
        , data__states
        , data__cases__total as cases_total
        , data__testing__total
        , data__outcomes__hospitalized__currently
        , data__outcomes__hospitalized__in_icu__currently
        , data__outcomes__hospitalized__on_ventilator__currently
        , data__outcomes__death__total
    from {{ source('covid19_states_data', 'daily_cases') }}
)
select *
from source_data

