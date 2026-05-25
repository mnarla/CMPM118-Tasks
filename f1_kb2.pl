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
teammates(X, Y) :-
    driver(X, Team),
    driver(Y, Team),
    X \= Y.

% 2. Engine Customers
engine_customer(Team, Engine) :-
    constructor_engine(Team, Engine),
    Team \= Engine.

% 3. Works Team
works_team(Team) :-
    constructor_engine(Team, Team).

% 4. Rival Drivers
rival_drivers(X, Y) :-
    driver(X, TeamX),
    driver(Y, TeamY),
    TeamX \= TeamY.

% 5. Veteran Driver
veteran_driver(X) :-
    gp_wins(X, Wins),
    Wins > 10.

% 6. Race Winner
race_winner(X) :-
    gp_wins(X, Wins),
    Wins >= 1.