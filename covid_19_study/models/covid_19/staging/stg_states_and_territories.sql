with source_data as (
    select 
        name
        , state_code
        , fips
        , census__population as state_population
        , field_sources__tests__pcr__total
        , covid_tracking_project__preferred_total_test__field
        , covid_tracking_project__preferred_total_test__units
    from {{ source('covid19_states_data', 'states_and_territories') }}
)
select *
from source_data

