import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def get_mag(FT_arr):
    """
    silly fxn, but nice symmetry with less trivial get_phase() function.
    """
    return np.abs(FT_arr)

def get_phase(FT_arr):
    """
    Gets the complex phases 
    """
    phase = np.arctan2(np.imag(FT_arr),np.real(FT_arr))



    return phase
def mix_FT(mag_arr, phase_arr):
    """
    Performs the fourier transforms and then mixes the phases and magnitudes.
    Calls mix_FT_arr() and Returns a new complex array
    """

    return mix_FT_arr(np.fft.fft2(mag_arr),np.fft.fft2(phase_arr))

def mix_FT_arr(mag_arr, phase_arr):
    """
    Mixes two fourier transform arrays by taking the magnitude from one and
    the phase from the other. Returns a new complex array

    arrays must be the same shape.
    """
    mag = get_mag(mag_arr)
    phase = get_phase(phase_arr)

    return mag*np.exp(1j*phase)

def phase_intensity_plot(arr, cb=True):
    """
    inputs:
        arr: An array of complex numbers. This should be fftshifted already
        cb: Do you want to show a vertical colorbar. Default True
    outputs:
        A plot following kevin cowtan's convention
    """
    r = get_mag(arr)
    theta = get_phase(arr)
    norm = plt.Normalize()

    disp_arr = cm.hsv(norm(theta))
    disp_arr[:,:,-1] = r/np.max(r)
    fig, ax = plt.subplots(figsize=(10,10))
    if cb:#Relabel the colorbar without actually rescaling theta to be in [0,2pi]
        cax = ax.imshow(disp_arr,cmap='hsv')
        cbar = fig.colorbar(cax,ticks=np.linspace(0,1,5))
        cbar.ax.set_yticklabels([r"0",r"$\frac{\pi}{2}$",r"$\pi$",r"$\frac{3\pi}{2}$",r"$2\pi$"],fontsize=20)
    else:
        ax.imshow(disp_arr, cmap='hsv')
    plt.show()
