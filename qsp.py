import numpy as np
import scipy.linalg
import scipy.optimize

# Pauli matrices

sI = np.eye(2)
sX = np.array([[0, 1], [1,0]])
sY = np.array([[0, (0-1j)], [(0+1j) ,0]])
sZ = np.array([[1, 0], [0, -1]])

# Bras and kets

b0 = np.array([[1, 0]]) # <+z| = <0|
b1 = np.array([[0, 1]]) # <-z| = <1|
bp = (b0+b1)/np.sqrt(2) # <+x| = <+|
bm = (b0-b1)/np.sqrt(2) # <-x| = <-|
k0 = b0.T # |+z> = |0>
k1 = b1.T # |-z> = |1>
kp = bp.T # |+x> = |+>
km = bm.T # |-x> = |->

def ket(theta, phi):
    '''Create a ket with standard angle parameters theta and phi'''
    return np.cos(theta) * k0 + np.exp((0+1j)*phi) * np.sin(theta) * k1

def bra(theta, phi):
    '''Create a ket with standard angle parameters theta and phi'''
    return ket(theta, phi).T

# Rotations

def Rx(theta):
    '''Create a rotation matrix about the x-axis with parameter theta (rotation by 2*theta)'''
    return scipy.linalg.expm((0+1j) * theta * sX)

def Rz(theta):
    '''Create a rotation matrix about the z-axis with parameter theta (rotation by 2*theta)'''
    return scipy.linalg.expm((0+1j) * theta * sZ)

def gaussian(mu, sigma):
    '''
    Probability distribution function for a normal (Gaussian) distribution

    Args:
        mu: Mean of the distribution
        sigma: Standard deviation of the distribution

    Returns:
        Function that computes the PDF
    '''
    return lambda : np.random.normal(mu, sigma)

def qsp_simul(meansep, std, n, angles, start = k0, end = b0, numTrials=100):
    '''
    Calculate the success probability of the QSP strategy via Monte Carlo simulation

    Args:
        meansep: Separation betweeen the means of the two distributions
        std: Standard deviation shared by the two distributions
        n: Length of QSP sequence
        angles: List or tuple of QSP phase angles
        start: Vector for the prepared starting state (default |0> ket)
        end: Vector for the prepared ending measuremnet state (default <0| bra)
        numTrials: Number of trials to simulate (default 100)

    Returns:
        Success probability of the QSP strategy
    '''
    assert(n == len(angles))
    total = 0.0

    # Initialize the distibutions
    distro0 = gaussian(0, std)
    distro1 = gaussian(meansep, std)

    # Run numTrials samples of distro0 and distro1
    for i in range(numTrials):
        # Compute probability of measuring 0 if distro0
        state = start
        for i in range(n):
            state = Rz(angles[i]) @ Rx(distro0()) @ state
        total += np.abs(end @ state)**2
        # Compute probability of measuring 1 if distro1
        state = start
        for i in range(n):
            state = Rz(angles[i]) @ Rx(distro1()) @ state
        total += 1 - np.abs(end @ state)**2

    return total/2.0/numTrials

def qsp_optimize(meansep, std, n, numTrials=100):
    '''
    Find an optimal set of angles for QSP-n at a given point

    Args:
        meansep: Separation betweeen the means of the two distributions
        std: Standard deviation shared by the two distributions
        n: QSP sequence length
        numTrials: Number of trials to simulate (default 100)

    Returns:
        Tuple with two elements
        0:  List of n+4 elements - First n are QSP angles,
            followed by 2 angle parameters for the starting state
            and 2 angle parameters for the ending state
        1:  Minimized error probability
    '''

    seed = np.random.randint(1e6)
    def qsp_func(angles):
        # A simulated instance of QSP with numTrials*n random samples from the distribution
        np.random.seed(seed)
        phis = angles[:n]
        start = ket(angles[n], angles[n+1])
        end = bra(angles[n+2], angles[n+3])
        error_prob = np.ravel(1-qsp_simul(meansep, std, n, phis, start, end, numTrials))
        return error_prob

    angles = np.array([np.random.random() for i in range(n+4)])
    result = scipy.optimize.minimize(qsp_func, angles)
    return (result.x, result.fun)
