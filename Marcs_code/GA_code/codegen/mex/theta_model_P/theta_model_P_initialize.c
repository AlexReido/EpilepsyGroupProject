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
#include "eml_rand.h"
#include "eml_rand_mcg16807_stateful.h"
#include "eml_rand_mt19937ar_stateful.h"
#include "eml_rand_shr3cong_stateful.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"
#include "theta_model_P_data.h"

/* Function Declarations */
static void theta_model_P_once(void);

/* Function Definitions */
static void theta_model_P_once(void)
{
  mex_InitInfAndNan();
  c_eml_rand_mt19937ar_stateful_f();
  eml_rand_shr3cong_stateful_free();
  eml_rand_mcg16807_stateful_free();
  eml_rand_free();
  eml_rand_init();
  eml_rand_mcg16807_stateful_init();
  eml_rand_shr3cong_stateful_init();
  c_eml_rand_mt19937ar_stateful_i();
}

void theta_model_P_initialize(void)
{
  emlrtStack st = { NULL,              /* site */
    NULL,                              /* tls */
    NULL                               /* prev */
  };

  mexFunctionCreateRootTLS();
  emlrtBreakCheckR2012bFlagVar = emlrtGetBreakCheckFlagAddressR2012b();
  st.tls = emlrtRootTLSGlobal;
  emlrtClearAllocCountR2012b(&st, false, 0U, 0);
  emlrtEnterRtStackR2012b(&st);
  if (emlrtFirstTimeR2012b(emlrtRootTLSGlobal)) {
    theta_model_P_once();
  }
}

/* End of code generation (theta_model_P_initialize.c) */
