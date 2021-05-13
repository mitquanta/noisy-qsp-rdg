from plots import *
import scipy.integrate

def gaussianpdf(mean, std):
    '''
    Probability distribution function for a normal (Gaussian) distribution
    '''
    def pdf(x):
        return np.exp(-0.5*(x-mean)**2/std**2) / (std*np.sqrt(2*np.pi))
    return pdf

def classical_single_exact(meansep, std):
    '''
    Returns the exact success probability of single shot Helstrom strategy from analytic integration
    '''
    alpha = np.pi/4 - meansep/2
    return 0.25 * np.exp(-2 * std**2) * (2 * np.exp(2 * std**2) + np.cos(2 * alpha) - np.cos(2 * (alpha + meansep)))

def classical_wrapper(x, y):
    '''
    Wrapper function for generating data
    '''
    res = classical_single_exact(x*np.pi, y*np.pi)
    return res

if __name__ == "__main__":
    name = "data/classical-exact"
    print("Starting " + name)
    data = generate_data(classical_wrapper, xmin=0.0, xmax=0.50001, dx = 0.001, dy = 0.001)
    np.savetxt(name + ".txt", data)
