/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * theta_model_P_terminate.c
 *
 * Code generation for function 'theta_model_P_terminate'
 *
 */

/* Include files */
#include "theta_model_P_terminate.h"
#include "_coder_theta_model_P_mex.h"
#include "eml_rand.h"
#include "eml_rand_mcg16807_stateful.h"
#include "eml_rand_mt19937ar_stateful.h"
#include "eml_rand_shr3cong_stateful.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"
#include "theta_model_P_data.h"

/* Function Definitions */
void theta_model_P_atexit(void)
{
  emlrtStack st = { NULL,              /* site */
    NULL,                              /* tls */
    NULL                               /* prev */
  };

  mexFunctionCreateRootTLS();
  st.tls = emlrtRootTLSGlobal;
  emlrtEnterRtStackR2012b(&st);
  c_eml_rand_mt19937ar_stateful_f();
  eml_rand_shr3cong_stateful_free();
  eml_rand_mcg16807_stateful_free();
  eml_rand_free();
  emlrtLeaveRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
  emlrtExitTimeCleanup(&emlrtContextGlobal);
}

void theta_model_P_terminate(void)
{
  emlrtStack st = { NULL,              /* site */
    NULL,                              /* tls */
    NULL                               /* prev */
  };

  st.tls = emlrtRootTLSGlobal;
  emlrtLeaveRtStackR2012b(&st);
  emlrtDestroyRootTLS(&emlrtRootTLSGlobal);
}

/* End of code generation (theta_model_P_terminate.c) */
