% Facts 
% driver(Name, Team).
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

% Rule: X and Y are teammates if they drive for the same team.
teammates(X, Y) :-
    driver(X, Team),
    driver(Y, Team),
    X \= Y.