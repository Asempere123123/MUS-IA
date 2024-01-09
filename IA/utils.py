BARAJA_ESPAÑOLA = [
    1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 10, 11,
    12, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12]

class Player:
    def __init__(self, cards, score):
        self.cards = cards
        self.score = score

def get_hand_scores(player):

    #Tabla a la grande y chica(no se hacer hashmaps)
    grande = [0, 2, 2, 9, 3, 4, 5, 6, 0, 0, 7, 8, 9]
    chica = [0, 9, 9, 2, 8, 7, 6, 5, 0, 0, 4, 3, 2]

    grande_scores = [0, 0, 0, 0]
    chica_scores  = [0, 0, 0, 0]
    for i in range(4):
        grande_scores[i] = grande[player.cards[i]]
        chica_scores[i] = chica[player.cards[i]]
    grande_scores.sort()
    chica_scores.sort()

    grande_score = 0
    chica_score = 0
    for i in range(4):
        grande_score += grande_scores[i] * (10**i)
        chica_score += chica_scores[i] * (10**i)

    #Pares
    pair_tier = 0 # 0 --> no pair | 1--> Dobles | 2--> triple |3 --> duples
    pair_score = 0
    pair_already = 0
    
    if grande_scores[0] == grande_scores[1] and grande_scores[2] == grande_scores[3]:
        pair_tier = 3
        if grande_scores[0] > grande_scores[2]:
            pair_score = grande_scores[0]
        else:
            pair_score = grande_scores[2]
        
    else:
        for i in range(len(grande_scores) - 1):
            if grande_scores[i] == grande_scores[i + 1]:
                if pair_already == 1:
                    if pair_tier < 2:
                        pair_tier = 2
                        pair_score = grande_scores[i]

                if pair_tier < 1:
                    pair_tier = 1
                    pair_score = grande_scores[i]
                pair_already += 1
    
    pair_score = (10**pair_tier) * pair_score

    #puntijuego
    suma_punto = 0
    for i in range(4):
        if player.cards[i] in [3, 10, 11, 12]:
            suma_punto += 10
        elif player.cards[i] in [1, 2]:
            suma_punto += 1
        else:
            suma_punto += player.cards[i]

    juego_score = 0
    if suma_punto == 31:
        juego_score = 99
    elif suma_punto == 32:
        juego_score = 98
    else:
        juego_score = suma_punto
    if suma_punto >= 31 :
        juego_score *= 100

    player.score = [grande_score, chica_score, pair_score, juego_score]