with tax_lot_geometries as (
    select * from {{ ref('stg_dcp__restricted_lots') }}
),

borough_best_times as (
    select * from {{ ref('stg_dcp__borough_times') }}
),

tax_lot_best_time as (
    select
        tax_lot_geometries.*,
        borough_best_times.borough_name,
        borough_best_times.best_time
    from tax_lot_geometries
    left join
        borough_best_times
        on tax_lot_geometries.borocode = borough_best_times.borough_code
)

select * from tax_lot_best_time
