/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * applyScalarFunction.h
 *
 * Code generation for function 'applyScalarFunction'
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
void applyScalarFunction(const emlrtStack *sp, const real_T x_data[], const
  int32_T x_size[1], real_T z1_data[], int32_T z1_size[1]);

/* End of code generation (applyScalarFunction.h) */
