from TurboCodeCoder import TurboCodeCoder
from TurboCodeDecoder import TurboCodeDecoder
from GaussianChannel import GaussianChannel

if __name__ == '__main__':

    input_string = 'aeshto smeshno'
    interleaver = [2,1,4,3,6,5,0]
    coder = TurboCodeCoder(interleaver)
    decoder = TurboCodeDecoder(interleaver, 16)
    channel = GaussianChannel(1.0,0.0)

    coded_string = coder.encode_string(input_string)

    transmitted_sequence = channel.transmit_sequence(coded_string)

    decoded_word = decoder.decode_sequence(transmitted_sequence)
    print([chr(int(x,base=2)) for x in decoded_word])

