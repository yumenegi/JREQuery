JREQuery
=============================
This is a tool created to easily query the live conditions of JR East railroad information. 

## Available Modules
### JREQuery
JREQuery allows the user to get live status of JR East rail line running conditions. 
### Ekitan
Ekitan, as the name suggests, queries Ekitan for timetable, station, and basic route information on any JR East rail line provided.
> Note that Ekitan separates Ueno-Tokyo Line from some train lines so in order to access train lines start from Tokyo/Ueno Station that converts into another line, make sure to query Ueno-Tokyo Line.

## Simple Usage Example
```python
    eki = Ekitan("中央線")
    stations = eki.get_all_stations()
    timetable_chuo_tokyo = eki.get_timetable_by_name("東京駅", 1)
```