import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from cmocean.cm import phase as phase_cm

def get_mag(FT_arr):
    """
    silly fxn, but nice symmetry with less trivial get_phase() function.
    """
    return np.abs(FT_arr)

def get_phase(FT_arr):
    """
    Gets the complex phases
    """
    return np.angle(FT_arr)

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

def phase_intensity_plot(arr, ax=None, cb=True, min_alpha = 0, cmap = 'ocean'):
    """
    inputs:
        arr: An array of complex numbers. This should be fftshifted already
        ax: matplotlib axis object if you want the plot to happen in that
        cb: Do you want to show a vertical colorbar. Default True
        min_alpha: set to map the magnitudes on to alphas = [min_alpha,1]
        cmap: default is cmocean phase cm, otherwise the string will be used (hsv a good alternative)
    outputs:
        A plot following kevin cowtan's convention
    """

    r = get_mag(arr)
    theta = get_phase(arr)
    theta[theta<0]+=np.pi #correct for neg values of angle so no weird jumps going around 180 deg
    norm = plt.Normalize()

    disp_arr = phase_cm(norm(theta))
    disp_arr[:,:,-1] = r/np.max(r)
    disp_arr[:,:,-1] += (1-disp_arr[:,:,-1])*min_alpha
    if ax is None:
        fig, ax = plt.subplots(figsize=(10,10))
    elif ax is not None and cb:
        raise ValueError('if you pass an axis you can\'t have cb=True')
    if cmap == 'ocean':
        cmap = phase_cm
    # Relabel the colorbar without rescaling theta to be in [0,2pi]
    if cb:
        cax = ax.imshow(np.flipud(disp_arr),cmap=cmap)
        cbar = fig.colorbar(cax,ticks=np.linspace(0,1,5))
        labels = [ r"0", r"$\frac{\pi}{2}$", r"$\pi$",
                   r"$\frac{3\pi}{2}$", r"$2\pi$"]
        cbar.ax.set_yticklabels(labels, fontsize=20)
    else:
        ax.imshow(np.flipud(disp_arr), cmap=cmap)
    if ax is None:
	plt.show()


from scipy.stats import multivariate_normal

def gaussian_lattice(n_atoms,uc_size,n_tiles, means):
    """ Create a square lattice composed of unit cells each containg n_atoms gaussians of unit variance
        Lattice dimensions are (uc_size*n_tiles)x(uc_size*n_tiles)
        Means is an array of locations for the gaussians - each value must be less than uc_size
        Default variance is uc_size/10
        Output is an array containg the lattice"""
    uc = np.zeros((uc_size,uc_size))
    X,Y = np.meshgrid(np.arange(uc_size),np.arange(uc_size))
    pos = np.empty(X.shape + (2,))
    pos[:, :, 0] = X; pos[:, :, 1] = Y
    for i in range(n_atoms):
        mvn = multivariate_normal(mean=means[i],cov = uc_size/10.)
        uc = uc + mvn.pdf(pos)
    #return uc
    return np.tile(uc,(n_tiles,n_tiles))


#An example gaussian lattice with a unit cell containing 10 atoms in a ring
def rings():
    th = np.linspace(0,2*np.pi,11)
    circ_mu = np.array([[50+20*np.cos(t),50+20*np.sin(t)] for t in th[:-1]])
    return gaussian_lattice(10,100,20, circ_mu)
