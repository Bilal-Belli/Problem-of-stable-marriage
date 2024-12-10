def gale_shapley(candidates_prefs, establishments_prefs):
    """
    Implémente l'algorithme de Gale-Shapley pour le problème de mariage stable.
    """
    free_candidates = list(candidates_prefs.keys())
    proposals = {candidate: [] for candidate in candidates_prefs}
    matches = {establishment: None for establishment in establishments_prefs}
    candidate_to_establishment = {candidate: None for candidate in candidates_prefs}

    while free_candidates:
        candidate = free_candidates.pop(0)
        for establishment in candidates_prefs[candidate]:
            if establishment not in proposals[candidate]:
                proposals[candidate].append(establishment)
                print(f"{candidate} propose à {establishment}.")

                # Si l'établissement est libre
                if matches[establishment] is None:
                    matches[establishment] = candidate
                    candidate_to_establishment[candidate] = establishment
                    print(f"{establishment} accepte {candidate} (aucun candidat précédent).\n")
                    break

                # Sinon, l'établissement compare avec son candidat actuel
                else:
                    current_candidate = matches[establishment]
                    if establishments_prefs[establishment].index(candidate) < \
                        establishments_prefs[establishment].index(current_candidate):
                            matches[establishment] = candidate
                            candidate_to_establishment[candidate] = establishment
                            candidate_to_establishment[current_candidate] = None
                            free_candidates.append(current_candidate)
                            print(f"{establishment} préfère {candidate} à {current_candidate}. {current_candidate} redevient libre.\n")
                            break
                    else:
                        print(f"{establishment} préfère rester avec {current_candidate}.\n")
    return candidate_to_establishment

def satisfaction(matches, candidates_prefs, establishments_prefs):
    """
    Calcule la satisfaction des candidats et des établissements.
    """
    satisfied_candidates = 0
    satisfied_establishments = 0
    # Satisfaction des candidats
    for candidate, establishment in matches.items():
        if establishment is not None:
            rank = candidates_prefs[candidate].index(establishment)
            if rank < len(candidates_prefs[candidate]) // 2:
                satisfied_candidates += 1
    # Satisfaction des établissements
    for establishment in establishments_prefs:
        matched_candidates = [candidate for candidate, est in matches.items() if est == establishment]
        for candidate in matched_candidates:
            rank = establishments_prefs[establishment].index(candidate)
            if rank < len(establishments_prefs[establishment]) // 2:
                satisfied_establishments += 1
    total_candidates = len(candidates_prefs)
    total_establishments = len(establishments_prefs)
    print(f"Satisfaction des candidats: {satisfied_candidates}/{total_candidates} ({satisfied_candidates / total_candidates:.2%})")
    print(f"Satisfaction des établissements: {satisfied_establishments}/{total_establishments} ({satisfied_establishments / total_establishments:.2%})")

if __name__ == "__main__":
    # Préférences des candidats
    candidates_prefs = {
        "C1": ["E1", "E2", "E3"],
        "C2": ["E2", "E3", "E1"],
        "C3": ["E1", "E3", "E2"],
    }

    # Préférences des établissements
    establishments_prefs = {
        "E1": ["C3", "C2", "C1"],
        "E2": ["C1", "C3", "C2"],
        "E3": ["C3", "C2", "C1"],
    }

    print("Execution de l'algorithme de Gale-Shapley:\n")
    matches = gale_shapley(candidates_prefs, establishments_prefs)

    print("\nCorrespondances finales:")
    for candidate, establishment in matches.items():
        print(f"{candidate} - {establishment}")

    print("\nEvaluation de la satisfaction:\n")
    satisfaction(matches, candidates_prefs, establishments_prefs)