# -*- coding: utf-8 -*-
"""
    cardiowheel.hrv
    ---------------

    This module provides various methods to perform
    Heart Rate Variability (HRV) analysis.

    :copyright: (c) 2016 by CardioID Technologies Lda.
    :license: All rights reserved.
"""

# Imports
# built-in

# 3rd party
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ss
from scipy import interpolate
from sklearn import metrics
from sklearn.metrics import mean_squared_error
import math
from math import acos, hypot

# local

# Globals


def rr_resample(ts, RR, sampling_rate=4.0):
    """Resample a sequence of RR intervals into an evenly sampled signal.
    
    Uses cubic spline interpolation.
    
    Parameters
    ----------
    ts : array
        Input time reference.
    RR : array
        Input RR signal.
    sampling_rate : int, float, optional
        Sampling frequency of resampled signal.
    
    Returns
    -------
    ts_r : array
        Resampled time reference.
    RR_r : array
        Resampled RR signal.
    
    """
    
#    # interpolate
#    cs = interpolate.interp1d(ts, RR, kind='linear')
#    # resample
    dt = 1. / float(sampling_rate)
    ts_r = np.arange(ts[0], ts[-1], dt)
#    RR_r = cs(ts_r)
    
    RR_r=np.array([]);
    for i in range(0,len(ts_r)-1):
        
        if any(ts==ts_r[i]):
            pos=np.where(ts==ts_r[i]);
            RR_r=np.append(RR_r,RR[pos]);
        else:
            x0=ts[ts<ts_r[i]];
            if len(ts)>1: 
                x0=x0[-1];
            x1=ts[ts>ts_r[i]];
            if len(x1)>1: 
                x1=x1[0];

            pos=np.where(ts==x0);
            y0=RR[pos];
            pos=np.where(ts==x1);
            y1=RR[pos];
            RR_r=np.append(RR_r,y0+(y1-y0)*(ts_r[i]-x0)/(x1-x0));
    
    
    return ts_r, RR_r 


def time_features(RR, nbins=512, pNN_max=1.0):
    """Compute time-domain HRV features.
    
    Parameters
    ----------
    RR : array
        Input RR signal.
    nbins : int, optional
        Number of bins to use in pNNx histogram.
    pNN_max : float, optional
        Maximum range for the pNNx histogram.
    
    Returns
    -------
    HR : array
        Instantaneous heart rate.
    RMSSD : float
        Root mean square of successive RR differences.
    mNN : float
        Average RR.
    sdNN : float
        RR standard deviation.
    mHR : float
        Average HR.
    sdHR : float
        HR standard deviation.
    bins : array
        pNNx histogram bins.
    pNNx : array
        Histogram of successive RR diferences.
    pNN50 : float
        Fraction of consecutive RR intervals that differ by more than 50 ms.
    
    """
    
    HR = 60. / RR
    
    dRR = np.diff(RR)
    RMSSD = np.sqrt(np.mean(dRR**2))
    
    sdNN = np.std(RR, ddof=1)
    mNN = np.mean(RR)
    
    sdHR = np.std(HR, ddof=1)
    mHR = np.mean(HR)
    
    adRR = np.abs(dRR)
    A = float(len(dRR))
    pNNx, bins = np.histogram(adRR, bins=nbins, range=(0, pNN_max),
                              density=False)
    pNNx = pNNx / A
    pNN50 = np.sum(adRR > 0.05) / A
    
    return HR, RMSSD, mNN, sdNN, mHR, sdHR, bins, pNNx, pNN50


def plot_pNNx(bins, pNNx):
    """Plot the pNNx histogram.
    
    Parameters
    ----------
    bins : array
        pNNx histogram bins.
    pNNx : array
        Histogram of successive RR diferences.
    
    """
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # get the corners of the rectangles for the histogram
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + pNNx
    
    # we need a (numrects x numsides x 2) numpy array for the path helper
    # function to build a compound path
    XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T
    
    # get the Path object
    barpath = path.Path.make_compound_path_from_polys(XY)
    
    # make a patch out of it
    patch = patches.PathPatch(barpath, facecolor='blue', edgecolor='gray',
                              alpha=0.8)
    ax.add_patch(patch)
    
    # update the view limits
    ax.set_xlim(left[0], right[-1])
    ax.set_ylim(bottom.min(), top.max())
    
    ax.grid()
    plt.show()


def frequency_features(ts, RR, sampling_rate=4.0):
    """Compute frequency-domain HRV features.
    
    Parameters
    ----------
    ts : array
        Input time reference.
    RR : array
        Input RR signal.
    sampling_rate : int, float, optional
        Sampling frequency for resampled signal.
    
    Returns
    -------
    its : array
        Interpolated RR time reference.
    iRR : array
        Interpolated instantaneous RR intervals.
    iHR : array
        Interpolated instantaneous heart rate.
    VLF : float
        Very low frequency band power [0.003, 0.04) Hz.
    LF : float
        Low frquency band power [0.04, 0.15) Hz.
    HF : float
        High frequency band power [0.15, 0.4) Hz.
    TF : float
        Total power in the VLF, LF, and HF bands.
    L2HF : float
        Ratio of LF to HF power.
    nuLF : float
        LF power in normalized units.
    nuHF : float
        HF power in normalized units.
    
    """
    
    # resample
    its, iRR = rr_resample(ts, RR, sampling_rate=sampling_rate)
    iHR = 60. / iRR
    
    size = int(5 * sampling_rate)
    f, pwr = ss.welch(iRR, sampling_rate, window='hann', nperseg=size,
                      noverlap=size/2, nfft=1024, scaling='density')
    
#    pwr=np.array([0.000571416427730006,0.00114431201225227,0.00114874359721569,0.00115610997976011,0.00116638186093932,0.00117951840105712,0.00119546739741791,0.00121416551133063,0.00123553854322803,0.00125950175452420,0.00128596023460115,0.00131480931109259,0.00134593500142033,0.00137921450333813,0.00141451672204910,0.00145170283128822,0.00149062686560122,0.00153113634090657,0.00157307290029828,0.00161627298193614,0.00166056850577512,0.00170578757580960,0.00175175519444964,0.00179829398560676,0.00184522492304531,0.00189236806055298,0.00193954326049959,0.00198657091738737,0.00203327267304779,0.00207947212020958,0.00212499549124895,0.00216967232903562,0.00221333613690715,0.00225582500493686,0.00229698220980826,0.00233665678576894,0.00237470406430915,0.00241098618039355,0.00244537254326714,0.00247774027005803,0.00250797458060817,0.00253596915217807,0.00256162643289064,0.00258485791300253,0.00260558435331601,0.00262373597027057,0.00263925257747842,0.00265208368369184,0.00266218854741091,0.00266953618855631,0.00267410535784287,0.00267588446469389,0.00267487146473292,0.00267107370807773,0.00266450774983981,0.00265519912440042,0.00264318208519130,0.00262849931185242,0.00261120158677154,0.00259134744312894,0.00256900278667590,0.00254424049356682,0.00251713998664117,0.00248778679261435,0.00245627208268369,0.00242269219908901,0.00238714817018551,0.00234974521659122,0.00231059225096034,0.00226980137391093,0.00222748736859729,0.00218376719636774,0.00213875949588571,0.00209258408801790,0.00204536148870805,0.00199721243195893,0.00194825740494063,0.00189861619712859,0.00184840746525398,0.00179774831571966,0.00174675390600095,0.00169553706641022,0.00164420794346070,0.00159287366591776,0.00154163803447659,0.00149060123585458,0.00143985958193556,0.00138950527445304,0.00133962619554981,0.00129030572440515,0.00124162257997676,0.00119365068976484,0.00114645908437041,0.00110011181749011,0.00105466791086556,0.00101018132358775,0.000966700945046624,0.000924270610712736,0.000882929139842901,0.000842710394114710,0.000803643356116596,0.000765752226550324,0.000729056538942222,0.000693571290607657,0.000659307088570622,0.000626270309106653,0.000594463269552568,0.000563884411010548,0.000534528490566884,0.000506386781646610,0.000479447281134567,0.000453694921910198,0.000429111789467725,0.000405677341324670,0.000383368627959377,0.000362160514062203,0.000342025898934402,0.000322935934923316,0.000304860242841537,0.000287767123380763,0.000271623763597552,0.000256396437617651,0.000242050700777211,0.000228551576492819,0.000215863735226976,0.000203951664991185,0.000192779832904440,0.000182312837400347,0.000172515550750627,0.000163353251646172,0.000154791747648463,0.000146797487393795,0.000139337662499907,0.000132380299189016,0.000125894339702500,0.000119849713640431,0.000114217399413405,0.000108969476044633,0.000104079165606713,9.95208666198623e-05,9.52701787765039e-05,9.13039193909408e-05,8.76001320023089e-05,8.41380875841760e-05,8.08982788349776e-05,7.78624080400827e-05,7.50133690087072e-05,7.23352235972665e-05,6.98131733352225e-05,6.74335266701904e-05,6.51836623461948e-05,6.30519894227189e-05,6.10279044327798e-05,5.91017461659062e-05,5.72647485468483e-05,5.55089920633423e-05,5.38273541765503e-05,5.22134591261528e-05,5.06616275187489e-05,4.91668260634804e-05,4.77246177928940e-05,4.63311130802543e-05,4.49829217370642e-05,4.36771064466829e-05,4.24111377618855e-05,4.11828508662126e-05,3.99904042712185e-05,3.88322405944456e-05,3.77070495363133e-05,3.66137331482858e-05,3.55513734598286e-05,3.45192025079154e-05,3.35165747903357e-05,3.25429421428795e-05,3.15978310207290e-05,3.06808221461526e-05,2.97915324679142e-05,2.89295993627420e-05,2.80946669957538e-05,2.72863747449368e-05,2.65043475846146e-05,2.57481883142956e-05,2.50174715123420e-05,2.43117390885096e-05,2.36304973054998e-05,2.29732151372118e-05,2.23393238302819e-05,2.17282175356893e-05,2.11392548786025e-05,2.05717613371419e-05,2.00250323042551e-05,1.94983367113355e-05,1.89909210974654e-05,1.85020140141267e-05,1.80308306617942e-05,1.75765776619031e-05,1.71384578751682e-05,1.67156751850198e-05,1.63074391729272e-05,1.59129696204996e-05,1.55315007814115e-05,1.51622853743038e-05,1.48045982557913e-05,1.44577397404895e-05,1.41210385424960e-05,1.37938543199584e-05,1.34755798112003e-05,1.31656425572829e-05,1.28635062118517e-05,1.25686714445934e-05,1.22806764496048e-05,1.19990970744215e-05,1.17235465893726e-05,1.14536751203000e-05,1.11891687705169e-05,1.09297484601863e-05,1.06751685130826e-05,1.04252150219821e-05,1.01797040247251e-05,9.93847952333225e-06,9.70141137846972e-06,9.46839311106482e-06,9.23933964202169e-06,9.01418499979748e-06,8.79288002411972e-06,8.57539009238657e-06,8.36169289333464e-06,8.15177627042039e-06,7.94563615507890e-06,7.74327460763612e-06,7.54469798119031e-06,7.34991522128427e-06,7.15893631169008e-06,6.97177087415694e-06,6.78842692755651e-06,6.60890980952615e-06,6.43322126148210e-06,6.26135867577239e-06,6.09331450178192e-06,5.92907580600507e-06,5.76862397947595e-06,5.61193458450435e-06,5.45897733141271e-06,5.30971617490959e-06,5.16410951887202e-06,5.02211051764019e-06,4.88366746145024e-06,4.74872423334132e-06,4.61722082476140e-06,4.48909389715627e-06,4.36427737704563e-06,4.24270307245820e-06,4.12430129910040e-06,4.00900150525776e-06,3.89673288515878e-06,3.78742497135250e-06,3.68100819754968e-06,3.57741442433475e-06,3.47657742115865e-06,3.37843329905510e-06,3.28292088956931e-06,3.18998206643569e-06,3.09956200757579e-06,3.01160939599630e-06,2.92607655913901e-06,2.84291954715891e-06,2.76209815147363e-06,2.68357586572990e-06,2.60731979206183e-06,2.53330049616901e-06,2.46149181531114e-06,2.39187062380125e-06,2.32441656097630e-06,2.25911172693328e-06,2.19594035154068e-06,2.13488844237058e-06,2.07594341724900e-06,2.01909372709427e-06,1.96432847460962e-06,1.91163703422231e-06,1.86100867842271e-06,1.81243221535955e-06,1.76589564219829e-06,1.72138581835599e-06,1.67888816229483e-06,1.63838637509546e-06,1.59986219354787e-06,1.56329517499917e-06,1.52866251569122e-06,1.49593890381454e-06,1.46509640800367e-06,1.43610440151091e-06,1.40892952182481e-06,1.38353566505309e-06,1.35988401397114e-06,1.33793309825143e-06,1.31763888503980e-06,1.29895489773355e-06,1.28183236054814e-06,1.26622036623286e-06,1.25206606411490e-06,1.23931486551421e-06,1.22791066347940e-06,1.21779606374646e-06,1.20891262381585e-06,1.20120109707859e-06,1.19460167899451e-06,1.18905425243521e-06,1.18449862944570e-06,1.18087478684980e-06,1.17812309332167e-06,1.17618452576495e-06,1.17500087307856e-06,1.17451492564048e-06,1.17467064910289e-06,1.17541334136109e-06,1.17668977183021e-06,1.17844830243395e-06,1.18063898997550e-06,1.18321366981836e-06,1.18612602105158e-06,1.18933161354677e-06,1.19278793753003e-06,1.19645441649028e-06,1.20029240442216e-06,1.20426516855705e-06,1.20833785886762e-06,1.21247746573968e-06,1.21665276728865e-06,1.22083426785705e-06,1.22499412926476e-06,1.22910609639486e-06,1.23314541868637e-06,1.23708876907210e-06,1.24091416184600e-06,1.24460087087244e-06,1.24812934946015e-06,1.25148115311948e-06,1.25463886630437e-06,1.25758603411216e-06,1.26030709977803e-06,1.26278734865747e-06,1.26501285924380e-06,1.26697046161836e-06,1.26864770358279e-06,1.27003282457689e-06,1.27111473734353e-06,1.27188301716697e-06,1.27232789838325e-06,1.27244027774330e-06,1.27221172410186e-06,1.27163449381016e-06,1.27070155110731e-06,1.26940659273639e-06,1.26774407595610e-06,1.26570924907807e-06,1.26329818363358e-06,1.26050780726137e-06,1.25733593641056e-06,1.25378130796763e-06,1.24984360894550e-06,1.24552350341286e-06,1.24082265589367e-06,1.23574375052841e-06,1.23029050535933e-06,1.22446768118024e-06,1.21828108447584e-06,1.21173756406535e-06,1.20484500115818e-06,1.19761229262505e-06,1.19004932738380e-06,1.18216695589530e-06,1.17397695285850e-06,1.16549197328474e-06,1.15672550221817e-06,1.14769179845063e-06,1.13840583265489e-06,1.12888322042842e-06,1.11914015080043e-06,1.10919331080759e-06,1.09905980678688e-06,1.08875708306916e-06,1.07830283878139e-06,1.06771494348185e-06,1.05701135235869e-06,1.04621002171951e-06,1.03532882548810e-06,1.02438547340422e-06,1.01339743159442e-06,1.00238184614624e-06,9.91355470276113e-07,9.80334595633029e-07,9.69334988226734e-07,9.58371829411354e-07,9.47459662294258e-07,9.36612343875908e-07,9.25843003160892e-07,9.15164005413758e-07,9.04586922666720e-07,8.94122510520524e-07,8.83780691215655e-07,8.73570542889188e-07,8.63500294873820e-07,8.53577328840472e-07,8.43808185534891e-07,8.34198576812419e-07,8.24753402633936e-07,8.15476772650172e-07,8.06372031971513e-07,7.97441790696015e-07,7.88687956750002e-07,7.80111771582947e-07,7.71713848251649e-07,7.63494211427505e-07,7.55452338865089e-07,7.47587203879556e-07,7.39897318394747e-07,7.32380776142461e-07,7.25035295616077e-07,7.17858262407828e-07,7.10846770588297e-07,7.03997662818391e-07,6.97307568917833e-07,6.90772942649369e-07,6.84390096514116e-07,6.78155234389969e-07,6.72064481881622e-07,6.66113914286701e-07,6.60299582117506e-07,6.54617534151571e-07,6.49063838015997e-07,6.43634598340395e-07,6.38325972540585e-07,6.33134184319960e-07,6.28055534997405e-07,6.23086412789582e-07,6.18223300191326e-07,6.13462779610698e-07,6.08801537424930e-07,6.04236366630103e-07,5.99764168261039e-07,5.95381951758648e-07,5.91086834460038e-07,5.86876040382209e-07,5.82746898463421e-07,5.78696840417450e-07,5.74723398345345e-07,5.70824202237095e-07,5.66996977482187e-07,5.63239542493590e-07,5.59549806534639e-07,5.55925767822701e-07,5.52365511967910e-07,5.48867210789599e-07,5.45429121537957e-07,5.42049586533750e-07,5.38727033225098e-07,5.35459974647504e-07,5.32247010261448e-07,5.29086827131496e-07,5.25978201401578e-07,5.22920000013471e-07,5.19911182609202e-07,5.16950803553373e-07,5.14038014008120e-07,5.11172063991629e-07,5.08352304350798e-07,5.05578188579564e-07,5.02849274416641e-07,5.00165225159866e-07,4.97525810638706e-07,4.94930907791834e-07,4.92380500802826e-07,4.89874680753675e-07,4.87413644763133e-07,4.84997694584362e-07,4.82627234644182e-07,4.80302769513972e-07,4.78024900810031e-07,4.75794323528743e-07,4.73611821829095e-07,4.71478264281955e-07,4.69394598611794e-07,4.67361845962331e-07,4.65381094722654e-07,4.63453493954888e-07,4.61580246468155e-07,4.59762601586651e-07,4.58001847661955e-07,4.56299304381266e-07,4.54656314924215e-07,4.53074238021100e-07,4.51554439965101e-07,4.50098286630064e-07,4.48707135544083e-07,4.47382328067220e-07,4.46125181719515e-07,4.44936982702896e-07,4.43818978657836e-07,4.42772371692716e-07,4.41798311720738e-07,4.40897890136259e-07,4.40072133859217e-07,4.39321999773424e-07,4.38648369581468e-07,4.38052045096240e-07,4.37533743986422e-07,4.37094095990808e-07,4.36733639614039e-07,4.36452819314189e-07,4.36251983190733e-07,4.36131381179612e-07,2.18045581880237e-07])
    # VLF
    idx = np.logical_and(0.003 <= f, f < 0.04)
    x = f[idx]
    y = pwr[idx]
    VLF = metrics.auc(x, y)
    
    # LF
    idx = np.logical_and(0.04 <= f, f < 0.15)
    x = f[idx]
    y = pwr[idx]
    LF = metrics.auc(x, y)
    
    # HF
    idx = np.logical_and(0.15 <= f, f < 0.4)
    x = f[idx]
    y = pwr[idx]
    HF = metrics.auc(x, y)
    
    TF = VLF + LF + HF
    L2HF = LF / HF
    nuLF = LF / (TF - VLF)
    nuHF = HF / (TF - VLF)
    
    return its, iRR, iHR, VLF, LF, HF, TF, L2HF, nuLF, nuHF, f, pwr

def nonlinear_features(R, Fs):
    """Compute Heart Rate Variability (HRV) metrics
    from a sequence of R peak locations.
    
    Parameters
    ----------
    R : array
        R peak positions (samples).
    Fs :      int
        Sampling Frequency
    Returns
    -------
    SD1 : float
        Dispersion of the points (Standard Deviation) around the 45 degrees axis
    SD2 : float
        Dispersion of the points (Standard Deviation) around the 135 degrees axis  
    SD2SD1: float
        SD2/SD1 ratio
    eig1 : float
        First Eigen value of the Principal Component Analysis.
    eig2 : float
        Second Eigen value of the Principal Component Analysis.
    SD1pca : float
        Dispersion of the points (Standard Deviation) around the axis of the first principal component.
    SD2pca : float
        Dispersion of the points (Standard Deviation) around the axis of the second principal component.
    SD2SD1pca : float
        SD2pca/SD1pca ratio.
    mse_V : float
        Mean squared error between the 45 degrees rotation matrix and the principal directions matrix.
    error_SD1 : float
        Relative error between SD1 and SD1pca.
    error_SD2 : float
        Relative error between SD2 and SD2pca.
    error_SD2SD1 : float
        Relative error between SD2SD1 and SD2SD1pca.
    """
#    R = R * Fs
    
    Rn = np.diff(R)
    Rnn = Rn[1:]
    Rn = Rn[0:-1]
    
    Table = np.array([Rn, Rnn])
    V45 = np.array([[1/np.sqrt(2),-1/np.sqrt(2)],[1/np.sqrt(2),1/np.sqrt(2)]]);
    Table_ = np.matmul(V45, Table, out=None)
    SD1 = np.sqrt(np.var(Table_[0,:]))
    SD2 = np.sqrt(np.var(Table_[1,:]))
    SD2SD1 = SD2/SD1
    
    Rn0 = np.mean(Rn)
    Rnn0 = np.mean(Rnn)
    
    Table_cent = np.array([Rn-Rn0, Rnn-Rnn0])
    cov_matrix = np.matmul(Table_cent, Table_cent.T, out=None)/len(Rn)
    W,Vpca = np.linalg.eig(cov_matrix)
    
    if Vpca[0,0] < 0: 
        vpca0=math.asin(-Vpca[0,0])
        v450=math.asin(-V45[0,1])
    else:
        vpca0=math.acos(Vpca[0,0])
        v450=math.acos(V45[0,0])
               

    if W[0]<W[1]:
        eig1 = W[0]
        eig2 = W[1]
    else:
        eig1 = W[1]
        eig2 = W[0]

    Table_pca =  np.matmul(Vpca, Table, out=None)
    SD1pca = np.sqrt(np.var(Table_pca[0,:]))
    SD2pca = np.sqrt(np.var(Table_pca[1,:]))
    if SD1>SD2 and SD1pca>SD2pca: 
        pass
    else:
        if SD1<SD2 and SD1pca<SD2pca:
            pass
        else:
            aux=SD1pca
            SD1pca=SD2pca
            SD2pca=aux
            
    SD2SD1pca = SD2pca/SD1pca
    
    
#    mse_V = mean_squared_error(V45,Vpca)
    mse_V=vpca0-v450 ##############################CAMBIAR BIEN!!!
    error_SD1 = np.abs(SD1-SD1pca)/SD1
    error_SD2 = np.abs(SD2-SD2pca)/SD2
    error_SD2SD1 = np.abs(SD2SD1-SD2SD1pca)/SD2SD1

    alpha = np.array([])
    area = np.array([])
    for i in range(0,len(Rn)-3):
        aux = (Rn[i]*Rn[i+1]+Rn[i+1]*Rn[i+2])/(hypot(Rn[i],Rn[i+1])+hypot(Rn[i+1],Rn[i+2]))
        aux2 = 0.5*abs(Rn[i]*(Rn[i+2]-Rn[i+3])-Rn[i+1]*(Rn[i+1]-Rn[i+3])+Rn[i+2]*(Rn[i+1]-Rn[i+2]))
        alpha = np.append(alpha,acos(aux))
        area = np.append(area,aux2)
    alpha = np.mean(alpha)
    area = np.mean(area)
    
    return SD1, SD2, SD2SD1, eig1, eig2, SD1pca, SD2pca, SD2SD1pca, Vpca, mse_V, error_SD1, error_SD2, error_SD2SD1, alpha, area #incluir en outputs

def hrv(R, sampling_rate):
    """Compute Heart Rate Variability (HRV) metrics
    from a sequence of R peak locations.
    
    Parameters
    ----------
    R : array
        R peak positions (samples).
    sampling_rate : int, float
        Sampling rate (Hz).
    
    Returns
    -------
    ts : array
        RR time reference.
    RR : array
        Instantaneous RR intervals.
    HR : array
        Instantaneous heart rate.
    its : array
        Interpolated RR time reference.
    iRR : array
        Interpolated instantaneous RR intervals.
    iHR : array
        Interpolated instantaneous heart rate.
    f   : array
        Frequencies to represent spectrogram.
    pwr: array
        Power of the Welch spectrum.
    features : dict
        A dictionary containing the computed metrics:
        RMSSD : float
        Root mean square of successive RR differences.
        mNN : float
            Average RR.
        sdNN : float
            RR standard deviation.
        mHR : float
            Average HR.
        sdHR : float
            HR standard deviation.
        bins : array
            pNNx histogram bins.
        pNNx : array
            Histogram of successive RR diferences.
        pNN50 : float
            Fraction of consecutive RR intervals that differ by more than 50 ms.
        VLF : float
            Very low frequency band power [0.003, 0.04) Hz.
        LF : float
            Low frquency band power [0.04, 0.15) Hz.
        HF : float
            High frequency band power [0.15, 0.4) Hz.
        TF : float
            Total power in the VLF, LF, and HF bands.
        L2HF : float
            Ratio of LF to HF power.
        nuLF : float
            LF power in normalized units.
        nuHF : float
            HF power in normalized units.
    
    Raises
    ------
    ValueError
        If there are not ebough R peaks to perform computations.
    
    """
    
    # ensure array of floats
    R = np.array(R, dtype='float')
    
    if len(R) < 4:
        raise ValueError("Not enough R peaks to perform computations.")
    
    # ensure float
    Fs = float(sampling_rate)
    
    # convert samples to time units
    R /= Fs
    
    # compute RR and exclude values outside physiological limits (HR > 200 and HR < 40)
    RR = np.diff(R)
    ts = R[:-1] + RR / 2
    
    #remove hr out of physiological accepted values
    indy = np.nonzero(np.logical_and(RR >= 60./220, RR <= 60./40))
    ts = ts[indy]
    RR = RR[indy]
    
    hr = 60./RR
    
#    print hr
    # remove outliers
    index = 0
    removeIndex = []
    
    for i in range(0,len(RR)-1,1):
        if abs(hr[i+1]-hr[index]) > 40: # and abs(ts[i+1]-ts[index])<1500:
            if index == 0 and abs(hr[index]-np.mean(hr))>20:
                index = i+1
                
            removeIndex.append(i+1)
        else:
            index = i+1
       
    ts = np.delete(ts, np.array(removeIndex))
    RR = np.delete(RR, np.array(removeIndex))

    if len(RR)<5:
        HR, RMSSD, mNN, sdNN, mHR, sdHR, bins, pNNx, pNN50 = [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1]
        its, iRR, iHR, VLF, LF, HF, TF, L2HF, nuLF, nuHF, f, pwr = [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1]
        SD1, SD2, SD2SD1, eig1, eig2, SD1pca, SD2pca, SD2SD1pca, Vpca, mse_V, error_SD1, error_SD2, error_SD2SD1, alpha, area = [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1],[-1], [-1], [-1], [-1]
    else:
        # time domain
        aux = time_features(RR, nbins=512, pNN_max=1.0)
        HR, RMSSD, mNN, sdNN, mHR, sdHR, bins, pNNx, pNN50 = aux
        # frquency domain
        bux = frequency_features(ts, RR, sampling_rate=4.0)
        its, iRR, iHR, VLF, LF, HF, TF, L2HF, nuLF, nuHF, f, pwr = bux
        
        #nonlinear features (geometric features)
        cux = nonlinear_features(R, Fs)
        SD1, SD2, SD2SD1, eig1, eig2, SD1pca, SD2pca, SD2SD1pca, Vpca, mse_V, error_SD1, error_SD2, error_SD2SD1, alpha, area = cux
        
    
    features = {
        'VLF': VLF,
        'LF': LF,
        'HF': HF,
        'TF': TF,
        'L2HF': L2HF,
        'nuLF': nuLF,
        'nuHF': nuHF,
        'RMSSD': RMSSD,
        'sdNN': sdNN,
        'mNN': mNN,
        'sdHR': sdHR,
        'mHR': mHR,
        'bins': bins,
        'pNNx': pNNx,
        'pNN50': pNN50,
        'SD1': SD1,
        'SD2': SD2,
        'SD2SD1': SD2SD1,
        'eig1': eig1,
        'eig2': eig2,
        'SD1pca': SD1pca, 
        'SD2pca': SD2pca, 
        'SD2SD1pca': SD2SD1pca, 
        'mse_V': mse_V, 
        'error_SD1': error_SD1, 
        'error_SD2': error_SD2, 
        'error_SD2SD1': error_SD2SD1,
        'alpha':    alpha,
        'area': area
    }
    
    return ts, RR, HR, its, iRR, iHR, f, pwr, Vpca, features
R=np.array([691335,691568,691802,692020,692229,692437,692656,692897,693135,693380,693621,693859,694086,694300,694507,694716,694929,695153,695385,695619,695856,696091,696322,696535,696740,696941,697153,697395,697665,697927,698184,698432,698670,698901,699124,699340,699559,699778,699996,700202,700409,700625,700883,701153,701415,701659,701897,702129,702360,702595,702815,703039,703267,703499,703738,703960,704176,704398,704625,704864,705102,705327,705547,705772,706006,706237,706457,706673,706898,707130,707359,707579,707802,708025,708242,708449,708664,708884,709104,709312,709526,709743,709962,710176,710401,710636,710869,711092,711321,711547,711759,711968,712181,712400,712611,712820,713038,713251,713456,713655,713862,714067,714267,714465,714670,714876,715084,715285,715478,715675,715873,716072,716275,716476,716683,716890,717104,717323,717546,717757,717963,718168,718377,718595,718823,719053,719276,719500])
ts,RR,HR,its,iRR,iHR, f1, pwr1,Vpca1, features_aux = hrv(R,256)