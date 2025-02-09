with source_data as (
    select 
         data__date as date
        , data__state as state_id
        , data__meta__data_quality_grade
        , data__meta__updated
        , data__meta__tests__total_source
        , data__cases__total as cases_total
        , data__cases__confirmed
        , data__cases__probable
        , data__tests__pcr__total
        , data__tests__pcr__people__total
        , data__tests__pcr__people__positive
        , data__tests__pcr__people__negative
        , data__tests__antibody__people__total     
    from {{ source('covid19_states_data', 'state_daily_cases') }}
)
select *
from source_data