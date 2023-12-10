from GaussianForTests import GaussianForTests
from HammingCodeCoder import HammingCodeCoder
from HammingCodeDecoder import HammingCodeDecoder
from HammingCodePlusParityCoder import HammingCodePlusParityCoder
from HammingCodePlusParityDecoder import HammingCodePlusParityDecoder
from TurboCodeCoder import TurboCodeCoder
from TurboCodeDecoder import TurboCodeDecoder
import random
import numpy as np
import matplotlib.pyplot as plot

def create_ber_plot(plot_params):
    block_size = plot_params["block_size"]
    num_trials = plot_params["num_trials"]

    snr_range = np.linspace(*plot_params["snr"])

    interleaver = random.sample(range(0, block_size), block_size)
    turbo_coder = TurboCodeCoder(interleaver)
    turbo_decoder = TurboCodeDecoder(interleaver,32)
    hamming_coder = HammingCodeCoder()
    hamming_decoder = HammingCodeDecoder()
    ext_hamming_coder = HammingCodePlusParityCoder()
    ext_hamming_decoder = HammingCodePlusParityDecoder()

    ext_hamming_coded_errors = np.zeros(len(snr_range))
    hamming_coded_errors = np.zeros(len(snr_range))
    turbo_coded_errors = np.zeros(len(snr_range))
    uncoded_errors = np.zeros(len(snr_range))

    for n in range(len(snr_range)):
        for _ in range(num_trials):
            input_vector = np.random.randint(2, size=block_size)
            turbo_encoded_vector = turbo_coder.encode_bits(input_vector)
            hamming_encoded_vector = hamming_coder.encode_string()
            channel = GaussianForTests(snr_range[n])

            turbo_channel_vector = list(map(float, turbo_encoded_vector))
            hamming_channel_vector = list(map(float, hamming_encoded_vector))
            ext_hamming_channel_vector = list(map(float,ext_hamming_encoded_vector))

            channel_vector = channel.convert_to_symbols(channel_vector)

            uncoded_vector = list(map(float, input_vector))
            uncoded_vector = channel.convert_to_symbols(uncoded_vector)
            uncoded_vector = channel.transmit_sequence(uncoded_vector)

            hamming_channel_vector = channel.transmit_sequence(hamming_channel_vector)

            turbo_decoded_vector = turbo_decoder.decode_vector_for_tests(channel_vector)
            hamming_decoded_vector =[int(c) for c in hamming_decoder.decode("".join(channel_vector))]
            ext_hamming_decoded_vector = [int(c) for c in ext_hamming_decoder.decode("".join(channel_vector))]


            turbo_decoded_vector = [int(b > 0.0) for b in turbo_decoded_vector]
            uncoded_vector = [int(b > 0.0) for b in uncoded_vector]
            hamming_decoded_vector = [int(b > 0.0) for b in hamming_decoded_vector]
            ext_hamming_decoded_vector = [int(b > 0.0) for b in ext_hamming_decoded_vector]

            turbo_decoder.reset()
            ext_hamming_coded_error_count = sum([x^y for x,y in zip(input_vector,ext_hamming_decoded_vector)])
            hamming_coded_error_count = sum([x^y for x,y in zip(input_vector,hamming_decoded_vector)])
            turbo_coded_error_count = sum([x ^ y for x, y in zip(input_vector, turbo_decoded_vector)])
            uncoded_error_count = sum([x ^ y for x, y in zip(input_vector, uncoded_vector)])

            turbo_coded_errors[n] = turbo_coded_errors[n] + turbo_coded_error_count
            hamming_coded_errors[n]  = hamming_coded_errors[n] + hamming_coded_error_count
            ext_hamming_coded_errors = ext_hamming_coded_errors[n] + ext_hamming_coded_error_count
            uncoded_errors[n] = uncoded_errors[n] + uncoded_error_count

        print("Finished {} trials for SNR = {:8.2f} dB ...".format(num_trials, snr_range[n]))
    hamming_ber_values = hamming_coded_errors / (num_trials * block_size)
    turbo_coded_ber_values = turbo_coded_errors / (num_trials * block_size)
    uncoded_ber_values = uncoded_errors / (num_trials * block_size)
    ext_hamming_ber_values = ext_hamming_coded_errors / (num_trials * block_size)

    plot.plot(snr_range, turbo_coded_ber_values, "r.-", label="Турбо код")
    plot.plot(snr_range, uncoded_ber_values, "b.-", label="Без код")
    plot.plot(snr_range, hamming_ber_values, "g.-", label="Hamming")
    plot.plot(snr_range, ext_hamming_ber_values, "y.-", label="Extended Hamming")

    plot.ylim(bottom=10**(-2.5))
    plot.yscale("log")
    plot.title("Turbo Codes Performance for R=1/3, Block={}, Trials={}".format(block_size, num_trials))
    plot.xlabel("SNR [dB]")
    plot.ylabel("Bit Error Rate (BER)")
    plot.grid(visible=True,which="major", linestyle="-")
    plot.grid(visible=True,which="minor", linestyle="--")
    plot.legend()
    plot.show()


if __name__ == '__main__':

    create_ber_plot({'block_size':7,'num_trials':50,'snr':[-10,20,20]})