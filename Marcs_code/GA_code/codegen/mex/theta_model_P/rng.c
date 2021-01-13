/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * rng.c
 *
 * Code generation for function 'rng'
 *
 */

/* Include files */
#include "rng.h"
#include "rt_nonfinite.h"
#include "theta_model_P.h"

/* Variable Definitions */
static uint32_T seed;
static boolean_T seed_not_empty;

/* Function Definitions */
void rng_free(void)
{
  seed_not_empty = false;
}

void rng_init(void)
{
  seed = 0U;
  seed_not_empty = true;
}

/* End of code generation (rng.c) */
