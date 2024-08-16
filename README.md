# Scott's Fantasy Football Platform 2024

This is just a tool I made in two days to have easily accessible information that I could format in anyway I like(mostly graphs). I originally intended for this to be on a hosted relational database using the play by play as a fact table but when planning out how I would access the data it made more sense to use a series of documents.

` Insert old schema graph here`

The current data is setup as a hierachy where the `player_info` document drills down to the `games_info` document which drills down to a `play_info` table. There is also a seperate depth chart CSV which is a great reference and needs to be linked in players.

` Insert new schema here`

I still might host this using Mongo or another database tool depending on if I continue to use this and find a dataset which has full names and ids on one page (Tyreek Hill & Taysom Hill caused me more problems than I expected).


## Installation

Copy the github and double check the paths before you run anything

## Usage

Final copies of the datsets are in the queries folder along with a script containing some sample queries

DBSetup contains the scripts to build from scratch using the CSVs I created by scraping websites and the 2023 dataset linked[ here](https://nflsavant.com/about.php)

## Todo

* Bug occurs because of capitalization differences in names like LaPorta
* Handling duplicates in `playerMunging` requires manual input
* Find a new dataset
* Host online for access anywhere

## License

[MIT](https://choosealicense.com/licenses/mit/)
