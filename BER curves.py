from GaussianForTests import GaussianForTests
from HadamardCodeCoder import HadamardCodeCoder
from HadamardCodeDecoder import HadamardCodeDecoder
from TurboCodeCoder import TurboCodeCoder
from TurboCodeDecoder import TurboCodeDecoder
import random
import numpy as np
import matplotlib.pyplot as plot

from scipy.interpolate import make_interp_spline, BSpline

def create_ber_plot(plot_params):
    block_size = plot_params["block_size"]
    num_trials = plot_params["num_trials"]

    snr_range = np.linspace(*plot_params["snr"])

    interleaver = random.sample(range(0, block_size), block_size)
    turbo_coder = TurboCodeCoder(interleaver)
    turbo_decoder = TurboCodeDecoder(interleaver,32)
    hadamard_coder = HadamardCodeCoder()
    hadamard_decoder = HadamardCodeDecoder()

    hadamard_coded_errors = np.zeros(len(snr_range))
    turbo_coded_errors = np.zeros(len(snr_range))
    uncoded_errors = np.zeros(len(snr_range))

    input_vectors = [np.random.randint(2, size=block_size) for i in range(num_trials)]
    
    """
    TODO:
    PER (package error rate)
    similar transmission rates
    """
    
    for n in range(len(snr_range)):
        for input_vector in input_vectors:
            turbo_encoded_vector = turbo_coder.encode_bits(input_vector)
            hadamard_encoded_vector = hadamard_coder.encode_binary_vector(input_vector)

            channel = GaussianForTests(snr_range[n])


            turbo_channel_vector = list(map(float, turbo_encoded_vector))
            hadamard_channel_vector = list(map(float, hadamard_encoded_vector))
            uncoded_vector = list(map(float, input_vector))

            turbo_channel_vector = channel.convert_to_symbols(turbo_channel_vector)
            hadamard_channel_vector = channel.convert_to_symbols(hadamard_channel_vector)
            uncoded_vector = channel.convert_to_symbols(uncoded_vector)


           # ext_hamming_channel_vector = channel.transmit_sequence(ext_hamming_channel_vector)
            uncoded_channel_vector = channel.transmit_sequence(uncoded_vector)
            hadamard_channel_vector = channel.transmit_sequence(hadamard_channel_vector)
            turbo_channel_vector = channel.transmit_sequence(turbo_channel_vector)

            hadamard_decoded_vector = [int(b >= 0.0) for b in hadamard_channel_vector]
           # ext_hamming_decoded_vector = [int(b > 0.0) for b in ext_hamming_channel_vector]

            hadamard_decoded_vector = [int(c) for c in hadamard_decoder.decode_str_to_binary_vector("".join([str(a) for a in hadamard_decoded_vector]))]
            turbo_decoded_vector = turbo_decoder.decode_vector_for_tests(turbo_channel_vector)
            turbo_decoded_vector = [int(b > 0.0) for b in turbo_decoded_vector]
            turbo_decoder.reset()
            uncoded_channel_vector = [int(b > 0.0) for b in uncoded_channel_vector]

            hadamard_coded_error_count = sum([x^y for x,y in zip(input_vector,hadamard_decoded_vector)])
            turbo_coded_error_count = sum([x ^ y for x, y in zip(input_vector, turbo_decoded_vector)])
            uncoded_error_count = sum([x ^ y for x, y in zip(input_vector, uncoded_channel_vector)])

            turbo_coded_errors[n] = turbo_coded_errors[n] + turbo_coded_error_count
            hadamard_coded_errors[n]  = hadamard_coded_errors[n] + hadamard_coded_error_count
            uncoded_errors[n] = uncoded_errors[n] + uncoded_error_count

        print("Finished {} trials for SNR = {:8.2f} dB ...".format(num_trials, snr_range[n]))
    hadamard_ber_values = hadamard_coded_errors / (num_trials * block_size)
    turbo_coded_ber_values = turbo_coded_errors / (num_trials * block_size)
    uncoded_ber_values = uncoded_errors / (num_trials * block_size)

    def plot_data():
        plot.plot(snr_range, turbo_coded_ber_values, "r.-", label="Турбо код")
        plot.plot(snr_range, uncoded_ber_values, "b.-", label="Без код")
        plot.plot(snr_range, hadamard_ber_values, "g.-", label="Хадамардов код")

        plot.yscale("log")
        plot.title("Турбо код со рата на пренос 1/3, Информациски битови={}, Обиди={}".format(block_size, num_trials))
        plot.xlabel("SNR [dB]")
        plot.ylabel("Bit Error Rate (BER)")
        plot.grid(visible=True,which="major", linestyle="-")
        plot.grid(visible=True,which="minor", linestyle="--")
        plot.legend()
        plot.savefig("plot.ber.svg")
        plot.show()

    def plot_smooth_data():
        plot.figure(figsize=(10,10))
        xnew = np.linspace(*plot_params["snr"][:2], num=50)

        spl = make_interp_spline(snr_range, turbo_coded_ber_values)
        plot.plot(xnew, spl(xnew), "r.-", label="Турбо код")

        spl = make_interp_spline(snr_range, uncoded_ber_values)
        plot.plot(xnew, spl(xnew), "b.-", label="Без код")
        
        spl = make_interp_spline(snr_range, hadamard_ber_values)
        plot.plot(xnew, spl(xnew), "g.-", label="Хадамардов код")

        plot.yscale("log")
        plot.title("Турбо код со рата на пренос 1/3, Информациски битови={}, Обиди={}".format(block_size, num_trials))
        plot.xlabel("SNR [dB]")
        plot.ylabel("Bit Error Rate (BER)")
        plot.grid(visible=True,which="major", linestyle="-")
        plot.grid(visible=True,which="minor", linestyle="--")
        plot.legend()
        plot.savefig("plot.ber.smooth.svg")
        plot.show()

    plot_smooth_data()


if __name__ == '__main__':

    create_ber_plot({'block_size':7,'num_trials':100,'snr':[-3,10,20]})