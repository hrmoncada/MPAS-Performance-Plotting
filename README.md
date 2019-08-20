# MPAS-Performance-Plotting
This is a control version private repository for the development and sharing (public, no available) . 
The python code store in this repository read the outputs from MPAS testcase which were executed on differents HPC cluster. The outputs have information about the layer subroutine performance 

## Table of Contents
- [Layer performance evaluation](#Layer-performance-evaluation)
  * [Compile](#Compile)
  * [Layer subroutines](#Layer-subroutines)
  * [Data Layer](#Data-Layer)
- [HPC Cluster performance](#HPC-Cluster-performance)
  * [Compile](#Compile)
  * [Data HPC](#Data-HPC-Cluster)
<!-- 
    + [Sub-sub-heading](#sub-sub-heading-1)
-->
- [Rules](#Rules)

<!-- Comments -->

## Layer performance evaluation
<!-- This is an h1 heading -->
### Compile
```sh
$ python3 Layer_subroutine_performance.py  ' 5 '
```
#### Layer subroutines
The program search and extract subroutine performance time on a specific output folder 
```
perf_p??_gr_openmpi/ . 
```
The program search for specifc layer and select the subroutines that bellow to than layer.
and calculate the average for each variable using the information found on the following files 
```
log_p??_s1, log_p??_s2, log_p??_s3
```
The importan part on each **{log_p??_s?}** file is similar to
```
    timer_name                                            total       calls        min            max            avg      pct_tot   pct_par     par_eff
  1 total time                                        2983.49082         1     2983.47955     2983.49082     2983.48518   100.00       0.00       1.00
  2  initialize                                        303.51822         1      301.54159      303.51822      302.52991    10.17      10.17       1.00
  3   io_read                                          106.56784         2       13.50259       92.94399       52.98999     3.57      35.11       0.99
  4    analysis_bootstrap                                0.00018         1        0.00017        0.00018        0.00017     0.00       0.00       0.98
  5     init_read_globalStats                            0.00002         1        0.00002        0.00002        0.00002     0.00      10.83       0.94
  3   reset_io_alarms                                    0.00048         2        0.00002        0.00046        0.00024     0.00       0.00       0.99
  3   diagnostic solve                                   7.50943         1        7.36049        7.50943        7.43496     0.25       2.47       0.99
  4    equation of state                                 0.71458         3        0.18986        0.33163        0.23753     0.02       9.52       1.00
  3   gm bolus velocity                                 10.64420         1       10.20827       10.64420       10.42623     0.36       3.51       0.98
  3   reconstruct gm vecs                                1.74685         1        1.67487        1.74685        1.71086     0.06       0.58       0.98
  3   analysis_init                                      0.00026         1        0.00019        0.00026        0.00022     0.00       0.00       0.87
  4    init_globalStats                                  0.00009         1        0.00006        0.00009        0.00007     0.00      35.30       0.82
  2  analysis_compute_startup                            4.40939         1        2.42660        4.40939        3.41800     0.15       0.15       0.78
  3   compute_startup_globalStats                        3.92781         1        1.94505        3.92781        2.93643     0.13      89.08       0.75
  2  io_shortwave                                        0.00081        13        0.00004        0.00010        0.00006     0.00       0.00       0.97
  2  io_read                                             0.00095        12        0.00006        0.00009        0.00008     0.00       0.00       0.99
  2  reset_io_alarms                                     0.00953        48        0.00001        0.00043        0.00019     0.00       0.00       0.95
  2  land_ice_build_arrays                               0.00010        12        0.00001        0.00001        0.00001     0.00       0.00       0.98
  2  time integration                                 2642.96706        12      219.06570      220.74921      220.07646    88.59      88.59       1.00
  3   se timestep                                     2642.96525        12      219.06553      220.74906      220.07631    88.59     100.00       1.00
  4    se prep                                           9.44072        12        0.77686        0.78933        0.78348     0.32       0.36       1.00
  4    se loop                                        2073.49684        24       84.48328       87.95722       86.36108    69.50      78.45       1.00
  5     se halo diag obd                                 1.68543        24        0.00010        0.10821        0.03517     0.06       0.08       0.50
  5     se halo diag                                     0.08658        24        0.00336        0.00413        0.00359     0.00       0.00       1.00
  5     se bcl vel                                     292.89518        24       10.83714       13.52374       12.20395     9.82      14.13       1.00
  6      se bcl vel tend                               201.75243        24        8.26866        8.45388        8.38534     6.76      68.88       1.00
  7       ocn_tend_vel                                 200.86768        24        8.22773        8.41779        8.34859     6.73      99.56       1.00
  8        bulk_ws                                       1.05533        24        0.04266        0.04515        0.04339     0.04       0.53       0.99
  8        coriolis                                     61.78329        24        2.50016        2.60742        2.56351     2.07      30.76       1.00
  8        vel vadv                                      8.29534        24        0.32888        0.35737        0.34404     0.28       4.13       1.00
  8        pressure grad                                42.45175        24        1.73500        1.78171        1.76448     1.42      21.13       1.00
  8        vel hmix                                     45.86026        24        1.82847        1.91909        1.87152     1.54      22.83       0.98
  9         vel del4                                    44.99939        24        1.79746        1.88665        1.83755     1.51      98.12       0.98
  8        vel surface stress                           43.92964        24        1.68870        1.83119        1.76155     1.47      21.87       0.96
  6      bcl iters on linear Coriolis                   92.14563        36        2.50102        2.60965        2.54557     3.09      31.46       0.99
  7       ocn_fuperp                                    79.29597        36        2.08357        2.21537        2.14873     2.66      86.06       0.98
```
     
### Data Layer
This folder contains the folder outputs for each testcase and HPC system
```
data/
 |__LANL_Badge/
 |__LANL_Grizzly/
 |__NERSC_Cori_Haswell/
 |__NERSC_Cori_KNL/
 |__ORNL_Summit/
```
## HPC Cluster performance
<!-- This is an h1 heading -->
### Compile
```sh
$ python3 HPC_cluster_system_performance.py
```
### Data HPC
Each file contains performance measures for each testcase and HPC system 
```sh
data/
  |__EC60to30_badger.txt
  |__EC60to30_Cori_Haswell.txt
  |__EC60to30_Cori_KNLl.txt
  |__EC60to30_grizzly.txt
  |__RRS18to6_badger.txt
  |__RRS18to6_Cori_Haswell.txt
  |__RRS18to6_grizzly.txt
  |__RRS30to10_badger.txt
  |__RRS30to10_Cori_Haswell.txt
  |__RRS30to10_grizzly.txt
```
<!-- 
#### Sub-sub-heading
This is an h3 heading
-->

## Rules
Here are the rules for (or lack thereof):
   1. Push changes directly to head of https://github.com/hrmoncada/MPAS-Performance-Plotting
   2. No pull requests or reviews are needed, unless you would like one. This means that personal forks of /MPAS-Performance-Plotting are not needed.
   3. Only restriction is to not overwrite files others have uploaded, without asking them.
   4. Scripts are not required to work in any particular way. The purpose is for the convenience of sharing scripts of any kind. Scripts do not come with any guarantees.
   5. Files may include everything, such as source code, source binary, figures and grapghics.
   6. Files should generally be a few MB or less. If a single file is larger than 2 to 5 MB, please keep some graphics as examples, keep the code, but clear the remaining graphics before saving.
   7. When the repository becomes too large (>~100MB) we reserve the right to purge the history in order to reduce the size.
