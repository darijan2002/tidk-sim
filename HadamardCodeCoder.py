from Coder import Coder
import numpy as np

# n,k,d = 2**k, k+1, 2**(k-1)
# augmented hadamard code
class HadamardCodeCoder(Coder):
  def __init__(self, r=5):
    self.r = r
    cols = [x for x in range(2**(r-1))]
    bit_cols = [f'{x:0{r}b}' for x in cols]
    ibit_cols = [[int(x) for x in y] for y in bit_cols]
    self.G = np.array(ibit_cols)
    self.G = np.asmatrix(self.G)
    # self.G = np.transpose(self.G)

    # print(self.G)

  def encode_integer(self, k: int):
    # k' = Gk
    # message length = r+1 (imagine extra 0)
    bk = np.array([int(x) for x in f'{k:0{self.r}b}'])

    coded = np.matmul(self.G, bk) % 2

    return coded

  def encode_string(self, string):
    return_string = ""

    for character in string:
      character_value = ord(character)

      uh = self.encode_integer(character_value >> 4)
      lh = self.encode_integer(character_value & 0xf)

      # print(uh, lh)

      return_string += "".join(map(str, uh.tolist()[0]))
      return_string += "".join(map(str, lh.tolist()[0]))

    return return_string
  
  def encode_binary_vector(self, vec):
    output = []
    k = int("".join(vec.astype(str)), 2)

    uh = self.encode_integer(k >> 4)
    lh = self.encode_integer(k & 0xf)

    # print(uh, lh)

    output += uh.tolist()[0]
    output += lh.tolist()[0]

    return output


if __name__ == '__main__':
  c = HadamardCodeCoder()
  # print(c.encode_integer(5))
  print("".join(str(x) for x in c.encode_binary_vector(np.array([1,0,0,0,0,0,1]))))
  print(c.encode_string('A'))
  # print(c.encode_string('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sed fringilla orci. Integer accumsan ornare placerat. Vestibulum a purus ut risus aliquam molestie sed eget neque. Maecenas vehicula sem justo, quis rhoncus nulla sollicitudin non. Ut non sem orci. Aliquam erat volutpat. Etiam congue sodales elit non laoreet. Morbi semper gravida ex, ac suscipit sem varius ut. Curabitur posuere nec massa vitae venenatis. Proin dapibus ex at interdum lacinia. Proin pulvinar lorem lacus, quis efficitur metus viverra eu. Mauris a nisl venenatis, feugiat odio non, mattis neque. In velit arcu, sagittis vel neque eu, convallis condimentum tortor.'))