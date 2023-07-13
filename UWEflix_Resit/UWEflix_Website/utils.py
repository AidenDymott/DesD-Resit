def is_valid_card_number(card_number):
    reversed = card_number[::-1]
    doubled = []
    for index, digit in enumerate(reversed):
        if index % 2 == 1:
            tmp = int(digit) * 2
            if tmp > 9:
                tmp -= 9
            doubled.append(tmp)
        else:
            doubled.append(int(digit))
    return sum(doubled) % 10 == 0
