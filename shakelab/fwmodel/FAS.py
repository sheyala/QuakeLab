# =============================================================================
#
# Place for Copyright and authors information
#
# =============================================================================
"""
First attempt at implementing the forward modelling for Fourier 
amplitude spectra for seismic traces, based on the formulas by
Edwards et al. (2008), Poggi et al. (2011) and Bora et al. (2015)
"""

import numpy as _np
import math
import matplotlib.pyplot as _plt

# =============================================================================
# Figure settings

FAS_LABELS = {'f': 'Frequency (Hz)',
              'd': 'Displacement FAS (m*s)',
              'v': 'Velocity FAS (m)',
              'a': 'Acceleration FAS (m/s)'}


# =============================================================================

def plot_spectrum(f, fas, key):
    """
    Plotting utility for Fourier amplitude spectra visualisation
    """

    _plt.figure(figsize=(8.0,5.0))
    _plt.grid('on')
    _plt.xscale('log')
    _plt.yscale('log')
    if(key=='a'):
        _plt.ylim(1e-08, 5)
        _plt.xlim(0.035, 56)
    _plt.xlabel(FAS_LABELS['f'])
    _plt.ylabel(FAS_LABELS[key])
    _plt.plot(f, fas, linestyle='--', color='green')
    _plt.show()


# =============================================================================

class Event_Params(object):
    """
    Seismic event characterized through its main parameters.

    :param float M0:
        The seismic moment, expressed in N*m

    :param float f_c:
        The corner frequency
    """

    def __init__(self, name, M0, f_c):
        self.name = name
        self.M0 = M0
        self.f_c = f_c

    def __len__(self):
        return len(self.recording)

# =============================================================================

class Site_Params(object):
    """
    Recording site characterized through its main parameters.

    :param float k:
        The constant site-related attenuation operator

    :param float a:
        The frequency-independent site correction factor
    """

    def __init__(self, id, k, a):
        self.id = id
        self.k = k
        self.a = a


# =============================================================================

class Path_Params(object):
    """
    Path soil characterized through its main parameters.

    :param float rho:
        The mean density around the origin, expressed in kg/m**3

    :param float beta:
        The mean S-wave velocity around the origin, expressed in m/s

    :param float Q0:
        The dimensionless quality factor
    """

    def __init__(self, rho, beta, Q0):
        self.rho = rho
        self.beta = beta
        self.Q0 = Q0


# =============================================================================

def fd_site_ampl(f):
    """
    Compute the frequency-dependent amplification at the site

    :param float f:
        The input frequency

    :return float FDSA:
        The frequency-dependent amplification at the site
    """

    fdsa = 1.0

    return fdsa


# =============================================================================

def pd_attenuation(f, r, path, site):
    """
    Compute path dependent attenuation contribution to Fourier 
    amplitude spectrum as a combination of the frequency-dependent
    amplification at the site and the exponential attenuation function

    :param float f:
        The input frequency

    :param float r:
        The hypocentral distance

    :param class path:
        The path-related parameters

    :param class site:
        The site-related parameters

    :return float pda:
        The total path-dependent attenuation function
    """

    t_star = (r / (path.Q0*path.beta)) + site.k
    t_star = 0.031

    pda = fd_site_ampl(f) * math.exp(-math.pi*f*t_star)

    return pda


# =============================================================================

def source_spectrum(f, event):
    """
    Compute the source spectrum shape using the Brune omega-square
    model

    :param float f:
        The input frequency

    :param class event:
        The event-related parameters

    :return float ss:
        The Brune source spectrum shape
    """

    ss = 1./(1. + (f/event.f_c)**2)

    return ss


# =============================================================================

def omega_zero(event, path):
    """
    Compute the long-period plateau value of the source spectrum at
    the source 

    :param class event:
        The event-related parameters

    :param class path:
        The path-related parameters

    :return float w0:
        The plateau value at the source
    """

    R0 = 1000.
    THETA = 0.55
    F = 2.
    CSI = 1./math.sqrt(2.)

    w0 = event.M0 * (THETA*F*CSI) / (4.*math.pi*path.rho*(path.beta**3)*R0) 

    return w0


# =============================================================================

def appar_geom_spreading(r):
    """
    Compute the apparent geometrical spreading piecewise function
    (from Poggi et al., 2011)

    :param float r:
        The hypocentral distance

    :return float ags:
        The apparent geometrical spreading
    """

    R0 = 1000.
    R1 = 70000.
    B1 = -1.14
    B2 = -0.5

    if(r <= R1):
        ags = (r/R0)**B1

    else:
        ags = (R1**B1) * ((r/R1)**B2)

    return ags

# =============================================================================

def signal_moment(r, event, path, site):
    """
    Compute the collective signal moment

    :param float r:
        The hypocentral distance

    :param class event:
        The event-related parameters

    :param class path:
        The path-related parameters

    :param class site:
        The site-related parameters

    :return float sm:
        The collective signal moment
    """

    sm = omega_zero(event, path) * site.a * appar_geom_spreading(r)

    return sm


# =============================================================================

def fourier_ampl_spectrum(f, r, event, path, site, comp):
    """
    Compute the Fourier amplitude spectrum for a given event and site

    :param float f:
        The input frequency

    :param float r:
        The hypocentral distance

    :param class event:
        The event-related parameters

    :param class path:
        The path-related parameters

    :param class site:
        The site-related parameters

    :param int comp:
        The component for which FAS will be calculated: 
            0 for displacement
            1 for velocity
            2 for acceleration

    :return float fas:
        The fourier amplitude spectrum value for given f and r
    """

    fas = (signal_moment(r, event, path, site) * source_spectrum(f, event) 
         * pd_attenuation(f, r, path, site))

    fas = fas * (2 * math.pi * f)**comp

    return fas



# create sample case with parameters for event, path and site 
# characterization taken from literature

ev_irp = Event_Params("Irpinia", 2.95e+19, 0.07)
path_irp = Path_Params(2800, 3500, 1059)
site_irp = Site_Params(347, 0.025, 1.)
r_irp = 30000.

ev_1 = Event_Params("N/A", 6.67e+17, 0.45)
path_1 = Path_Params(2800, 3500, 1059)
site_1 = Site_Params(174, 0.0243, 1.)
r_1 = 25000.

ev_2 = Event_Params("N/A", 2.286e+15, 1.88)
path_2 = Path_Params(2800, 3500, 1059)
site_2 = Site_Params(174, 1.18795, 1.)
r_2 = 24000.

freqs = _np.arange(0.04, 50.01, 0.01)
acc_spectrum = [0 for i in range(len(freqs))]
vel_spectrum = [0 for i in range(len(freqs))]
dis_spectrum = [0 for i in range(len(freqs))]

i = 0
for f in freqs:
    acc_spectrum[i] = fourier_ampl_spectrum(f, r_1, ev_1, path_1, site_1, 2)
    vel_spectrum[i] = fourier_ampl_spectrum(f, r_1, ev_1, path_1, site_1, 1)
    dis_spectrum[i] = fourier_ampl_spectrum(f, r_1, ev_1, path_1, site_1, 0)
    i += 1

plot_spectrum(freqs, _np.array(acc_spectrum), 'a')
plot_spectrum(freqs, _np.array(vel_spectrum), 'v')
plot_spectrum(freqs, _np.array(dis_spectrum), 'd')

