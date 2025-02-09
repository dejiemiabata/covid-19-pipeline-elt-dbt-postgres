select
    name
    , state_code
    , state_population
from 
    {{ ref('stg_states_and_territories') }}