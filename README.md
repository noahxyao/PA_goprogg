# Riot Games API

Things to keep in mind when new patches release:

* champion.json was pulled from DDragon online and needs to be updated
* item.json was pulled from DDragon online and needs to be updated
* Square Assets are pulled from LeagueWiki (but could also be pulled from DDragon) and might need to be updated


## Understanding Stats
* DPM > 500 and DMG% > 25% indicates he's carrying the team, could also mean the rest sucks ass
* GOLD% < DMG% indicates he's being more efficient with gold for dmg than others
* KP indicates heavy roams and team play
* positive CSD and GD  @15 indicates won lane
* Team GOLD diff @15 indicates how far a team is ahead. Good for analysing team strengths/weaknesses throughout game phases
* DRG%, HLD%, BN% for analysing objective control, but generally higher for winning games

## Further Things to be done:
* DB related
    * Import Timeline API Data to database
        * set up auto updater
        * migrate new table to django
        * update on PA
    * Implement method to enter new summoners into database and pull quick data of 20 games
* Add tabs for champ mastery, etc
* Add tab for education on stats, how to read them, graphs
* Add More interesting stats: 
	-CS Difference @ 15 Min -> CSD @ 15
	-Gold Difference @ 15 min -> GD @ 15
    -Champion Mastery in Ranked
    
    
    
    