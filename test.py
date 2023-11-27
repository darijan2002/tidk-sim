from TurboCodeCoder import TurboCodeCoder
from TurboCodeDecoder import TurboCodeDecoder
from GausianChannel import GausianChannel

if __name__ == '__main__':

    input_string = 'neshto smeshno'
    interleaver = [2,1,4,3,6,5,0]
    coder = TurboCodeCoder(interleaver)
    decoder = TurboCodeDecoder(interleaver, 16)
    channel = GausianChannel(1.0,0.0)
    for c in input_string:
        coded_string = coder.encode_string(c)
        transmitted_sequence = [channel.transmit_bit(b) for b in coded_string]

    decoded_word = decoder.decode(transmitted_sequence)
    print(decoded_word[:-2])

