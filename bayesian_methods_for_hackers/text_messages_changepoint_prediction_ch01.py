import matplotlib.pyplot as plt
import numpy as np
import pymc as pm


def main():

    count_data = np.loadtxt("txtdata.csv")
    n_count_data = len(count_data)

    alpha = 1.0 / count_data.mean()  # Recall count_data is the
                                   # variable that holds our txt counts
    lambda_1 = pm.Exponential("lambda_1", alpha)
    lambda_2 = pm.Exponential("lambda_2", alpha)

    tau = pm.DiscreteUniform("tau", lower=0, upper=n_count_data)

    @pm.deterministic
    def lambda_(tau=tau, lambda_1=lambda_1, lambda_2=lambda_2):
        out = np.zeros(n_count_data)
        out[:tau] = lambda_1  # lambda before tau is lambda1
        out[tau:] = lambda_2  # lambda after (and including) tau is lambda2
        return out

    observation = pm.Poisson("obs", lambda_, value=count_data, observed=True)

    model = pm.Model([observation, lambda_1, lambda_2, tau])

    # Mysterious code to be explained in Chapter 3.
    mcmc = pm.MCMC(model)
    mcmc.sample(40000, 10000, 1)

    lambda_1_samples = mcmc.trace('lambda_1')[:]
    lambda_2_samples = mcmc.trace('lambda_2')[:]
    tau_samples = mcmc.trace('tau')[:]

    # Predicted the number of text messages sent for each day in the series

    # tau_samples, lambda_1_samples, lambda_2_samples contain
    # N samples from the corresponding posterior distribution
    N = tau_samples.shape[0]
    expected_texts_per_day = np.zeros(n_count_data)
    for day in range(0, n_count_data):
        # ix is a bool index of all tau samples corresponding to
        # the switchpoint occurring prior to value of 'day'
        ix = day < tau_samples
        # Each posterior sample corresponds to a value for tau.
        # for each day, that value of tau indicates whether we're "before"
        # (in the lambda1 "regime") or
        #  "after" (in the lambda2 "regime") the switchpoint.
        # By taking the posterior sample of lambda1/2 accordingly, we can
        # average over all samples to get an expected value for lambda on that
        # day. As explained, the "message count" random variable is Poisson
        # distributed, and therefore lambda (the poisson parameter) is the
        # expected value of "message count".
        expected_texts_per_day[day] = (lambda_1_samples[ix].sum()
                                       + lambda_2_samples[~ix].sum()) / N


    plt.plot(range(n_count_data), expected_texts_per_day, lw=4, color="#E24A33",
             label="expected number of text-messages received")
    plt.xlim(0, n_count_data)
    plt.xlabel("Day")
    plt.ylabel("Expected # text-messages")
    plt.title("Expected number of text-messages received")
    plt.ylim(0, 60)
    plt.bar(np.arange(len(count_data)), count_data, color="#348ABD", alpha=0.65,
            label="observed texts per day")

    plt.legend(loc="upper left")

    plt.show()


if __name__ == '__main__':
    main()