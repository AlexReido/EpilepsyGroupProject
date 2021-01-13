/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * rand.c
 *
 * Code generation for function 'rand'
 *
 */

/* Include files */
#include "rand.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"

/* Function Definitions */
void b_rand(real_T varargin_1, real_T r_data[], int32_T r_size[1])
{
  int32_T i;
  i = (int32_T)varargin_1;
  r_size[0] = i;
  if (i != 0) {
    emlrtRandu(&r_data[0], (int32_T)varargin_1);
  }
}

/* End of code generation (rand.c) */
