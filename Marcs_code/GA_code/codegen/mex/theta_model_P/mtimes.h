/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * mtimes.h
 *
 * Code generation for function 'mtimes'
 *
 */

#pragma once

/* Include files */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mex.h"
#include "emlrt.h"
#include "rtwtypes.h"
#include "omp.h"
#include "theta_model_P_types.h"

/* Function Declarations */
void mtimes(const emxArray_real_T *A, const real_T B_data[], const int32_T
            B_size[1], real_T C_data[], int32_T C_size[1]);

/* End of code generation (mtimes.h) */
