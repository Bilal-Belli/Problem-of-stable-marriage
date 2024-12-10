def gale_shapley_modified(candidates_prefs, establishments_prefs):
    free_candidates = list(candidates_prefs.keys())
    proposals = {candidate: [] for candidate in candidates_prefs}
    matches = {establishment: [] for establishment in establishments_prefs}
    candidate_to_establishment = {candidate: None for candidate in candidates_prefs}
    while free_candidates:
        candidate = free_candidates.pop(0)
        for establishment in candidates_prefs[candidate]:
            if establishment not in proposals[candidate]:
                proposals[candidate].append(establishment)
                print(f"{candidate} propose à {establishment}.")
                if len(matches[establishment]) < establishments_prefs[establishment]["capacity"]:
                    matches[establishment].append(candidate)
                    candidate_to_establishment[candidate] = establishment
                    print(f"{establishment} accepte {candidate} (place disponible).\n")
                    break
                else:
                    current_candidates = matches[establishment]
                    worst_current = min(current_candidates, key=lambda c: establishments_prefs[establishment]["preferences"].index(c) 
                                        if c in establishments_prefs[establishment]["preferences"] else float('inf'))
                    if candidate in establishments_prefs[establishment]["preferences"]:
                        if establishments_prefs[establishment]["preferences"].index(candidate) < establishments_prefs[establishment]["preferences"].index(worst_current):
                            matches[establishment].remove(worst_current)
                            matches[establishment].append(candidate)
                            candidate_to_establishment[candidate] = establishment
                            candidate_to_establishment[worst_current] = None
                            free_candidates.append(worst_current)
                            print(f"{establishment} préfère {candidate} à {worst_current}. {worst_current} redevient libre.\n")
                            break
                        elif establishments_prefs[establishment]["preferences"].index(candidate) == establishments_prefs[establishment]["preferences"].index(worst_current):
                            matches[establishment].append(candidate)
                            candidate_to_establishment[candidate] = establishment
                            print(f"{establishment} accepte {candidate} (égalité de préférence).\n")
                            break
                    print(f"{establishment} préfère garder ses candidats actuels.\n")
    return candidate_to_establishment

def satisfaction(matches, candidates_prefs, establishments_prefs):
    satisfied_candidates = 0
    satisfied_establishments = 0
    for candidate, establishment in matches.items():
        if establishment is not None:
            if establishment in candidates_prefs[candidate]:
                rank = candidates_prefs[candidate].index(establishment)
                if rank < len(candidates_prefs[candidate]) // 2:
                    satisfied_candidates += 1
    
    for establishment in establishments_prefs:
        matched_candidates = [candidate for candidate, est in matches.items() if est == establishment]
        for candidate in matched_candidates:
            if candidate in establishments_prefs[establishment]["preferences"]:
                rank = establishments_prefs[establishment]["preferences"].index(candidate)
                if rank < len(establishments_prefs[establishment]["preferences"]) // 2:
                    satisfied_establishments += 1
    
    total_candidates = len(candidates_prefs)
    total_establishments = len(establishments_prefs)
    print(f"Satisfaction des candidats: {satisfied_candidates}/{total_candidates} ({satisfied_candidates / total_candidates:.2%})")
    print(f"Satisfaction des établissements: {satisfied_establishments}/{total_establishments} ({satisfied_establishments / total_establishments:.2%})")

if __name__ == "__main__":
    candidates_prefs = {
        "C1": ["E1", "E2"],
        "C2": ["E2", "E3", "E1"],
        "C3": ["E1", "E3"],
        "C4": ["E2", "E1"],
    }
    establishments_prefs = {
        "E1": {"preferences": ["C3", "C1", "C4"], "capacity": 2},
        "E2": {"preferences": ["C1", "C2", "C4"], "capacity": 1},
        "E3": {"preferences": ["C3", "C2"], "capacity": 1},
    }
    print("Execution de l'algorithme de Gale-Shapley modifié:\n")
    matches = gale_shapley_modified(candidates_prefs, establishments_prefs)
    print("\nCorrespondances finales:")
    for candidate, establishment in matches.items():
        print(f"{candidate} - {establishment}")
    print("\nEvaluation de la satisfaction:\n")
    satisfaction(matches, candidates_prefs, establishments_prefs)