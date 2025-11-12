import itertools
import numpy as np

def Equipe(name, rank, nationality, group):
    """
    Create a team entry for the draw

    Parameters
    ----------
    name : str
        Team name
    rank : int
        Team rank in its group (1 for first, 2 for second)
    nationality : str
        Team nationality (country)
    group : str
        Group letter (A–H)

    Returns
    -------
    list
        List containing [name, rank, nationality, group]
    """
    return [name, rank, nationality, group]


def Match(team1, team2):
    """
    Create a match between two teams

    Parameters
    ----------
    team1 : list
        First team (from pot 1)
    team2 : list
        Second team (from pot 2)

    Returns
    -------
    tuple
        Tuple (team1, team2)
    """
    return (team1, team2)


def bijections_possibles(set1, set2):
    """
    Generate all possible bijections (pairings) between two sets of teams

    Parameters
    ----------
    set1 : list
        Teams from pot 1
    set2 : list
        Teams from pot 2

    Returns
    -------
    list of list of tuple
        All valid one-to-one mappings between teams from set1 and set2
    """
    return [list(zip(set1, perm)) for perm in itertools.permutations(set2)]


def MatchImpossible(match):
    """
    Check whether a match violates the draw rules

    Rules
    -----
    - Same group → forbidden
    - Same nationality → forbidden
    - Same rank → forbidden

    Parameters
    ----------
    match : tuple
        Tuple (team1, team2)

    Returns
    -------
    int
        0 if the match is impossible, 1 otherwise
    """
    team1, team2 = match
    if team1[1] == team2[1] or team1[2] == team2[2] or team1[3] == team2[3]:
        return 0
    return 1


def ListeConfigurationsPossibles(pot1, pot2):
    """
    List all mathematically possible draw configurations and remove invalid ones

    Parameters
    ----------
    pot1 : list
        Teams from pot 1
    pot2 : list
        Teams from pot 2

    Returns
    -------
    list of list of tuple
        All valid configurations (list of valid match tuples)
    """
    all_configs = bijections_possibles(pot1, pot2)
    valid_configs = [config for config in all_configs if all(MatchImpossible(m) for m in config)]
    return valid_configs


def DetectionErreurs(match, pot1, pot2):
    """
    Check for inconsistent or invalid input data

    Parameters
    ----------
    match : tuple
        Match to check (team1, team2)
    pot1 : list
        Teams from pot 1
    pot2 : list
        Teams from pot 2

    Returns
    -------
    tuple
        (status, message)
        - status = 1 if OK, 0 if an error was detected
        - message = diagnostic string
    """
    if len(pot1) != 8:
        return (0, "Error: Pot 1 must contain exactly 8 teams")
    if len(pot2) != 8:
        return (0, "Error: Pot 2 must contain exactly 8 teams")
    if match[0] not in pot1:
        return (0, f"Error: {match[0]} is not in Pot 1")
    if match[1] not in pot2:
        return (0, f"Error: {match[1]} is not in Pot 2")
    if MatchImpossible(match) == 0:
        return (0, "p=0 because the match is forbidden by the rules")
    return (1, "OK")


def TableauProbas2023(pot1, pot2):
    """
    Compute the probability table of all possible matches between two pots

    Enumerates all valid configurations and counts
    the frequency of each possible valid matchup

    Parameters
    ----------
    pot1 : list
        8 teams from pot 1
    pot2 : list
        8 teams from pot 2

    Returns
    -------
    np.ndarray
        (8x8) numpy array of probabilities where [i, j] corresponds
        to the probability that pot1[i] faces pot2[j]

    Notes
    -----
    - The total number of valid configurations is used as denominator
    - Impossible matches (same country/group/rank) are assigned probability 0
    """
    valid_configs = ListeConfigurationsPossibles(pot1, pot2)
    total = len(valid_configs)
    proba_table = np.zeros((8, 8))

    for i, team1 in enumerate(pot1):
        for j, team2 in enumerate(pot2):
            match = (team1, team2)
            if MatchImpossible(match) == 0:
                proba_table[i, j] = 0
            else:
                count = sum(match in config for config in valid_configs)
                proba_table[i, j] = count / total
    return proba_table
