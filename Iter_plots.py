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

from scipy.interpolate import make_interp_spline, BSpline

def create_iter_plot(plot_params):
    block_size = plot_params["block_size"]
    num_trials = plot_params["num_trials"]
    num_iters = plot_params["num_iters"]

    snr_range = np.linspace(*plot_params["snr"])

    interleaver = random.sample(range(0, block_size), block_size)
    turbo_coder = TurboCodeCoder(interleaver)

    turbo_coded_errors = { n: np.zeros(len(snr_range)) for n in num_iters }
    uncoded_errors = np.zeros(len(snr_range))

    input_vectors = [np.random.randint(2, size=block_size)
                     for i in range(num_trials)]

    for n in range(len(snr_range)):
        for input_vector in input_vectors:
            turbo_encoded_vector = turbo_coder.encode_bits(input_vector)

            channel = GaussianForTests(snr_range[n])

            turbo_channel_vector = list(map(float, turbo_encoded_vector))
            uncoded_vector = list(map(float, input_vector))

            turbo_channel_vector = channel.convert_to_symbols(
                turbo_channel_vector)
            uncoded_vector = channel.convert_to_symbols(uncoded_vector)

            uncoded_channel_vector = channel.transmit_sequence(uncoded_vector)
            turbo_channel_vector = channel.transmit_sequence(
                turbo_channel_vector)

            uncoded_channel_vector = [int(b > 0.0)
                                      for b in uncoded_channel_vector]
            uncoded_error_count = sum(
                [x ^ y for x, y in zip(input_vector, uncoded_channel_vector)])
            uncoded_errors[n] = uncoded_errors[n] + uncoded_error_count

            for n_iter in num_iters:
                turbo_decoder = TurboCodeDecoder(interleaver, n_iter)

                turbo_decoded_vector = turbo_decoder.decode_vector_for_tests(
                    turbo_channel_vector)

                turbo_decoded_vector = [int(b > 0.0)
                                        for b in turbo_decoded_vector]

                turbo_coded_error_count = sum(
                    [x ^ y for x, y in zip(input_vector, turbo_decoded_vector)])

                turbo_coded_errors[n_iter][n] = turbo_coded_errors[n_iter][n] + \
                    turbo_coded_error_count

        print("Finished {} trials for SNR = {:8.2f} dB ...".format(
            num_trials, snr_range[n]))
    
    turbo_coded_ber_values = {}
    for n_iter in num_iters:
        turbo_coded_ber_values[n_iter] = turbo_coded_errors[n_iter] / (num_trials * block_size)
    uncoded_ber_values = uncoded_errors / (num_trials * block_size)

    def plot_data():
        plot.figure(figsize=(10,10))
        for n,c in zip(num_iters, ('red', 'green', 'magenta', 'cyan', 'blue')): #rgmcy
            plot.plot(snr_range, turbo_coded_ber_values[n], ".-", color=c, label=f"Турбо код, {n} ит.")
        plot.plot(snr_range, uncoded_ber_values, ".-", color='yellow', label="Без код")

        plot.ylim(top=0.25)
        # plot.yscale("log")
        plot.title(
            "Турбо код со рата на пренос 1/3, Информациски битови={}, Обиди={}".format(block_size, num_trials))
        plot.xlabel("SNR [dB]")
        plot.ylabel("Bit Error Rate (BER)")
        plot.grid(visible=True, which="major", linestyle="-")
        plot.grid(visible=True, which="minor", linestyle="--")
        plot.legend()
        plot.savefig("plot.iter.svg")
        plot.show()

    def plot_smooth_data():
        xnew = np.linspace(*plot_params["snr"][:2], num=50)
        plot.figure(figsize=(10,10))
        for n,c in zip(num_iters, ('red', 'green', 'magenta', 'cyan', 'blue')): #rgmcy
            spl = make_interp_spline(snr_range, turbo_coded_ber_values[n])
            smooth = spl(xnew)
            plot.plot(xnew, smooth, ".-", color=c, label=f"Турбо код, {n} ит.")
        
        spl = make_interp_spline(snr_range, uncoded_ber_values)
        smooth = spl(xnew)
        plot.plot(xnew, smooth, ".-", color='yellow', label="Без код")

        plot.ylim(top=0.25)
        # plot.yscale("log")
        plot.title(
            "Турбо код со рата на пренос 1/3, Информациски битови={}, Обиди={}".format(block_size, num_trials))
        plot.xlabel("SNR [dB]")
        plot.ylabel("Bit Error Rate (BER)")
        plot.grid(visible=True, which="major", linestyle="-")
        plot.grid(visible=True, which="minor", linestyle="--")
        plot.legend()
        plot.savefig("plot.iter.smooth.svg")
        plot.show()

    plot_smooth_data()
    


if __name__ == '__main__':

    create_iter_plot({'block_size': 7, 'num_trials': 100,
                    'snr': [-5, 2, 20], 'num_iters': [1, 2, 4, 8, 16]})
