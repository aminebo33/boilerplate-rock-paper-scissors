def player(prev_play, opponent_history=[], my_history=[], patterns={}):
    if prev_play:
        opponent_history.append(prev_play)
    else:
        opponent_history.clear()
        my_history.clear()
        patterns.clear()

    if len(my_history) < 3:
        guess = "R"
        my_history.append(guess)
        return guess

    # Track sequence combos of what we played and what they played
    last_combination = my_history[-1] + opponent_history[-1]
    
    if len(opponent_history) >= 3:
        # Abbey and Kris counter: track double pairs to catch recursive behaviors
        seq = "".join([my_history[i] + opponent_history[i] for i in range(len(opponent_history)-2, len(opponent_history))])
        
        if seq not in patterns:
            patterns[seq] = {"R": 0, "P": 0, "S": 0}
        
        # Look back at what they played last time this sequence happened
        if len(opponent_history) > 3:
            prev_seq = "".join([my_history[i] + opponent_history[i] for i in range(len(opponent_history)-3, len(opponent_history)-1)])
            if prev_seq in patterns:
                patterns[prev_seq][prev_play] += 1

        # Predict next opponent move based on historical sequence tracking
        if seq in patterns and sum(patterns[seq].values()) > 0:
            predicted = max(patterns[seq], key=patterns[seq].get)
        else:
            # Fallback to general history frequency
            last_three = "".join(opponent_history[-3:])
            combos = [last_three + move for move in ["R", "P", "S"]]
            full_hist = "".join(opponent_history)[:-1]
            counts = {c: full_hist.count(c) for c in combos}
            predicted = max(counts, key=counts.get)[-1] if sum(counts.values()) > 0 else "R"
    else:
        predicted = "R"

    counters = {"R": "P", "P": "S", "S": "R"}
    guess = counters[predicted]
    
    my_history.append(guess)
    return guess
