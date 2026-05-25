% Facts

% driver(DriverName, Team).
driver(lewis_hamilton, ferrari).
driver(charles_leclerc, ferrari).
driver(max_verstappen, red_bull).
driver(isack_hadjar, red_bull).
driver(lando_norris, mclaren).
driver(oscar_piastri, mclaren).
driver(george_russell, mercedes).
driver(kimi_antonelli, mercedes).
driver(fernando_alonso, aston_martin).
driver(lance_stroll, aston_martin).

% constructor_engine(Team, EngineSupplier).
constructor_engine(ferrari, ferrari).
constructor_engine(red_bull, red_bull_powertrains).
constructor_engine(mclaren, mercedes).
constructor_engine(mercedes, mercedes).
constructor_engine(aston_martin, honda).

% gp_wins(Driver, NumberOfWins).
gp_wins(lewis_hamilton, 103).
gp_wins(max_verstappen, 62).
gp_wins(fernando_alonso, 32).
gp_wins(charles_leclerc, 8).
gp_wins(lando_norris, 4).
gp_wins(george_russell, 2).
gp_wins(oscar_piastri, 2).
gp_wins(lance_stroll, 0).
gp_wins(isack_hadjar, 0).
gp_wins(kimi_antonelli, 0).

% RULES 

% 1. Teammates
% Two drivers are teammates if they drive for the same F1 constructor team and are not the same person.
teammates(X, Y) :-
    driver(X, Team),
    driver(Y, Team),
    X \= Y.

% 2. Engine Customers
% A team is considered an engine customer if they purchase and use an engine supplied by a different entity (i.e. the team name is different from the engine name).
engine_customer(Team, Engine) :-
    constructor_engine(Team, Engine),
    Team \= Engine.

% 3. Works Team
% A works team is a manufacturer that builds both its own chassis and its own engine (i.e. the team name matches the engine name).
works_team(Team) :-
    constructor_engine(Team, Team).

% 4. Rival Drivers
% Drivers are considered rivals if they drive for different teams (and therefore compete against each other).
rival_drivers(X, Y) :-
    driver(X, TeamX),
    driver(Y, TeamY),
    TeamX \= TeamY.

% 5. Veteran Driver
% A driver is considered a veteran driver if they have won more than 10 Grand Prix races in their career.
veteran_driver(X) :-
    gp_wins(X, Wins),
    Wins > 10.

% 6. Race Winner
% A driver is a race winner if they have finished first in at least 1 Grand Prix (wins >= 1).
race_winner(X) :-
    gp_wins(X, Wins),
    Wins >= 1.