from classes import LengthClass

# def parse_len_classes(line):
#     try:
#         parts = line.split()
#         if len(parts) != 4:
#             raise ValueError("Error!\nLEN_CLASSES correct form:\n<class lengths> <p_cata_cond> <p_cata_cll> <specificity>")
        
#         classes = list(map(int, parts[0].split(',')))
#         return [LengthClass(classes, float(parts[1]), float(parts[2]), int(parts[3]))]
#     except (ValueError, IndexError) as e:
#         raise ValueError(f"Error parsing LEN_CLASSES: {str(e)}")

def _parse_len_classes(self, line):
    parts = line.split()
    if len(parts) != 4:
        raise ValueError("Error!\nLEN_CLASSES correct form:\n<class lengths> <p_cata_cond> <p_cata_cll> <specificity>")
    classes = parts[0].split(',')
    p_cata_cond = float(parts[1])
    p_cata_cll = float(parts[2])
    specificity = int(parts[3])
    return [LengthClass(cls, p_cata_cond, p_cata_cll, specificity) for cls in classes]