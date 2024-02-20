from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.compat import lzip
from IPython.display import display, HTML
import statsmodels as sm
import scipy.stats as stats
import statsmodels.stats.stattools as smt
import statsmodels.stats.diagnostic as smd
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd
import numpy as np
import pylab


class LinearDiagnostics():
    """
    Perform linear model diagnostics and statistical tests on given sample.

    For linear regression tasks. Given significance level as a parameter
    performs number of tests and plots several diagrams: \n
    * Descriptive statistics of model residuals \n
    * histogram of residuals \n
    * Kernel density plot of residuals \n
    * QQ plot of residuals \n
    * Jarque-Bera test for normality (residuals) \n
    * Shapiro-Wilk test for normality (residuals) \n
    * Anderson-Darling test for normality (residuals) \n
    * DAgostino and Pearsons normality test (residuals) - stats.normaltest \n
    * Durbin-Watson test for autocorrelation (residuals) \n
    * Predicted value vs residual scatter plot \n
    * Predicted value vs true value scatter plot \n
    * Breusch-Pagan test for homoscedasticity (residuals) \n
    * Variance Inflation Factor (VIF) table \n
    * Correlation matrix of independent variables

    Attributes
    ----------
    model: str
        Name of model used for diagnostics.
    data : str
        Data used for model goodness of fit.
    target : series
        Series of target variable value. Must have corresponding index value
        with data.
    alpha : int
        Probability of rejecting H0 when it is true. Parameter for statistical
        tests. Against significance level we find critical value for
        statistical test and compare it to statistic. Equal to
        significance_level parameter.
    predictions : pandas DataFrame
        DataFrame with predicted values of dependent variable.
    results_df : pandas DataFrame
        DataFrame with goodness of fit for each observation.

    Notes
    -------------------
    Prerequisites: \n
    models_list - dictionary {'model_name' : { 'model' : class instance, \n
                                    'variables' : model variables set alias}}\n
    scoring_dict - dictionary { 'variables' : [corresponding list of variables]} \n
    Required libraries: \n
    * from statsmodels.stats.outliers_influence import variance_inflation_factor \n
    * from statsmodels.compat import lzip \n
    * from IPython.display import display, HTML \n
    * import statsmodels as sm \n
    * import scipy.stats as stats \n
    * import statsmodels.stats.stattools as smt \n
    * import statsmodels.stats.diagnostic as smd \n
    * import matplotlib as plt \n
    * import seaborn as sn \n
    * import pandas as pd \n
    * import numpy as np \n
    * import pylab

    Methods
    -------
    __init__(self, model_in, data_in, target, scoring_dict, model_list, significance_level=0.05)
        Constructor method.
    _residual_stats(self)
        Print descriptive statistics of residuals.
    _res_hist(self)
        Display residuals histogram.
    _res_kde(self)
        Display residuals kernel density plot.
    _jb_normal_test(self)
        Perform Jarque-Bera test for normality of residuals.
    _sw_normal_test(self)
        Perform Shapiro-Wilk test for normality of residuals.
    _ad_normal_test(self)
        Perform Anderson-Darling test for normality of residuals.
    _normal_test(self)
        Perform D'Agostino normality test for residuals.
    _dw_autocorr_test(self)
        Perform Durbin-Watson test for autocorrelation of residuals.
    _homoskedasticity_plot(self)
        Display predicted values vs residuals plot.
    _bp_test_homoskedasticity(self)
        Perform Breusch-Pagan test for homoskedasticity.
    _vif(self)
        Display variance inflation factors (VIF).
    _corr_matrix(self)
        Display Pearson correlation matrix between variables.
    """

    def __init__(self, model_in, data_in, target, scoring_dict, model_list,
                 significance_level=0.05):
        """
        Constructor method.

        Constructor method creating LinearDiagnostics class object.

        Parameters
        ----------
        model_in : str
            Name of model stored in models_list dictionary
        data_in : str
            Dataset on which predictions will be made and residuals calculated.
            Must have variables required by the model present.
        target : str
            Series of target variable value. Must have corresponding index
            value with data_in.
        scoring_dict : str
            Stored dictionary with list of variables selected for scoring.
        model_list : str
            Stored dictionary with list of estimated models.
        significance_level : float, default = 0.05
            Probability of rejecting H0 when it is true. Parameter for
            statistical tests. Against significance level we find
            critical value for statistical test and compare it to statistic.
        """
        self.model = model_in
        self.data = data_in
        self.target = target
        self.alpha = significance_level
        # calculating residuals
        vars = model_list[self.model]['variables']
        self.prdct_set = data_in[scoring_dict[vars]]
        self.predictions = model_list[self.model]['model'].predict(self.prdct_set)
        self.results_df = pd.DataFrame()
        self.results_df['predicted'] = list(self.predictions)
        self.results_df['actual'] = list(self.target)
        self.results_df['residual'] = self.results_df['actual'] - self.results_df['predicted']
        self.results_df = self.results_df.sort_values(by='residual').reset_index(drop=True)
        self._residual_stats()
        self._res_hist()
        self._res_kde()
        self._res_qq()
        self._jb_normal_test()
        self._sw_normal_test()
        self._ad_normal_test()
        self._normal_test()
        self._dw_autocorr_test()
        self._homoskedasticity_plot()

        self._bp_test_homoskedasticity()
        self._vif()
        self._corr_matrix()

    def _residual_stats(self):
        """
        Calculate residual descriptive statistics on pointed dataset.

        Calculating summary statistics about residuals (true - predicted
        values)
        values of dependent variable.
        """
        print('*** Test data residuals statistics ***')
        display(HTML(self.results_df.describe().to_html()))

    def _res_hist(self):
        """
        Display residuals histogram.

        Displays histogram of residuals (true values - predicted values).
        """
        sn.histplot(data=self.results_df['residual'])
        pylab.title('Residuals histogram')
        plt.show()

    def _res_kde(self):
        """
        Display residuals kernel density plot.

        Displays kernel density plot of residuals (true values - predicted
        values).
        """
        sn.kdeplot(data=self.results_df['residual'])
        pylab.title('Test data residuals kernel density plot')
        plt.show()

    def _res_qq(self):
        """
        Display residuals qqplot.

        Display residuals (true values - predicted values) quantile-quantile 
        plot.
        """
        stats.probplot(self.results_df['residual'], dist="norm", plot=pylab)
        pylab.title('Residuals qq plot')
        plt.show()

    def _jb_normal_test(self):
        """
        Perform Jarque Bera test for normality of residuals.

        References
        ----------
        Source materials: \n
        1. Wiki <https://en.wikipedia.org/wiki/Jarque%E2%80%93Bera_test> \n
        """
        print('*** Jarque-Bera test for normality of residuals ***')
        name = ['Jarque-Bera', 'Chi^2 two-tail prob.', 'Skew', 'Kurtosis']
        jarqueBera_test = smt.jarque_bera(self.results_df['residual'])
        print(lzip(name, jarqueBera_test))
        if jarqueBera_test[1] > self.alpha:
            print('On', self.alpha, 'significance level we fail',
                  ' to reject H0 about normal distribution of residuals.')
        else:
            print('On', self.alpha, 'significance level we ',
                  'reject H0 about normal distribution of residuals.')
        print()

    def _sw_normal_test(self):
        """
        Perform Shapiro-Wilk test for normality of residuals.

        References
        ----------
        Source materials: \n
        1. Wiki <https://en.wikipedia.org/wiki/Shapiro%E2%80%93Wilk_test> \n
        """
    # 'Shapiro-Wilk test for normality'
        print('Shapiro-Wilk test for normality')
        print(stats.shapiro(self.results_df['residual']))
        if stats.shapiro(self.results_df['residual'])[1] > self.alpha:
            print('On', self.alpha, 'significance level we fail to reject H0',
                  ' that residuals come from a normal distribution.')
        else:
            print('On', self.alpha, 'significance level we reject H0 that ',
                  'residuals come from a normal distribution.')
        print()

    def _ad_normal_test(self):
        """
        Perform Anderson-Darling test for normality of residuals.

        References
        ----------
        Source materials: \n
        1. Wiki <https://en.wikipedia.org/wiki/Anderson%E2%80%93Darling_test> \n
        """
        # Anderson-Darling Test for normality
        # H0 : sample is drawn from a population that follows a
        # particular distribution.
        print('Anderson-Darling test for normality')
        self.result = stats.anderson(self.results_df['residual'], dist='norm')
        print('Statistic: %.3f' % self.result.statistic)
        for i in range(len(self.result.critical_values)):
            sl, cv = self.result.significance_level[i], self.result.critical_values[i]
            if self.result.statistic < self.result.critical_values[i]:
                print('Significance level - %.3f: %.3f (Critical '% (sl, cv),
                      'Value), fail to reject H0 that sample comes from ',
                      'normal distribution.')
            else:
                print('Significance level - %.3f: %.3f (Critical ' % (sl, cv),
                      'Value), rejecting H0 that sample comes from normal ',
                      'distribution.')
        print()

    def _normal_test(self):
        """
        Perform D'Agostino normality test.

        References
        ----------
        Source materials: \n
        1. Wiki <https://en.wikipedia.org/wiki/D%27Agostino%27s_K-squared_test> \n
        """
        # Normal test
        print('Normal test for normality')
        stat, p = stats.normaltest(self.results_df['residual'])
        print('Statistics=%.3f, p=%.3f' % (stat, p))
        # interpret
        if p > self.alpha:
            print('On', self.alpha, 'significance level we fail to reject H0,',
                  ' that residuals come from a normal distribution.')
        else:
            print('On', self.alpha, 'significance level we reject H0 that',
                  'residuals come from a normal distribution.')
        print()

    def _dw_autocorr_test(self):
        """
        Perform Durbin-Watson test for autocorrelation.

        References
        ----------
        Source materials: \n
        1. Wiki <https://en.wikipedia.org/wiki/Durbin%E2%80%93Watson_statistic> \n
        """
        print('*** Durbin-Watson residual autocorrelation test ***')
        durbin = sm.stats.stattools.durbin_watson(self.results_df['residual'])
        print('Statistic value -', durbin)
        if durbin > 2.5:
            print('Statistic indicates negative serial correlation between',
                  ' residuals.')
        elif durbin > 1.5:
            print('Statistic indicates no serial correlation between ',
                  'residuals.')
        else:
            print('Statistic indicates positive serial correlation ',
                  'between residuals.')
        print()

    def _homoskedasticity_plot(self):
        """
        Plot predicted values against residual errors.

        Investigate visually possible homoscedasticity.
        """
        print('*** Investigating homoscedasticity of residuals ***')
        # Plot the model's residuals against the predicted values of y
        plt.xlabel('Predicted value')
        plt.ylabel('Residual error')
        plt.title('Model predicted values against residuals')
        plt.scatter(self.results_df['predicted'], self.results_df['residual'])
        plt.show()
        plt.scatter(self.results_df['actual'], self.results_df['predicted'],
                    alpha=.35)
        plt.title("Plot of Regression Test Values, Predicted vs. Actual")
        plt.xlabel('True value')
        plt.ylabel('Predicted value')
        plt.plot([min(self.results_df['actual'].min(),
                  self.results_df['predicted'].min()),
                  max(self.results_df['actual'].max(),
                  self.results_df['predicted'].max())],
                 [min(self.results_df['actual'].min(),
                  self.results_df['predicted'].min()),
                  max(self.results_df['actual'].max(),
                  self.results_df['predicted'].max())], color='black')
        plt.show()

    def _bp_test_homoskedasticity(self):
        """
        Perform Breusch-Pagan test for homoskedasticity.

        References
        ----------
        Source materials: \n
        1. Wiki <https://en.wikipedia.org/wiki/Breusch%E2%80%93Pagan_test> \n
        """
        print('*** Breusch-Pagan homoscedasticity test***')
        name = ['Lagrange multiplier statistic', 'p-value',
                'f-value', 'f p-value']
        bpagan_test = smd.het_breuschpagan(self.results_df['residual'],
                                           self.prdct_set)
        print(lzip(name, bpagan_test))

        if bpagan_test[1] > self.alpha:
            print('On', self.alpha, 'significance level we fail to reject H0 ',
                  'about homoscedasticity of residuals.')
        else:
            print('On', self.alpha, 'significance level we reject H0 and ',
                  'assume heteroscedasticity of residuals.')
        print()
        # Either one can transform the variables to improve the model, or
        # use a robust regression method
        # that accounts for the heteroscedasticity.

    def _vif(self):
        """
        Display variance inflation factors (VIF).

        Calculate variance inflation factors in dataset to check for
        multicollinearity.

        References
        ----------
        Source materials: \n
        1. Wiki <https://en.wikipedia.org/wiki/Variance_inflation_factor> \n
        """
        # Multicollinearity check
        print('*** Investigating Multicollinearity ***')
        print('*** Variance Inflation Factor (VIF) table***')
        vif_data = pd.DataFrame()
        vif_data["feature"] = self.prdct_set.columns
        # calculating VIF for each feature
        vif_data["VIF"] = [variance_inflation_factor(self.prdct_set.values, i)
                           for i in range(len(self.prdct_set.columns))]
        display(HTML(vif_data.to_html()))
        if vif_data["VIF"].max() > 5:
            print('There is indication (VIF > 5) that multicollinearity is ',
                  'present in the data.')
        else:
            print('Based on VIF there seems that there are no significant ',
                  'correlations between independent variables.')
        print()

    def _corr_matrix(self):
        """
        Display Pearson correlation matrix between variables.

        Calculates and displays matrix of correlations between variables in
        dataset. Correlation metric - Pearson correlation.
        """
        print('*** Correlation Matrix ***')
        f, ax = plt.subplots(figsize=(40, 30))
        mat = round(self.prdct_set.corr('pearson'), 2)
        mask = np.triu(np.ones_like(mat, dtype=bool))
        cmap = sn.diverging_palette(230, 20, as_cmap=True)
        sn.heatmap(mat, mask=mask, cmap=cmap, vmax=1, center=0, annot=True,
                   square=True, linewidths=.5, cbar_kws={"shrink": .7})
        plt.show()
