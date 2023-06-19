with events as (select * from {{ source('raw', 'events') }}) select * from events
