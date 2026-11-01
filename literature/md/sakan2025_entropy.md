---
key: sakan2025_entropy
arxiv: '2511.08010'
title: Probing Supernovae through gravitational wave entropy
authors:
- Aknur Sakan
- Nurzhan Ussipov
- Ernazar Abdikamalov
- Almat Akhmetali
- Marat Zaidyn
- Alisher Zhunuskanov
- José A. Font
- Matthew C. Edwards
- Sultan Abylkairov
arxiv_version: 2511.08010v1
method: latex
fetched: '2026-11-01'
---

# Introduction

In 1916, Einstein’s theory of general relativity predicted the existence of gravitational waves, subtle distortions that ripple through the fabric of space-time. They are generated when massive objects accelerate asymmetrically. In 2015, LIGO made the first direct detection of these waves coming from a merger of two black holes . This opened a new window on the universe. Since then, gravitational-wave astronomy has become a key tool for exploring energetic cosmic events such as mergers of black holes and neutron stars . Core-collapse supernovae (CCSNe) are another promising source of GWs . Despite decades of study, the exact mechanism behind these explosions remains uncertain . Gravitational waves offer a new way to probe them, carrying information directly from their cores and revealing how massive stars die and compact objects are born .

Entropy, originally introduced in information theory, quantifies the degree of uncertainty, order, and predictability in a system. It has become a powerful tool for analyzing complex, non-linear, and non-stationary time series data . In gravitational-wave research, entropy-based measures have so far seen limited application, but recent studies have demonstrated their effectiveness for detection , classification , and for characterizing the complexity and organization of binary-merger signals .

Entropy could be particularly useful for CCSN gravitational waves, as these signals contain stochastic components arising from turbulent dynamics, superimposed on more coherent features associated with, for example, proto-neutron star oscillations . By evaluating entropy, one can detect pattern changes and random fluctuations within the signal. These features can then serve as informative inputs for machine-learning algorithms, improving the classification and physical interpretation of CCSN gravitational-wave signals.

In this study, we apply entropy to CCSN gravitational waves. As a first application, we focus on relatively simple signals: the so-called rotating bounce waveforms produced by rapidly rotating progenitors of different masses (more on them in Section <a href="#sec:astro_context" data-reference-type="ref" data-reference="sec:astro_context">2</a>). The objective is to classify the progenitor mass based on the waveform. These signals are known to be highly similar across masses, making them a challenging test case for machine-learning models . Applying entropy to this problem serves as an intermediate step to assess its utility in a controlled setting. Because rotating bounce signals lack stochastic components, they provide a clean benchmark. More realistic explosions exhibit strong stochasticity due to turbulence , which we leave for future work.

With this goal, we perform a systematic machine-learning analysis across multiple signal representations and entropy measures. The analysis is conducted in three domains: the time domain and two time-frequency representations obtained using the short-time Fourier transform and the continuous wavelet transform. We calculate four types of entropy for each representation: Shannon, exponential, Rényi, and Tsallis. We then identify the most informative characteristics using three feature-selection algorithms: Least Absolute Shrinkage and Selection Operator (LASSO), Recursive Feature Elimination with Cross-Validation (RFE-CV), and Relief-F. The selected features are subsequently used to train six machine-learning classifiers, including $k$-Nearest Neighbors ($k$-NN), Support Vector Machine (SVM), Random Forest (RF), Logistic Regression (LR), Naïve Bayes (NB), and Extreme Gradient Boosting (XGBoost). The results identify the most informative entropy features, effective feature-selection methods, and classifiers that achieve high accuracy across different signal-to-noise ratios (SNRs).

This paper is organized as follows. Section <a href="#sec:astro_context" data-reference-type="ref" data-reference="sec:astro_context">2</a> outlines the astrophysical context of core-collapse supernovae and their gravitational-wave emission. Section <a href="#sec:methods" data-reference-type="ref" data-reference="sec:methods">3</a> describes the computation of entropy features, the feature selection procedures, and the classification algorithms. Section <a href="#sec:results" data-reference-type="ref" data-reference="sec:results">4</a> presents the main results, and Section <a href="#sec:conclusions" data-reference-type="ref" data-reference="sec:conclusions">5</a> summarizes the key findings and conclusions.

# Astrophysical Context

For completeness, this section provides additional background on CCSNe and their GW emission. Readers primarily interested in the data analysis and entropy-based methods may skip it without loss of continuity.

Core-collapse supernovae mark the end of massive stars. When such a star exhausts its nuclear fuel, its core can no longer support itself against gravity, and it collapses inward. The collapse stops once matter reaches nuclear densities, creating a rebound that launches a shock wave. This shock quickly loses energy and stalls , but if it is revived, it drives a powerful explosion that tears the star apart . A successful explosion leaves a neutron star remnant, while failed or partially successful ones may form black holes, either directly or through fallback accretion .

During collapse, the newborn proto–neutron star emits an enormous number of neutrinos , and a small fraction of them are absorbed in the region behind the stalled shock . This heats the gas, drives turbulent motion, and helps push the shock outward . Additional turbulence can also come from large-scale instabilities such as the standing accretion shock instability  or from convective plumes originating in the outer stellar layers . This mechanism, known as the neutrino mechanism, is believed to power explosions in slowly or non-rotating stars, likely the dominant class among massive stars .

In rapidly rotating stars, the situation is very different. The forming neutron star gains substantial rotational kinetic energy, which magnetic fields can tap to power the explosion. This mechanism can drive powerful, magnetorotationally driven jet explosions . If the jet fails to penetrate the stellar envelope, it can still contribute to the explosion by depositing energy within the star . In moderately rotating stars, it is possible that both neutrino heating and magnetic fields contribute to the explosion dynamics .

Gravitational waves provide a unique means of probing the interior of core-collapse supernovae. Because they originate directly from the stellar core, they carry information about the physical conditions in that region . The GW emission mostly arises from oscillations of the proto-neutron star (PNS) . Emission from non-radial hydrodynamics instabilities can also contribute . Additional, lower-frequency components may result from anisotropic neutrino emission , asymmetric shock propagation , or jets . When the progenitor rotates rapidly, centrifugal forces distort the collapsing core, so that the proto neutron star formation is accompanied by a sharp gravitational-wave spike at bounce. . Rapid rotation can also trigger non-axisymmetric instabilities that produce long-lasting, nearly periodic GW signals .

Once detected, these signals can provide direct probe of the supernova dynamics . They may reveal the mass, radius, and rotation rate of the proto-neutron star . Comparing GW patterns across different explosion scenarios could help distinguish between neutrino-driven and magnetorotational supernovae . Constraining the properties of high-density nuclear matter is another key objective , as gravitational-wave observations can help discriminate among competing nuclear models .

The rich physics of CCSNe makes them interesting laboratories for studying stellar physics and astrophysics under extreme conditions . As current and upcoming GW detectors approach the sensitivity to capture these signals , developing robust methods to characterize and classify them becomes increasingly important. The next sections focus on such methods based on entropy-based representations of GW signals.

# Methods

This study adopts a probabilistic framework to analyze gravitational-wave signals through four main stages: signal transformation, entropy-based feature extraction, optimal feature selection, and machine learning classification. Each signal representation is converted into a probability distribution, enabling the computation of entropy values. These entropy measures characterize the complexity and structure of the signal. The extracted features are then used to train machine-learning models for classifying gravitational-wave signals from supernovae. The overall workflow of the proposed methodology is illustrated in Figure <a href="#fig:flowchart" data-reference-type="ref" data-reference="fig:flowchart">1</a>.

<figure id="fig:flowchart" data-latex-placement="h!">
<embed src="figures/flowchart2.pdf" style="width:100.0%" />
<figcaption>Flowchart outlining the main steps of the proposed methodology. The signal representation stage (Time series, STFT, CWT) is described in Section <a href="#sec:representations" data-reference-type="ref" data-reference="sec:representations">3.1</a>, the entropy feature extraction in Section <a href="#subsec:entropy" data-reference-type="ref" data-reference="subsec:entropy">3.2</a>, the feature selection methods (LASSO, Relief-F, RFE-CV) and the classification procedure in Section <a href="#subsec:fsandclass" data-reference-type="ref" data-reference="subsec:fsandclass">3.3</a>.</figcaption>
</figure>

## Signal Representation

Signals can be represented in the time, frequency and time-frequency domains. To capture how frequencies change over time, we employ two common time-frequency representations: the short-time Fourier transform (STFT), which uses fixed-size sliding windows, and the continuous wavelet transform (CWT), which uses scale-dependent sliding windows to achieve higher time resolution at high frequencies and higher frequency resolution at low frequencies. To quantify local variations in signal complexity, the signal is divided into segments, and a probability distribution is computed for each segment. Here, the segment length is set to $10\%$ of the total signal duration.

To characterize the statistical properties of the gravitational wave strain signal, we construct a probability distribution from the time-domain strain data of a single waveform. The strain values, which range from $h_{min}$ to $h_{max}$, are partitioned into discrete bins of width $\Delta h$. For each bin $k$, we count the number of data points $N_k$ whose strain values fall within that bin’s range. The probability distribution is then obtained by normalizing these counts: $$\begin{equation}
p_{k} = \frac{N_k}{\sum_{k} N_k},
\end{equation}$$ where $N_k$ is the number of data points in the $k$-th bin and $\sum_{k} N_k$ is the total number of data points in the waveform. This distribution characterizes the relative frequency with which different strain values occur throughout the gravitational wave signal.

The STFT decomposes a segment into localized frequency components by applying a window function . The STFT coefficients are given by $$\begin{equation}
X(f, t) = \sum_{n} x[n]\, g[n-t]\, e^{-j 2 \pi f n / M},
\end{equation}$$ where $g(\cdot)$ denotes the analysis window and $j$ is the imaginary unit. The STFT was computed using a Hann window of length 256 samples, with consecutive segments overlapping by 50%. The complex magnitudes are then normalized to form a probability distribution: $$\begin{equation}
p_{f,t} = \frac{|X(f,t)|}{\sum_{f}\sum_{t} |X(f,t)|}.
\end{equation}$$

The CWT provides simultaneous localization in both the time and frequency domains . For a segment, the CWT is defined as $$\begin{equation}
W_x(s, \tau) = \frac{1}{\sqrt{s}} \int_{-\infty}^{\infty} x(t)\, \psi^*\!\left(\frac{t - \tau}{s}\right) dt,
\end{equation}$$ where $\psi$ is the mother wavelet, $s$ denotes scale. The CWT was computed using the Mexican Hat wavelet with a frequency range of 50-2000 Hz.

The magnitudes are normalized to form a probability distribution: $$\begin{equation}
p_{s,\tau} = \frac{|W_x(s,\tau)|}{\sum_{s}\sum_{\tau} |W_x(s,\tau)|}.
\end{equation}$$ These normalized distributions all satisfy $\sum p = 1$, making them suitable for entropy-based measures of signal complexity.

## Entropy Feature Extraction

Entropy measures provide a quantitative description of the uncertainty or information content inherent in a probability distribution. In this study, several entropy-based metrics are used as features to characterize the statistical complexity of the signals.

Shannon entropy quantifies the average uncertainty in a probabilistic event  and is defined as follows: $$\begin{equation}
    H_{\text{Sh}} = -\sum_{i=1}^{M} p_i \log_2 p_i,
    \label{eq:Shannon_entropy}
\end{equation}$$ where $M$ is the number of bins.

Exponential entropy replaces the logarithmic dependence of Shannon entropy with an exponential mapping : $$\begin{equation}
    H_{\text{Exp}}(X) = \sum_{i=1}^{M} \left(1 - e^{-p_i}\right).
    \label{eq:Exponential_entropy}
\end{equation}$$ The main advantage of this method is that it emphases rare events. This form matches the implementation used in the analysis and increases monotonically with $p_i$.

Tsallis entropy introduces a real-valued entropic index $q$, which controls the degree of nonadditivity and sensitivity to correlations in the data . It is computed as : $$\begin{equation}
    H_q(X) = \frac{1 - \sum_{i=1}^{M} p_i^q}{q - 1}.
    \label{eq:Tsallis_entropy}
\end{equation}$$ When $q \to 1$, Tsallis entropy converges to the Shannon entropy.

Rényi entropy generalizes Shannon entropy through an order parameter $\alpha$, controlling how probabilities are weighted  . It is computed as follows : $$\begin{equation}
    H_\alpha^{(\text{R})}(X) = \frac{\log_2 \!\left(\sum_{i=1}^{M} p_i^\alpha \right)}{1 - \alpha}.
    \label{eq:Renyi_entropy}
\end{equation}$$ The base-2 logarithm ensures consistency with the Shannon definition. As $\alpha \to 1$, Rényi entropy approaches the normalized Shannon entropy.

## Feature Selection

Feature selection identifies the most informative variables while removing redundant or noisy ones, thus reducing overfitting, lowering computational cost, and improving model interpretability . In this work, we employ three representative algorithms: LASSO, RFE-CV, and the Relief-F algorithm. LASSO applies an $L_1$ regularization penalty to suppress irrelevant coefficients and produce sparse, interpretable models . RFE-CV iteratively eliminates the least relevant features while optimizing performance through cross-validation . Relief-F, a distance-based approach, evaluates features by their ability to distinguish neighboring samples from different classes, providing robustness against noise and missing data .

## Classification

After feature selection, we use six classical machine learning (ML) algorithms for classification. To ensure optimal and fair performance across models, each classifier is tuned using `GridSearchCV` with 5-fold cross-validation . In this procedure, the dataset is divided into five folds. For every combination of hyperparameters, the model is trained on four folds and validated on the remaining one. This process repeats until each fold has served as a validation set and the average classification accuracy across all folds is computed to evaluate model performance. The combination of hyperparameters that yields the highest average accuracy is selected as optimal.

To verify that the tuned models generalize well, the mean accuracy on the training folds is compared with that on validation folds. The absence of a significant performance gap indicates that the models are neither overfitting nor underfitting. The resulting optimal hyperparameters for each model are summarized in Table <a href="#Table:ML_grid" data-reference-type="ref" data-reference="Table:ML_grid">[Table:ML_grid]</a>, where the best configurations obtained through `GridSearchCV` are highlighted in bold.

After determining the optimal hyperparameters, the dataset is split into training and test sets with an 80:20 ratio. Model performance is evaluated based on accuracy, which quantifies the proportion of correctly predicted samples relative to the total number of predictions, defined as: $$\begin{equation}
\text{Accuracy} = \frac{\text{Number of Correct Predictions}}{\text{Total Number of Predictions}}.
\end{equation}$$ This evaluation ensures a fair and consistent comparison of all ML models under the same data and noise conditions.

<div class="table*">

<div class="adjustbox">

width=

<div class="tabular">

C5.5cm \| C5.3cm \| C5.7cm Random Forest & Support Vector Machines & Naïve Bayes\

|                                               |
|:----------------------------------------------|
| ’n_estimators’: \[50, 75, **100**, 125, 150\] |
| ’max_depth’: \[None, 10, 15, **20**\]         |
| ’min_samples_split’: \[**2**, 5, 10\]         |
| ’min_samples_leaf’: \[**1**, 2, 4\]           |

&

|                                           |
|:------------------------------------------|
| ’C’: \[0.1, 1, **10**\]                   |
| ’kernel’: \[’linear’, **’rbf’**, ’poly’\] |
| ’gamma’: \[**’scale’**, ’auto’\]          |
| ’degree’: \[**2**, 3, 4\]                 |

&

|                                                     |
|:----------------------------------------------------|
| ’var_smoothing’: \[$10^{-9}$, $10^{-8}$, $10^{-7}$, |
| , $10^{-5}$\]                                       |

\
Logistic Regression & $k$-Nearest Neighbors & eXtreme Gradient Boosting\

|                                                |
|:-----------------------------------------------|
| ’C’: \[0.01, 0.1, 1, 10, **100**\]             |
| ’penalty’: \[**’l1’**, ’l2’, ’none’\]          |
| ’solver’: \[’lbfgs’, ’liblinear’, **’saga’**\] |
| ’max_iter’: \[100, **200**, 300\]              |

&

|                                          |
|:-----------------------------------------|
| ’n_neighbors’: \[**3**, 5, 7, 9, 11\]    |
| ’weights’: \[’uniform’, **’distance’**\] |
| ’metric’: \[**’euclidean’**,             |
| ’manhattan’,                             |
| ’minkowski’\]                            |
| ’p’: \[**1**, 2\]                        |

&

|                                           |
|:------------------------------------------|
| ’n_estimators’: \[50, 100, **200**\]      |
| ’max_depth’: \[3, **5**, 7\]              |
| ’learning_rate’: \[0.01, 0.1, **0.2**\]   |
| ’subsample’: \[0.8, 0.9, **1.0**\]        |
| ’colsample_bytree’: \[0.8, 0.9, **1.0**\] |
| ’gamma’: \[**0**, 0.1, 0.2\]              |
| ’reg_alpha’: \[0, **0.01**, 0.1\]         |
| ’reg_lambda’: \[1, 0.1, **0.01**\]        |

\

</div>

</div>

<span id="Table:ML_grid" label="Table:ML_grid"></span>

</div>

## Dataset

The dataset was obtained from numerical simulations using the general relativistic `CoCoNuT` code for progenitor models with zero-age main sequence (ZAMS) masses of 12, 15, 27, and 40 Solar mass. The 12 $M_\odot$ and 40 $M_\odot$ progenitor models were developed by , the 15 $M_\odot$ model by , and the 27 $M_\odot$ model by . All progenitor models assume solar metallicity. For each progenitor mass, six equations of state (EOS): `SFHo`, `SFHx`, `GShenFSU2.1`, `HSDD2`, `LS220`, and `BHB`$\Lambda\Phi$, were selected from the catalog based on their consistency with current observational constraints. For each EOS, we simulated a number of rotational configurations, the number ranging from 52 to 56. We quantify the impact of rotation by the ratio $T/|W|$, where $T$ denotes rotational kinetic energy and $W$ denotes gravitational binding energy. The number of rotation configurations varies because some EOS models do not undergo core collapse within the given simulation time limit. We consider $T/|W|$ values ranging from 0.02 to 0.21. This yields 1332 unique gravitational waveforms in total. All waveform data have a sampling rate of 16384 Hz, which matches LIGO’s operational sampling rate. The upper limit for the simulated signals is imposed by code limitations in accurately modeling post-bounce dynamics beyond $\sim$<!-- -->6–8 ms after the bounce time ($t = 0$).

To qualify the noise level presented in the signal we use signal-to-noise ratio , the matched-filter SNR $\rho$ for a detected GW signal $h$ is defined under the assumption of a perfectly matched template, $$\begin{equation}
\rho = \sqrt{\int_0^{\infty}\frac{4\hat{h}^*(f)\hat{h}(f)}{S_n(f)}df},
\end{equation}$$ where $\hat{h}(f)$ is the Fourier transform of the template waveform and $S_n(f)$ is the one-sided noise spectral density. All SNR values are calculated assuming optimal orientation of both the detector and the source. In this work, we use the Advanced LIGO noise spectrum at its design sensitivity, specifically in the high-power, zero-detuning configuration. Figure <a href="#fig:data" data-reference-type="ref" data-reference="fig:data">2</a> shows example waveforms for `SFHo` EOS and $T/|W|=0.07$.

<figure id="fig:data" data-latex-placement="h!">
<embed src="figures/gw_signals.pdf" style="width:95.0%" />
<figcaption>Gravitational wave strain as a function of time. Left: clean signals generated for four different source masses. Right: example of a single signal for the <code>SFHo</code> EOS with <span class="math inline"><em>T</em>/|<em>W</em>| = 0.07</span> and a 40 <span class="math inline"><em>M</em><sub>⊙</sub></span> mass after the addition of noise corresponding to an SNR of 200.</figcaption>
</figure>

# Results

In this section, we evaluate how different representations, entropy types, feature selection algorithms, and classification methods affect accuracy. Our goal is to identify the optimal combination that most effectively distinguishes between different masses of GW sources. We start from a default model setup that combines the CWT representation, Rényi entropy with $\alpha = 2$, Relief-F feature selection, and an SVM classifier (see Table <a href="#tab:default_model" data-reference-type="ref" data-reference="tab:default_model">1</a>). We then vary each element in this setup to examine how it affects classification accuracy.

<div id="tab:default_model">

| **Parameter**         |      **Default choice**      |
|:----------------------|:----------------------------:|
| Signal representation |             CWT              |
| Entropy feature       | Rényi entropy ($\alpha = 2$) |
| Feature selection     |           Relief-F           |
| Classifier            |             SVM              |

Parameters of the default model configuration used for performance assessment.

</div>

<span id="tab:default_model" label="tab:default_model"></span>

## Dependence on representation

<figure id="fig:transforms" data-latex-placement="h!">
<embed src="figures/transforms.new.pdf" style="width:100.0%" />
<figcaption>Rényi entropy (<span class="math inline"><em>α</em> = 2</span>) as a function of SNR for CWT (a), STFT (b), and time series representations (c).</figcaption>
</figure>

<div id="entropy_results">

|  |  |  |  |
|:---|:--:|:--:|:--:|
| Shannon | $0.733 \pm 0.025$ | $0.391 \pm 0.026$ | $0.316 \pm 0.028$ |
| Exponential | $0.731 \pm 0.027$ | $0.410 \pm 0.026$ | $0.319 \pm 0.025$ |
| Rényi, $\alpha = 2$ | **$0.740 \pm 0.027$** | $0.410 \pm 0.027$ | $0.316 \pm 0.025$ |
| Tsallis, $q=1.5$ | $0.737 \pm 0.023$ | $0.400 \pm 0.028$ | $0.319 \pm 0.022$ |

Classification accuracy of the SVM (mean $\pm$ std) for different entropy measures obtained using various signal representations at $\mathrm{SNR} = 200$.

</div>

In this section, we evaluate which representation – time series, STFT, or CWT – provides the most informative characterization of GW signals. To this end, we compute entropy values and classification accuracies for all three representations using the default model configuration summarized in Table <a href="#tab:default_model" data-reference-type="ref" data-reference="tab:default_model">1</a>.

In Figure <a href="#fig:transforms" data-reference-type="ref" data-reference="fig:transforms">3</a>, the average Rényi entropy ($\alpha = 2$) as a function of SNR for the three signal representations: CWT, STFT, and time series. Among them, the CWT representation provides the clearest visual separation between different mass classes across the SNR range, suggesting that it preserves more discriminative information under varying noise levels. The time series representation shows moderate class distinction, while the STFT-based entropy exhibits no clear separation between masses. This is likely because the STFT uses a fixed time-frequency resolution, which limits its ability to capture the nonstationary and transient features characteristic of GW signals. In contrast, the CWT adapts its resolution across frequencies, retaining both low- and high-frequency components that vary with progenitor mass. Overall, the CWT representation shows the most stable and consistent entropy behavior, making it the most suitable representation for subsequent classification.

Note that the STFT-based entropy displays a characteristic peak at SNR of about 25. At lower values of SNR, entropy increases due to the stronger influence of noise on the spectral components. This behavior arises from the fixed time-frequency resolution of the STFT, which causes noise to be distributed uniformly within each analysis window, increasing uncertainty in the spectral energy distribution. As SNR increases, noise effects diminish, the signal structure becomes more pronounced, and entropy gradually decreases, reflecting a transition from a stochastic to a deterministic regime.

To complement these findings, Table <a href="#entropy_results" data-reference-type="ref" data-reference="entropy_results">2</a> reports the classification accuracies obtained using different entropy measures derived from CWT, STFT, and time series representations. The CWT consistently achieves the highest accuracy, exceeding $\sim 0.7$. In contrast, STFT and time series representations yield noticeably lower accuracies, remaining below $\sim 0.41$. These results confirm that entropy features computed from the CWT provide a more discriminative and informative representation for signal classification compared to STFT and time-domain forms.

## Dependence on entropy

We investigate how varying the type of entropy measure impacts classification accuracy. All remaining parameters are held at their default values (Table <a href="#tab:default_model" data-reference-type="ref" data-reference="tab:default_model">1</a>).

Figure <a href="#fig:CWT" data-reference-type="ref" data-reference="fig:CWT">4</a> shows the values of the four entropy measures as a function of SNR. In all cases, entropy decreases with increasing SNR, as the noise contribution diminishes and the signal structure becomes more ordered. Beyond a certain SNR threshold, further changes in entropy are mainly governed by the intrinsic randomness of the signal rather than external noise. Overall, different types of entropy measures yield qualitatively similarly results.

<figure id="fig:CWT" data-latex-placement="h!">
<embed src="figures/CWT.pdf" style="width:95.0%" />
<figcaption>Various types of entropy as a function of SNR estimated with CWT. (a) Shannon entropy; (b) Exponential entropy; (c) Rényi entropy; (d) Tsallis entropy.</figcaption>
</figure>

These results also shed light on the dependence of entropy measures on the source mass: higher-mass progenitors yield lower entropy values, indicating greater signal regularity. While all four entropy features distinguish most signal classes (12, 27, and 40 $M_\odot$) at high SNRs, partial overlap remains between the 12 $M_\odot$ and 15 $M_\odot$ cases due to their spectral similarity and smaller relative differences. This is true across all types of entropy measures.

In Table <a href="#entropy_results" data-reference-type="ref" data-reference="entropy_results">2</a>, we summarize the values of the classification accuracy for different types of entropy measures. Close inspection of these values support the trend noticed above: the choice of entropy type has only a minor impact on classification accuracy, with values ranging from $0.731 \pm 0.027$ to $0.740 \pm 0.037$. The highest accuracy is achieved using Rényi entropy with $\alpha = 2$.

In Figure <a href="#fig:q" data-reference-type="ref" data-reference="fig:q">5</a>, we show how the classification accuracy depends on the parameters $\alpha$ and $q$ of the Rényi and Tsallis entropies, respectively. For Rényi entropy, accuracy increases steadily with $\alpha$ up to a maximum at $\alpha = 2$, after which it gradually declines. A similar trend is observed for Tsallis entropy, which reaches its peak accuracy at $q = 1.5$.

<figure id="fig:q" data-latex-placement="h!">
<embed src="figures/qparam.pdf" style="width:90.0%" />
<figcaption>Dependence of accuracy on <span class="math inline"><em>α</em></span> and <span class="math inline"><em>q</em></span> parameters of Rényi and Tsallis entropy at <span class="math inline">SNR = 200</span>. The remaining parameters correspond to those of the optimal model configuration (Table <a href="#tab:default_model" data-reference-type="ref" data-reference="tab:default_model">1</a>). For <span class="math inline"><em>q</em> = 1</span> and <span class="math inline"><em>α</em> = 1</span>, both Rényi and Tsallis entropies reduce to the Shannon entropy, highlighted by the blue square.</figcaption>
</figure>

## Dependence on feature selection

In this section, we examine how different feature selection methods influence classification accuracy. All model parameters, except the feature selection methods, are kept at their default values (Table <a href="#tab:default_model" data-reference-type="ref" data-reference="tab:default_model">1</a>).

Table <a href="#tab:fs_results" data-reference-type="ref" data-reference="tab:fs_results">3</a> presents the results for various feature selection strategies. The overall performance without feature selection shows that applying LASSO and RFE-CV leads to only minor changes in accuracy, indicating that these methods neither substantially improve nor reduce the effectiveness of the entropy-based features.

In contrast, the Relief-F method led to a modest improvement, achieving the highest overall accuracy among all tested methods. This suggests that Relief-F can provide a slightly more refined and discriminative subset of entropy features, thereby improving the model’s ability to distinguish between different GW source classes

<div id="tab:fs_results">

| **Name of classifier** | **No FS** |  |  |  |
|:---|:--:|:--:|:--:|:--:|
| SVM | $0.740 \pm 0.027$ | $0.731 \pm 0.026$ | $0.736 \pm 0.028$ | **$0.774 \pm 0.025$** |
| $k$-NN | $0.639 \pm 0.026$ | $0.656 \pm 0.029$ | $0.632 \pm 0.025$ | $0.658 \pm 0.027$ |
| XGB | $0.595 \pm 0.026$ | $0.606 \pm 0.029$ | $0.594 \pm 0.028$ | $0.634 \pm 0.028$ |
| Random Forest | $0.604 \pm 0.030$ | $0.611 \pm 0.030$ | $0.591 \pm 0.028$ | $0.645 \pm 0.030$ |
| Naı̈ve Bayes | $0.365 \pm 0.032$ | $0.390 \pm 0.031$ | $0.399 \pm 0.028$ | $0.397 \pm 0.031$ |
| Logistic Regression | $0.411 \pm 0.025$ | $0.431 \pm 0.027$ | $0.437 \pm 0.027$ | $0.428 \pm 0.030$ |

Classification accuracy (mean $\pm$ std) of different classifiers for the original feature set and after applying various feature selection (FS) methods at $\mathrm{SNR} = 200$ using CWT and Rényi entropy with $\alpha = 2$.

</div>

## Dependence on classification algorithm

In this section, we examine how different classification models affect the classification accuracy. All model parameters, except the classification algorithms, are kept at their default values (Table <a href="#tab:default_model" data-reference-type="ref" data-reference="tab:default_model">1</a>).

As shown in Table <a href="#tab:fs_results" data-reference-type="ref" data-reference="tab:fs_results">3</a>, the SVM achieves the highest accuracy among all classifiers, reaching $77.4\%$ in the default configuration. This result highlights its effectiveness in handling entropy-based features and capturing complex, nonlinear relationships within the data. For additional results from STFT and time series, we refer readers to Tables <a href="#tab:stft_accuracy" data-reference-type="ref" data-reference="tab:stft_accuracy">4</a> and <a href="#tab:time series_accuracy" data-reference-type="ref" data-reference="tab:time series_accuracy">5</a> in Appendix <a href="#sec:appendix" data-reference-type="ref" data-reference="sec:appendix">6</a>.

## Optimal configuration

<figure id="fig:accuracy" data-latex-placement="h!">
<embed src="figures/accuracy.pdf" style="width:90.0%" />
<figcaption>Classification accuracy as a function of SNR for the optimal configuration (blue line), raw time series data (red line) and spectral entropy (green line).</figcaption>
</figure>

<figure id="conf" data-latex-placement="h!">
<embed src="figures/conf.pdf" style="width:80.0%" />
<figcaption>Confusion matrix for optimal model configuration for SNR=200. The parameters of the optimal model configuration is given in Table <a href="#tab:default_model" data-reference-type="ref" data-reference="tab:default_model">1</a>.</figcaption>
</figure>

The previous results indicate that the most effective configuration consists of the CWT as the signal representation (Figure <a href="#fig:transforms" data-reference-type="ref" data-reference="fig:transforms">3</a>, Table <a href="#entropy_results" data-reference-type="ref" data-reference="entropy_results">2</a>), Rényi entropy with parameter $\alpha = 2$ as the entropy feature (Table <a href="#entropy_results" data-reference-type="ref" data-reference="entropy_results">2</a>), Relief-F as the feature selection method (Table <a href="#tab:fs_results" data-reference-type="ref" data-reference="tab:fs_results">3</a>), and SVM as the classification algorithm (Table <a href="#tab:fs_results" data-reference-type="ref" data-reference="tab:fs_results">3</a>). This combination provides the highest classification accuracy and the most stable performance across varying SNR levels. Below, we analyze how this accuracy depends on SNR. In addition, we add a comparison with traditional classification approaches that rely on raw time-series data and spectral entropy. Spectral entropy, calculated from the Fourier power spectrum, is used here as a baseline since it is a widely adopted Shannon-based measure of signal complexity that reflects the degree of spectral disorder .

Figure <a href="#fig:accuracy" data-reference-type="ref" data-reference="fig:accuracy">6</a> shows the mean classification accuracy as a function of SNR for the optimal configuration identified in this work, compared with results from raw time-series data and spectral entropy. The proposed configuration consistently achieves higher accuracy across all SNR levels.

Figure <a href="#conf" data-reference-type="ref" data-reference="conf">7</a> shows the SVM confusion matrix for the optimal configuration at $\mathrm{SNR} = 200$. The results indicate strong classification performance across all four progenitor mass classes, with particularly high accuracy for the 40 and 27 $M_\odot$ models. Some overlap is observed between the 12 and 15 $M_\odot$ classes due to the similarity of their waveform morphologies.

# Conclusions

In this work, we studied entropy-based feature for classifying gravitational waves from core-collapse supernovae. We focus on rotating bounce signal for progenitors with four different masses and six equations of state. We compute entropy measures from time series, STFT, and CWT representations. To identify the most informative characteristics, three feature-selection algorithms, including LASSO, RFE-CV, and Relief-F were applied in combination with six machine-learning classifiers.

The results show that wavelet-based entropy features yield the highest classification accuracy, exceeding $\sim70\%$ for our gravitational-wave signals. In contrast, the accuracies obtained from the time-series and STFT representations remain below $\sim40\%$. This confirms that time–frequency representations encode richer discriminative information than purely temporal or spectral analyses. Different entropy measures produce comparable outcomes; however, among all tested measures, Rényi entropy with $\alpha=2$ derived from the CWT achieves the highest accuracy.

Feature selection also influences classification performance. While LASSO and RFECV provided only modest improvements, the Relief-F algorithm delivered the best overall result. Among classifies, the SVM yields the highest accuracy. Overall, the combination of CWT-based Rényi entropy and Relief-F feature selection yields the best performance with classification accuracy of $\sim 77 \%$.

These results suggest that entropy-based methods hold promise for studying gravitational-wave signals from core-collapse supernovae. Nevertheless, our study has several limitations. Our analysis focuses on rotating bounce signals, which are relatively easy to model and detect but likely rare in nature, and they lack stochastic components. In future work, we plan to extend the analysis to more realistic signals that include stochastic features arising from turbulent dynamics. In addition, the optimal method configuration identified here is based on waveforms from different progenitor masses, and its applicability to other tasks (e.g., measurement of rotation or equation-of-state) remains to be tested. We also assume an optimal source orientation, whereas real sources have random orientations. Finally, detector noise is modeled as simulated Gaussian noise, which represents a simplified approximation to realistic instrumental noise. These limitations will be systematically addressed in future studies.

# Additional results

This appendix provides supplementary classification results obtained using the STFT and time-series representations.

<div id="tab:stft_accuracy">

| **Name of classifier** | **No FS** | **LASSO FS** | **RFE-CV FS** | **Relief-F FS** |
|:---|:--:|:--:|:--:|:--:|
| SVM | $0.410 \pm 0.025$ | $0.404 \pm 0.027$ | $0.410 \pm 0.028$ | $0.438 \pm 0.026$ |
| $k$-NN | $0.356 \pm 0.027$ | $0.378 \pm 0.028$ | $0.358 \pm 0.027$ | $0.406 \pm 0.024$ |
| XGB | $0.397 \pm 0.030$ | $0.402 \pm 0.027$ | $0.384 \pm 0.027$ | $0.410 \pm 0.026$ |
| Random Forest | $0.389 \pm 0.027$ | $0.404 \pm 0.030$ | $0.390 \pm 0.027$ | $0.395 \pm 0.026$ |
| Naı̈ve Bayes | $0.355 \pm 0.026$ | $0.370 \pm 0.027$ | $0.380 \pm 0.030$ | $0.364 \pm 0.028$ |
| Logistic Regression | $0.352 \pm 0.026$ | $0.374 \pm 0.027$ | $0.395 \pm 0.030$ | $0.359 \pm 0.027$ |

Classification accuracy (mean $\pm$ std) of different classifiers for the original feature set and after applying various feature selection (FS) methods at $\mathrm{SNR} = 200$ using STFT transform.

</div>

<div id="tab:time series_accuracy">

| **Name of Classifiers** | **No FS** | **LASSO FS** | **RFE-CV FS** | **Relief-F FS** |
|:---|:--:|:--:|:--:|:--:|
| SVM | $0.313 \pm 0.025$ | $0.322 \pm 0.025$ | $0.331 \pm 0.025$ | $0.329 \pm 0.028$ |
| $k$-NN | $0.280 \pm 0.025$ | $0.279 \pm 0.023$ | $0.289 \pm 0.026$ | $0.297 \pm 0.028$ |
| XGB | $0.313 \pm 0.027$ | $0.318 \pm 0.027$ | $0.325 \pm 0.022$ | $0.324 \pm 0.026$ |
| Random Forest | $0.318 \pm 0.029$ | $0.332 \pm 0.026$ | $0.338 \pm 0.028$ | $0.330 \pm 0.028$ |
| Naı̈ve Bayes | $0.296 \pm 0.024$ | $0.308 \pm 0.023$ | $0.322 \pm 0.024$ | $0.308 \pm 0.026$ |
| Logistic Regression | $0.324 \pm 0.025$ | $0.348 \pm 0.026$ | $0.356 \pm 0.025$ | $0.332 \pm 0.026$ |

Classification accuracy (mean $\pm$ std) of different classifiers for the original feature set and after applying various feature selection (FS) methods at $\mathrm{SNR} = 200$ using time series.

</div>

<div class="adjustwidth">

-0cm

</div>
