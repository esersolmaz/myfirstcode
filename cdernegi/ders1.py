a = [10, 20, 30, 40, 50]

match a:
    case 10, _, _, 40, 50:
        print('matched')