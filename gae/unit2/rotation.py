def rotate_13(text):
  if text:
    new_chars = []
    for token in text:
      new_chars.append(rotate_char(token, 13))
    return ''.join(new_chars)
  else:
    return ''

def rotate_char(c, times):
  if c and c.isalpha():
    if c.islower():
      return chr(add_with_rotation(ord('a'), ord('z') + 1, ord(c), times))
    else:
      return chr(add_with_rotation(ord('A'), ord('Z') + 1, ord(c), times))
  else:
    return c  

def add_with_rotation(lo, hi, num, diff):
  unrotated = num + diff

  if unrotated >= hi:
    return unrotated - hi + lo
  else:
    return unrotated