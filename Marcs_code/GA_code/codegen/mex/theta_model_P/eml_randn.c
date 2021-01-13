/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * eml_randn.c
 *
 * Code generation for function 'eml_randn'
 *
 */

/* Include files */
#include "eml_randn.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"

/* Variable Definitions */
static uint32_T b_method;
static boolean_T b_method_not_empty;
static uint32_T d_state[2];
static boolean_T d_state_not_empty;

/* Function Definitions */
void eml_randn_free(void)
{
  b_method_not_empty = false;
  d_state_not_empty = false;
}

void eml_randn_init(void)
{
  b_method = 0U;
  b_method_not_empty = true;
  d_state[0] = 362436069U;
  d_state[1] = 0U;
  d_state[1] = 521288629U;
  d_state_not_empty = true;
}

void method_not_empty_init(void)
{
  b_method_not_empty = false;
}

void state_not_empty_init(void)
{
  d_state_not_empty = false;
}

/* End of code generation (eml_randn.c) */
