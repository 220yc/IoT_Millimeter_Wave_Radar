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

        if idxFrame == 100:

            kk =1

        # RDI MAP

        current_raw = cubeRaw[:up_sample_num,:,:,idxFrame] * 2**15 # dim 64*32*2

        fast_fft_cube_tmp = np.fft.fft(current_raw,up_sample_num,axis=0) # Fast FFT, dim 64*32, get range value

        fast_fft_cube_tmp[:,:,0] = fast_fft_cube_tmp[:,:,0] * (RX1_real_compansate - 1j *RX1_image_compansate) / 1024 # phase compensate

        fast_fft_cube = fast_fft_cube_tmp[:used_fft_num, :,:] # only can used half Fast FFT value, dim 32*32, get velocity value

        rdi_map_complex = np.fft.fftshift(np.fft.fft(fast_fft_cube,chirp_num,axis=1),axes=1) # Slow FFT, dim 32*32

        rdi_map = np.abs(rdi_map_complex[:,:,0]) # Slow FFT take abs, dim 32*32

        # PHD MAP

        phd_map_tmp = rdi_map_complex[:,16,:]

        phd_map_complex = np.fft.fftshift(np.fft.fft(phd_map_tmp,32,axis=1),axes=1) # Angle FFT, dim 32*32

        phd_map = np.abs(phd_map_complex)


        # plot region
        plt.figure(1)
        plt.pcolormesh(rdi_map)
        plt.pause(0.05)

        plt.figure(2)
        plt.pcolormesh(phd_map)
        plt.pause(0.05)

        kkk = 1






