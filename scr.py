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


# def satisfaction(matches, candidates_prefs, establishments_prefs):
#     """
#     Calcule la satisfaction des candidats et des établissements.
#     """
#     satisfied_candidates = 0
#     satisfied_establishments = 0

#     # Satisfaction des candidats
#     for candidate, establishment in matches.items():
#         if establishment is not None:
#             rank = candidates_prefs[candidate].index(establishment)
#             if rank < len(candidates_prefs[candidate]) // 2:
#                 satisfied_candidates += 1

#     # Satisfaction des établissements
#     for establishment in establishments_prefs:
#         matched_candidates = [candidate for candidate, est in matches.items() if est == establishment]
#         for candidate in matched_candidates:
#             rank = establishments_prefs[establishment].index(candidate)
#             if rank < len(establishments_prefs[establishment]) // 2:
#                 satisfied_establishments += 1

#     total_candidates = len(candidates_prefs)
#     total_establishments = len(establishments_prefs)

#     print(f"Satisfaction des candidats: {satisfied_candidates}/{total_candidates} ({satisfied_candidates / total_candidates:.2%})")
#     print(f"Satisfaction des établissements: {satisfied_establishments}/{total_establishments} ({satisfied_establishments / total_establishments:.2%})")


def satisfaction_with_percentage(matches, candidates_prefs, establishments_prefs, candidates_percentages, establishments_percentages):
    """
    Calcule la satisfaction des candidats et des établissements selon un pourcentage spécifique.
    :param matches: dictionnaire des correspondances (candidat -> établissement).
    :param candidates_prefs: dictionnaire des préférences des candidats.
    :param establishments_prefs: dictionnaire des préférences des établissements.
    :param candidates_percentages: pourcentage de satisfaction pour chaque candidat.
    :param establishments_percentages: pourcentage de satisfaction pour chaque établissement.
    """
    satisfied_candidates = 0
    satisfied_establishments = 0

    # Satisfaction des candidats
    for candidate, establishment in matches.items():
        if establishment is not None:
            # Calcul de la limite selon le pourcentage
            limit = int(len(candidates_prefs[candidate]) * (candidates_percentages[candidate] / 100))
            rank = candidates_prefs[candidate].index(establishment)
            if rank < limit:
                satisfied_candidates += 1

    # Satisfaction des établissements
    for establishment in establishments_prefs:
        matched_candidates = [candidate for candidate, est in matches.items() if est == establishment]
        for candidate in matched_candidates:
            limit = int(len(establishments_prefs[establishment]) * (establishments_percentages[establishment] / 100))
            rank = establishments_prefs[establishment].index(candidate)
            if rank < limit:
                satisfied_establishments += 1

    total_candidates = len(candidates_prefs)
    total_establishments = len(establishments_prefs)

    print(f"Satisfaction des candidats: {satisfied_candidates}/{total_candidates} ({satisfied_candidates / total_candidates:.2%})")
    print(f"Satisfaction des établissements: {satisfied_establishments}/{total_establishments} ({satisfied_establishments / total_establishments:.2%})")


# if __name__ == "__main__":
#     # Préférences des candidats
#     candidates_prefs = {
#         "C1": ["E1", "E2", "E3"],
#         "C2": ["E2", "E3", "E1"],
#         "C3": ["E1", "E3", "E2"],
#     }

#     # Préférences des établissements
#     establishments_prefs = {
#         "E1": ["C3", "C2", "C1"],
#         "E2": ["C1", "C3", "C2"],
#         "E3": ["C3", "C2", "C1"],
#     }

#     print("Execution de l'algorithme de Gale-Shapley:\n")
#     matches = gale_shapley(candidates_prefs, establishments_prefs)

#     print("\nCorrespondances finales:")
#     for candidate, establishment in matches.items():
#         print(f"{candidate} - {establishment}")

#     print("\nEvaluation de la satisfaction:\n")
#     satisfaction(matches, candidates_prefs, establishments_prefs)

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

    # Pourcentages de satisfaction
    candidates_percentages = {
        "C1": 60,  # C1 est satisfait si son attribution est dans les 60% supérieurs de sa liste
        "C2": 50,  # C2 est satisfait si son attribution est dans les 50% supérieurs de sa liste
        "C3": 70,  # C3 est satisfait si son attribution est dans les 70% supérieurs de sa liste
    }

    establishments_percentages = {
        "E1": 50,  # E1 est satisfait si ses correspondances sont dans les 50% supérieurs de sa liste
        "E2": 60,  # E2 est satisfait si ses correspondances sont dans les 60% supérieurs de sa liste
        "E3": 70,  # E3 est satisfait si ses correspondances sont dans les 70% supérieurs de sa liste
    }

    print("Execution de l'algorithme de Gale-Shapley:\n")
    matches = gale_shapley(candidates_prefs, establishments_prefs)

    print("\nCorrespondances finales:")
    for candidate, establishment in matches.items():
        print(f"{candidate} - {establishment}")

    print("\nEvaluation de la satisfaction avec les pourcentages:\n")
    satisfaction_with_percentage(matches, candidates_prefs, establishments_prefs, candidates_percentages, establishments_percentages)