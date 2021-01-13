/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * eml_rand_mt19937ar_stateful.c
 *
 * Code generation for function 'eml_rand_mt19937ar_stateful'
 *
 */

/* Include files */
#include "eml_rand_mt19937ar_stateful.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"
#include <string.h>

/* Variable Definitions */
static uint32_T c_state[625];
static boolean_T c_state_not_empty;

/* Function Definitions */
void c_eml_rand_mt19937ar_stateful_f(void)
{
  c_state_not_empty = false;
}

void c_eml_rand_mt19937ar_stateful_i(void)
{
  uint32_T r;
  int32_T mti;
  memset(&c_state[0], 0, 625U * sizeof(uint32_T));
  r = 5489U;
  c_state[0] = 5489U;
  for (mti = 0; mti < 623; mti++) {
    r = ((r ^ r >> 30U) * 1812433253U + mti) + 1U;
    c_state[mti + 1] = r;
  }

  c_state[624] = 624U;
  c_state_not_empty = true;
}

/* End of code generation (eml_rand_mt19937ar_stateful.c) */
