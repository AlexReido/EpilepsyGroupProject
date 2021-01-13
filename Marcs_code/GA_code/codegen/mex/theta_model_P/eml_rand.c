/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * eml_rand.c
 *
 * Code generation for function 'eml_rand'
 *
 */

/* Include files */
#include "eml_rand.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"

/* Variable Definitions */
static uint32_T method;
static boolean_T method_not_empty;

/* Function Definitions */
void eml_rand_free(void)
{
  method_not_empty = false;
}

void eml_rand_init(void)
{
  method = 7U;
  method_not_empty = true;
}

/* End of code generation (eml_rand.c) */
