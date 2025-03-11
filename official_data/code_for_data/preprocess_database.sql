use football_stats;

ALTER TABLE info_players
ADD PRIMARY KEY (playerId);

ALTER TABLE info_teams
ADD PRIMARY KEY (teamId);

ALTER TABLE info_tournaments_seasons
ADD PRIMARY KEY (seasonId);

ALTER TABLE stats_season
ADD PRIMARY KEY (ID),
add foreign key (teamId) references info_teams(teamId),
add foreign key (seasonId) references info_tournaments_seasons(seasonId),
add foreign key (playerId) references info_players(playerId);

ALTER TABLE `stats_tackles_success`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_aerial_success`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_assists_type`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_blocks_type`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_cards_type`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_clearances_success`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_dribbles_success`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_fouls_type`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_goals_bodyparts`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_goals_situations`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_goals_zones`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_interception_success`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_key_passes_length`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_key_passes_type`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_offsides_type`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_passes_length`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_passes_type`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_possession_loss_type`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_saves_shotzone`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_shots_accuracy`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_shots_bodyparts`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE `stats_shots_situations`	add foreign key (ID) references stats_season(ID),
	add primary key (ID);
ALTER TABLE stats_shots_zones add foreign key (ID) references stats_season(ID),
	add primary key (ID);
    
alter table stats_season
drop column teamRegionName;
alter table stats_goals_zones
drop column goalTotal;
alter table `stats_goals_bodyparts`
drop column goalTotal;

alter table stats_shots_accuracy
drop column shotsTotal;
alter table stats_shots_bodyparts
drop column shotsTotal;
alter table stats_shots_situations 
drop column shotsTotal;
