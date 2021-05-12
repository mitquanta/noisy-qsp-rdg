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
    Numerical integration for the success probability of a single-shot Helstrom measurement
    '''

    # Helstrom bound for no noise
    if std == 0:
        return 0.5 + 0.5 * np.sqrt(1 - np.cos(meansep)**2)

    # Optimal Helstrom angle
    alpha = np.pi/4 - meansep/2 

    # Numerically integrate the success probability
    def integrand(theta):
        return 0.5 * gaussianpdf(0, std)(theta) * np.cos(alpha+theta)**2 + 0.5 * gaussianpdf(meansep, std)(theta) * np.sin(alpha+theta)**2
    res = scipy.integrate.quad(integrand, -np.inf, np.inf)
    return res[0]

def classical_wrapper(x, y):
    '''
    Wrapper function for generating data
    '''
    res = classical_single_exact(x*np.pi, y*np.pi)
    return res

if __name__ == "__main__":
    name = "classical-exact"
    print("Starting " + name)
    data = generate_data(classical_wrapper, xmin=0.0, xmax=0.50001, dx = 0.001, dy = 0.001)
    np.savetxt(name + ".txt", data)
