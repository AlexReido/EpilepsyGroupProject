/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * eml_rand_mcg16807_stateful.c
 *
 * Code generation for function 'eml_rand_mcg16807_stateful'
 *
 */

/* Include files */
#include "eml_rand_mcg16807_stateful.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"

/* Variable Definitions */
static uint32_T state;
static boolean_T state_not_empty;

/* Function Definitions */
void eml_rand_mcg16807_stateful_free(void)
{
  state_not_empty = false;
}

void eml_rand_mcg16807_stateful_init(void)
{
  state = 1144108930U;
  state_not_empty = true;
}

/* End of code generation (eml_rand_mcg16807_stateful.c) */
