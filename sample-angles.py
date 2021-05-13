from qsp import *
from plots import generate_data

def qsp_wrapper(x, y):
    angles = angles_data.item().get((np.round(x, 3), np.round(y, 3)))[0]
    phis = angles[:n]
    start = ket(angles[n], angles[n+1])
    end = bra(angles[n+2], angles[n+3])
    prob = qsp_simul(x*np.pi, y*np.pi, n, phis, start, end, 10000)
    print(x, y, prob)
    return np.float_(prob)


if __name__ == "__main__":
    
    n = 3
    name = "data/qsp-%d" % n
    print("Starting " + name);

    # Optimize QSP angles using medium number of trials

    angles_data = {} 
    for x in np.arange(0, 0.5001, 0.001):
        for y in np.arange(0, 0.5001, 0.001):
            res = qsp_optimize(x*np.pi, y*np.pi, n, 100)
            print((x, y), res)
            angles_data[(np.round(x, 3), np.round(y, 3))] = res

        np.save("%s-angles.npy" % name, angles_data)

    # Calculate probabilities using larger number of trials

    prob_data = generate_data(qsp_wrapper, dx=0.001, dy=0.001)
    np.savetxt("%s-data.txt" % name, prob_data)
