# -*- coding: utf-8 -*-
"""
Created on Thu June 20 2024

@author: Ken Liu
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':


    raw = h5py.File(r'.\Test_pattern\Right_Right_0009_2024_01_03_17_15_18.h5', 'r')
    cubeRaw = np.transpose(raw['DS1'][:], (2, 1, 0, 3))

    # parameters

    sample_num = cubeRaw.shape[0]

    up_sample_num = int(sample_num *0.5)

    used_fft_num = int(up_sample_num*0.5)

    chirp_num = cubeRaw.shape[1]

    antenna_num = cubeRaw.shape[2]

    frame_num = cubeRaw.shape[3]

    # Phase Compensate parameters
    rf_config = dict(raw['RF_CONFIG'].attrs)
    RX1_image_compansate = raw['RF_CONFIG'].attrs.get('RX1_image_compansate')
    RX1_real_compansate = raw['RF_CONFIG'].attrs.get('RX1_real_compansate')

    # Main Code

    for idxFrame in range(frame_num):

        current_raw = cubeRaw[:up_sample_num,:,:,idxFrame] # dim 64*32*2

        current_raw_antenna0 = current_raw[:,:,0] # dim 64*32

        fast_fft_matrix_tmp = np.fft.fft(current_raw_antenna0,up_sample_num,axis=0) # Fast FFT, dim 64*32

        fast_fft_matrix_tmp = fast_fft_matrix_tmp * (RX1_real_compansate - 1j *RX1_image_compansate) / 1024 # phase compensate

        fast_fft_matrix = fast_fft_matrix_tmp[:used_fft_num, :] # only can used half Fast FFT value, dim 32*32

        rdi_map_complex = np.fft.fftshift(np.fft.fft(fast_fft_matrix,chirp_num,axis=1),axes=1) # Slow FFT, dim 32*32

        rdi_map = np.abs(rdi_map_complex) # Slow FFT take abs, dim 32*32

        # plot region
        plt.figure(1)
        plt.pcolormesh(rdi_map)
        plt.pause(0.05)






