from Coder import Coder


class HammingCodeCoder(Coder):
    def encode_integer(self, integer):
        binary_version = bin(integer)[2:]
        binary_version= "0"*(7-len(binary_version))+ binary_version

        iterator = iter(binary_version)

        return_list = list()
        for i in range(1, 12):
            if int.bit_count(i) == 1:
                return_list.append(0)
            else:
                return_list.append(int(next(iterator)))

        for i in range(1, 12):
            for mask in [1, 2, 4, 8]:
                if i & mask:
                    return_list[mask-1] = ((return_list[mask-1]) ^(return_list[i-1]))
        return_list = [str(x) for x in return_list]

        return "".join(return_list)

    def encode_string(self, string):
        return_string = ""

        for character in string:
            character_value = ord(character)
            return_string += self.encode_integer(character_value)

        return return_string



