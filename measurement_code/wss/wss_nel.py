import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
class WSS_NEL:
    def __init__(self, fc, f):

        if fc == 193300:
            file_path = 'NELAWG_Ch42.txt'

        print(file_path)

        raw_data = np.loadtxt(file_path, skiprows=8)

        #wavelength = raw_data[:,0]
        self.frequency = raw_data[:,1]
        self.frequency_target = f

        jm_a_amp = scipy.interpolate.interp1d(np.flipud(self.frequency),np.flipud(raw_data[:,2]) , kind='cubic', bounds_error=False, fill_value=raw_data[:,2][-1], assume_sorted=True)
        jm_a_amp = jm_a_amp(f)

        jm_b_amp = scipy.interpolate.interp1d(np.flipud(self.frequency),np.flipud(raw_data[:,3] ), kind='cubic', bounds_error=False, fill_value=raw_data[:,3][-1], assume_sorted=True)
        jm_b_amp = jm_b_amp(f)

        jm_c_amp = scipy.interpolate.interp1d(np.flipud(self.frequency),np.flipud(raw_data[:,4]) , kind='cubic', bounds_error=False, fill_value=raw_data[:,4][-1], assume_sorted=True)
        jm_c_amp = jm_c_amp(f)

        jm_d_amp = scipy.interpolate.interp1d(np.flipud(self.frequency),np.flipud(raw_data[:,5]) , kind='cubic', bounds_error=False, fill_value=raw_data[:,5][-1], assume_sorted=True)
        jm_d_amp = jm_d_amp(f)

        jm_a_phase = scipy.interpolate.interp1d(np.flipud(self.frequency),np.flipud(raw_data[:,6]) , kind='cubic', bounds_error=False, fill_value=raw_data[:,6][-1], assume_sorted=True)
        jm_a_phase = np.unwrap(jm_a_phase(f))

        jm_b_phase = scipy.interpolate.interp1d(np.flipud(self.frequency),np.flipud(raw_data[:,7]) , kind='cubic', bounds_error=False, fill_value=raw_data[:,7][-1], assume_sorted=True)
        jm_b_phase =  np.unwrap(jm_b_phase(f))

        jm_c_phase = scipy.interpolate.interp1d(np.flipud(self.frequency),np.flipud(raw_data[:,8]) , kind='cubic', bounds_error=False, fill_value=raw_data[:,8][-1], assume_sorted=True)
        jm_c_phase =  np.unwrap(jm_c_phase(f))

        jm_d_phase = scipy.interpolate.interp1d(np.flipud(self.frequency),np.flipud(raw_data[:,9] ), kind='cubic', bounds_error=False, fill_value=raw_data[:,9][-1], assume_sorted=True)
        jm_d_phase =  np.unwrap(jm_d_phase(f))

        # plt.figure()
        # plt.plot(f, jm_a_amp,f, jm_b_amp,f, jm_c_amp,f, jm_d_amp)
        # plt.figure()
        # plt.plot(f, jm_a_phase,f, jm_b_phase,f, jm_c_phase,f, jm_d_phase)
        # plt.show()

        jm_a = np.multiply(jm_a_amp, np.exp(1j * jm_a_phase))
        jm_b = np.multiply(jm_b_amp, np.exp(1j * jm_b_phase))
        jm_c = np.multiply(jm_c_amp, np.exp(1j * jm_c_phase))
        jm_d = np.multiply(jm_d_amp, np.exp(1j * jm_d_phase))

        self.jm = [[jm_a, jm_b],[jm_c, jm_d]]

    def get_jm(self):
        return self.jm

if __name__ == '__main__':
    L = 200
    fc = 193300.
    fs = 88
    f = np.linspace(-(L / 2. - 1), L / 2., endpoint=True, num=L) * fs / L

    WSS_NEL(fc, f)
