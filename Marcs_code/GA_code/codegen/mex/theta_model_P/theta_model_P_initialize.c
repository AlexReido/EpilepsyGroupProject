/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * theta_model_P_initialize.c
 *
 * Code generation for function 'theta_model_P_initialize'
 *
 */

/* Include files */
#include "theta_model_P_initialize.h"
#include "_coder_theta_model_P_mex.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"
#include "theta_model_P_data.h"

/* Function Definitions */
void theta_model_P_initialize(void)
{
  emlrtStack st = { NULL,              /* site */
    NULL,                              /* tls */
    NULL                               /* prev */
  };

  mex_InitInfAndNan();
  mexFunctionCreateRootTLS();
  emlrtBreakCheckR2012bFlagVar = emlrtGetBreakCheckFlagAddressR2012b();
  st.tls = emlrtRootTLSGlobal;
  emlrtClearAllocCountR2012b(&st, false, 0U, 0);
  emlrtEnterRtStackR2012b(&st);
  emlrtFirstTimeR2012b(emlrtRootTLSGlobal);
}

/* End of code generation (theta_model_P_initialize.c) */
