/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * theta_model_P_mexutil.c
 *
 * Code generation for function 'theta_model_P_mexutil'
 *
 */

/* Include files */
#include "theta_model_P_mexutil.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"
#include "theta_model_P_data.h"

/* Function Definitions */
emlrtCTX emlrtGetRootTLSGlobal(void)
{
  return emlrtRootTLSGlobal;
}

void emlrtLockerFunction(EmlrtLockeeFunction aLockee, const emlrtConstCTX aTLS,
  void *aData)
{
  omp_set_lock(&emlrtLockGlobal);
  emlrtCallLockeeFunction(aLockee, aTLS, aData);
  omp_unset_lock(&emlrtLockGlobal);
}

/* End of code generation (theta_model_P_mexutil.c) */
