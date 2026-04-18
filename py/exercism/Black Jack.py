def value_of_card(card):
    card = card.upper()
    face_cards = {
        'J':10,
        'Q':10,
        'K':10,
        'A':1
}
    if card in face_cards:
        return face_cards[card]
    else:
        return int(card)

def higher_card(card_one, card_two):
    v1 = value_of_card(card_one)
    v2 = value_of_card(card_two)
    if v1 == v2:
        return card_one, card_two
    elif v1 > v2:
        return card_one
    else:
        return card_two

def value_of_ace(card_one, card_two):
    v1 = value_of_card(card_one)
    v2 = value_of_card(card_two)
    if card_one.upper() == 'A' or card_two.upper() == 'A':
        return 1
    elif (v1 + v2 + 11) > 21:
        return 1
    else:
        return 11

def is_blackjack(card_one, card_two):
    x = ['10', 'J', 'Q', 'K']
    c1 = card_one.upper()
    c2 = card_two.upper()

    if (c1 == 'A' and c2 in x) or (c2 == 'A' and c1 in x):
        return True
    else:
        return False

def can_split_pairs(card_one, card_two):
    v1 = value_of_card(card_one)
    v2 = value_of_card(card_two)
    if v1 == v2:
        return True
    else:
        return False

def can_double_down(card_one, card_two):
    v1 = value_of_card(card_one)
    v2 = value_of_card(card_two)
    if v1 + v2 in range(9,12):
        return True
    else:
        return False