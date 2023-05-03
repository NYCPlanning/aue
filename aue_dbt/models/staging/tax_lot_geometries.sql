-- Limit tax lot data to columns needed for AUE analysis

with tax_lot_geometries as (
    select
        bbl,
        borocode,
        cast(wkb_geometry as geometry) as wkb_geometry
    from {{ source('source_data', var('input_version')) }}
)

select * from tax_lot_geometries
