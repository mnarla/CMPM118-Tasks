% ============================================================
%  F1 Knowledge Base (2024 Season Focus)
%  CMPM 118 - Task 4
%
%  Domain:   Formula 1 Racing
%  Entities: Drivers, Teams, Constructors
%  Relations: drives_for, champion, won_race, teammates,
%             podium, experienced, dominant_team, rivals
% ============================================================

% ---------- FACTS ----------

% drives_for(Driver, Team)
drives_for(max_verstappen,    red_bull).
drives_for(sergio_perez,      red_bull).
drives_for(lewis_hamilton,    mercedes).
drives_for(george_russell,    mercedes).
drives_for(charles_leclerc,   ferrari).
drives_for(carlos_sainz,      ferrari).
drives_for(lando_norris,      mclaren).
drives_for(oscar_piastri,     mclaren).
drives_for(fernando_alonso,   aston_martin).
drives_for(lance_stroll,      aston_martin).
drives_for(pierre_gasly,      alpine).
drives_for(esteban_ocon,      alpine).

% champion(Driver, Year)  — world champions
champion(max_verstappen, 2021).
champion(max_verstappen, 2022).
champion(max_verstappen, 2023).
champion(max_verstappen, 2024).
champion(lewis_hamilton,  2008).
champion(lewis_hamilton,  2014).
champion(lewis_hamilton,  2015).
champion(lewis_hamilton,  2017).
champion(lewis_hamilton,  2018).
champion(lewis_hamilton,  2019).
champion(lewis_hamilton,  2020).
champion(fernando_alonso, 2005).
champion(fernando_alonso, 2006).

% won_race(Driver, GrandPrix, Year)  — selected 2024 wins
won_race(max_verstappen, bahrain_gp,    2024).
won_race(max_verstappen, saudi_gp,      2024).
won_race(max_verstappen, australian_gp, 2024).
won_race(max_verstappen, japanese_gp,   2024).
won_race(max_verstappen, chinese_gp,    2024).
won_race(carlos_sainz,   australian_gp, 2024).  % Sainz won Aus before Verstappen streak
won_race(lando_norris,   miami_gp,      2024).
won_race(charles_leclerc,monaco_gp,     2024).
won_race(george_russell, austrian_gp,   2024).
won_race(lewis_hamilton,  british_gp,   2024).

% ---------- RULES ----------

% teammates(X, Y) — two drivers who drive for the same team
teammates(X, Y) :-
    drives_for(X, Team),
    drives_for(Y, Team),
    X \= Y.

% multi_champion(Driver) — won the championship more than once
multi_champion(Driver) :-
    champion(Driver, Y1),
    champion(Driver, Y2),
    Y1 \= Y2.

% race_winner(Driver) — drove to at least one race win in 2024
race_winner(Driver) :-
    won_race(Driver, _, 2024).

% team_winner(Team) — at least one of the team's drivers won a race in 2024
team_winner(Team) :-
    drives_for(Driver, Team),
    won_race(Driver, _, 2024).

% dominant(Driver) — won at least 4 races in 2024
dominant(Driver) :-
    findall(GP, won_race(Driver, GP, 2024), Wins),
    length(Wins, N),
    N >= 4.

% rivals(X, Y) — compete for the same championship year
rivals(X, Y) :-
    champion(X, Year),
    champion(Y, Year),
    X \= Y.

% experienced(Driver) — has been champion AND won a 2024 race
experienced(Driver) :-
    multi_champion(Driver),
    race_winner(Driver).
