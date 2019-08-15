# MPAS-Performance-Plotting
This is a control version private repository for the development and sharing (public, no available) . 
The python code store in this repository read the outputs from MPAS testcase which were executed on differents HPC cluster. The outputs have information about the layer subroutine performance 

## Table of Contents
- [Layer performance evaluation](#Layer-performance-evaluation)
  * [Compile](#Compile)
<!-- 
    + [Sub-sub-heading](#sub-sub-heading)
-->
- [HPC Cluster performance](#HPC-Cluster-performance)
  * [Compile](#Compile)
<!-- 
    + [Sub-sub-heading](#sub-sub-heading-1)
-->
- [Rules](#Rules)

<!-- Comments -->

## Layer performance evaluation
<!-- This is an h1 heading -->
## Compile
```sh
$ python3 Layer_subroutine_performance.py  ' 5 '
```
<!-- 
#### Sub-sub-heading
This is an h3 heading
-->

## HPC Cluster performance
<!-- This is an h1 heading -->
## Compile
```sh
$ python3 HPC_cluster_system_performance.py
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
